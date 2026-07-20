"""Ray Train lab: FashionMNIST on GPUs via TorchTrainer + MLflow.

OpenShift AI managed MLflow (3.4+) requires:
  MLFLOW_TRACKING_URI   https://<rhoai-dashboard-host>/mlflow
  MLFLOW_TRACKING_TOKEN OpenShift user token (Console / oc whoami -t)
  MLFLOW_WORKSPACE      OpenShift project name (e.g. ray-workshop)

Do NOT use MLFLOW_TRACKING_AUTH=kubernetes-namespaced from Ray workers — the
dashboard gateway rejects service-account tokens (RHOAIENG-44516). Pass the
same user token you use for CodeFlare AuthConfig.

Env:
  NUM_EPOCHS                 default 3
  NUM_WORKERS                default 2
  MLFLOW_TRACKING_URI        required
  MLFLOW_TRACKING_TOKEN      required
  MLFLOW_WORKSPACE           default ray-workshop
  MLFLOW_TRACKING_INSECURE_TLS  default true (lab self-signed certs)
  MLFLOW_EXPERIMENT          default ray-workshop-fashion-mnist
  MLFLOW_REGISTERED_MODEL    default ray-workshop-fashion-mnist
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

import mlflow
import mlflow.pytorch
import ray
import torch
import torch.nn as nn
from ray.train import ScalingConfig
from ray.train.torch import TorchTrainer
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor

BATCH_SIZE = 64
LEARNING_RATE = 0.01
NUM_CLASSES = 10
FASHION_MNIST_CLASSES = (
    "T-shirt/top",
    "Trouser",
    "Pullover",
    "Dress",
    "Coat",
    "Sandal",
    "Shirt",
    "Sneaker",
    "Bag",
    "Ankle boot",
)


class NeuralNetwork(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(28 * 28, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 10),
        )

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        inputs = self.flatten(inputs)
        return self.linear_relu_stack(inputs)


def get_dataset(*, train: bool = True) -> datasets.FashionMNIST:
    return datasets.FashionMNIST(
        root="/tmp/data",
        train=train,
        download=True,
        transform=ToTensor(),
    )


def _unwrap_model(model: nn.Module) -> nn.Module:
    return model.module if hasattr(model, "module") else model


@torch.no_grad()
def _evaluate(model: nn.Module, dataloader: DataLoader) -> tuple[float, float]:
    """Return mean cross-entropy loss and accuracy over dataloader."""
    model.eval()
    criterion = nn.CrossEntropyLoss(reduction="sum")
    total_loss = 0.0
    correct = 0
    total = 0
    device = next(model.parameters()).device
    for inputs, labels in dataloader:
        inputs = inputs.to(device)
        labels = labels.to(device)
        pred = model(inputs)
        total_loss += float(criterion(pred, labels).item())
        correct += int((pred.argmax(dim=1) == labels).sum().item())
        total += labels.size(0)
    if total == 0:
        return 0.0, 0.0
    return total_loss / total, correct / total


@torch.no_grad()
def _confusion_matrix(
    model: nn.Module, dataloader: DataLoader, num_classes: int = NUM_CLASSES
) -> torch.Tensor:
    """Return [true, pred] confusion counts."""
    model.eval()
    device = next(model.parameters()).device
    cm = torch.zeros(num_classes, num_classes, dtype=torch.int64)
    for inputs, labels in dataloader:
        inputs = inputs.to(device)
        labels = labels.to(device)
        preds = model(inputs).argmax(dim=1)
        for true_label, pred_label in zip(labels.view(-1), preds.view(-1)):
            cm[int(true_label), int(pred_label)] += 1
    return cm


def _configure_mlflow() -> tuple[str, str]:
    """Configure MLflow for OpenShift AI managed tracking (token + workspace)."""
    # Ray SA + kubernetes-namespaced fails at the RHOAI gateway — force token auth.
    os.environ.pop("MLFLOW_TRACKING_AUTH", None)

    tracking_uri = os.environ.get("MLFLOW_TRACKING_URI", "").strip()
    token = os.environ.get("MLFLOW_TRACKING_TOKEN", "").strip()
    workspace = os.environ.get("MLFLOW_WORKSPACE", "ray-workshop").strip()
    os.environ.setdefault("MLFLOW_TRACKING_INSECURE_TLS", "true")

    if not tracking_uri:
        raise RuntimeError(
            "MLFLOW_TRACKING_URI is required "
            "(e.g. https://rh-ai.apps.EXAMPLE.com/mlflow)"
        )
    if not token:
        raise RuntimeError(
            "MLFLOW_TRACKING_TOKEN is required. Pass your OpenShift Console "
            "user token (same as CodeFlare AuthConfig) — Ray service-account "
            "tokens are not accepted by OpenShift AI MLflow."
        )

    os.environ["MLFLOW_TRACKING_URI"] = tracking_uri
    os.environ["MLFLOW_TRACKING_TOKEN"] = token
    os.environ["MLFLOW_WORKSPACE"] = workspace

    mlflow.set_tracking_uri(tracking_uri)
    if hasattr(mlflow, "set_workspace"):
        mlflow.set_workspace(workspace)

    return tracking_uri, workspace


def train_func_distributed(config: dict) -> None:
    num_epochs = int(os.environ.get("NUM_EPOCHS", "3"))
    mlflow_run_id = config["mlflow_run_id"]
    registered_model = config["registered_model"]

    _configure_mlflow()

    train_dataset = get_dataset(train=True)
    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    train_loader = ray.train.torch.prepare_data_loader(train_loader)

    model = NeuralNetwork()
    model = ray.train.torch.prepare_model(model)

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=LEARNING_RATE)

    rank = ray.train.get_context().get_world_rank()

    # Non-distributed loaders for post-epoch eval (rank 0 only).
    eval_train_loader = DataLoader(
        get_dataset(train=True), batch_size=BATCH_SIZE, shuffle=False
    )
    eval_test_loader = DataLoader(
        get_dataset(train=False), batch_size=BATCH_SIZE, shuffle=False
    )

    for epoch in range(num_epochs):
        model.train()
        if ray.train.get_context().get_world_size() > 1:
            train_loader.sampler.set_epoch(epoch)

        for inputs, labels in train_loader:
            optimizer.zero_grad()
            pred = model(inputs)
            loss = criterion(pred, labels)
            loss.backward()
            optimizer.step()

        # Post-epoch eval on rank 0, then broadcast so every worker reports
        # the same metrics (Ray averages worker reports by default).
        metrics_tensor = torch.zeros(4, device=next(model.parameters()).device)
        if rank == 0:
            unwrapped = _unwrap_model(model)
            train_loss, train_acc = _evaluate(unwrapped, eval_train_loader)
            test_loss, test_acc = _evaluate(unwrapped, eval_test_loader)
            metrics_tensor[0] = train_loss
            metrics_tensor[1] = train_acc
            metrics_tensor[2] = test_loss
            metrics_tensor[3] = test_acc
            print(
                f"epoch: {epoch}, "
                f"train_loss: {train_loss:.4f}, train_accuracy: {train_acc:.4f}, "
                f"test_loss: {test_loss:.4f}, test_accuracy: {test_acc:.4f}"
            )
            with mlflow.start_run(run_id=mlflow_run_id):
                mlflow.log_metric("train_loss", train_loss, step=epoch)
                mlflow.log_metric("train_accuracy", train_acc, step=epoch)
                mlflow.log_metric("test_loss", test_loss, step=epoch)
                mlflow.log_metric("test_accuracy", test_acc, step=epoch)

        if ray.train.get_context().get_world_size() > 1:
            torch.distributed.broadcast(metrics_tensor, src=0)

        train_loss, train_acc, test_loss, test_acc = (
            float(metrics_tensor[0]),
            float(metrics_tensor[1]),
            float(metrics_tensor[2]),
            float(metrics_tensor[3]),
        )
        ray.train.report(
            {
                "train_loss": train_loss,
                "train_accuracy": train_acc,
                "test_loss": test_loss,
                "test_accuracy": test_acc,
            }
        )

    if rank == 0:
        unwrapped = _unwrap_model(model).cpu().eval()
        test_loader = DataLoader(
            get_dataset(train=False), batch_size=BATCH_SIZE, shuffle=False
        )
        test_loss, test_acc = _evaluate(unwrapped, test_loader)
        cm = _confusion_matrix(unwrapped, test_loader)
        print(f"final test_loss: {test_loss:.4f}, test_accuracy: {test_acc:.4f}")

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            checkpoint_path = tmp_path / "checkpoint.pt"
            torch.save(unwrapped.state_dict(), checkpoint_path)

            cm_path = tmp_path / "confusion_matrix.csv"
            with cm_path.open("w", encoding="utf-8") as handle:
                handle.write("true_class,pred_class,count\n")
                for true_idx in range(NUM_CLASSES):
                    for pred_idx in range(NUM_CLASSES):
                        count = int(cm[true_idx, pred_idx].item())
                        if count:
                            handle.write(f"{true_idx},{pred_idx},{count}\n")

            with mlflow.start_run(run_id=mlflow_run_id):
                mlflow.log_metric("final_test_loss", test_loss)
                mlflow.log_metric("final_test_accuracy", test_acc)
                for class_idx in range(NUM_CLASSES):
                    class_total = int(cm[class_idx].sum().item())
                    class_correct = int(cm[class_idx, class_idx].item())
                    class_acc = (
                        class_correct / class_total if class_total else 0.0
                    )
                    mlflow.log_metric(f"class_correct_{class_idx}", class_correct)
                    mlflow.log_metric(f"class_accuracy_{class_idx}", class_acc)
                    mlflow.log_param(
                        f"class_name_{class_idx}", FASHION_MNIST_CLASSES[class_idx]
                    )

                mlflow.log_artifact(str(checkpoint_path))
                mlflow.log_artifact(str(cm_path))
                # Use pickle — MLflow 3.x defaults to pt2, which needs TensorSpec signatures.
                mlflow.pytorch.log_model(
                    unwrapped,
                    artifact_path="model",
                    registered_model_name=registered_model,
                    serialization_format="pickle",
                )
        print(
            f"MLflow: logged checkpoint.pt, confusion_matrix.csv, and PyTorch model "
            f"to run {mlflow_run_id}, registered_model_name={registered_model}"
        )


def main() -> None:
    tracking_uri, workspace = _configure_mlflow()

    num_workers = int(os.environ.get("NUM_WORKERS", "2"))
    num_epochs = int(os.environ.get("NUM_EPOCHS", "3"))
    experiment = os.environ.get("MLFLOW_EXPERIMENT", "ray-workshop-fashion-mnist")
    registered_model = os.environ.get(
        "MLFLOW_REGISTERED_MODEL", "ray-workshop-fashion-mnist"
    )

    mlflow.set_experiment(experiment)

    print(
        f"Starting TorchTrainer: num_workers={num_workers}, use_gpu=True, "
        f"mlflow_uri={tracking_uri}, workspace={workspace}, "
        f"experiment={experiment}"
    )

    with mlflow.start_run(run_name="fashion-mnist-ray-train") as run:
        mlflow.set_tags(
            {
                "framework": "ray-train",
                "dataset": "FashionMNIST",
                "accelerator": "gpu",
                "workspace": workspace,
            }
        )
        mlflow.log_param("num_workers", num_workers)
        mlflow.log_param("num_epochs", num_epochs)
        mlflow.log_param("batch_size", BATCH_SIZE)
        mlflow.log_param("lr", LEARNING_RATE)
        mlflow.log_param("use_gpu", True)

        trainer = TorchTrainer(
            train_func_distributed,
            train_loop_config={
                "mlflow_run_id": run.info.run_id,
                "registered_model": registered_model,
            },
            scaling_config=ScalingConfig(
                num_workers=num_workers,
                use_gpu=True,
                resources_per_worker={"CPU": 1},
            ),
        )
        trainer.fit()
        print(f"MLflow run_id={run.info.run_id} experiment={experiment}")
        print("Done. Ray Train FashionMNIST finished successfully.")


if __name__ == "__main__":
    main()
