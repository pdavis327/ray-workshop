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


def get_dataset() -> datasets.FashionMNIST:
    return datasets.FashionMNIST(
        root="/tmp/data",
        train=True,
        download=True,
        transform=ToTensor(),
    )


def _unwrap_model(model: nn.Module) -> nn.Module:
    return model.module if hasattr(model, "module") else model


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

    dataset = get_dataset()
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)
    dataloader = ray.train.torch.prepare_data_loader(dataloader)

    model = NeuralNetwork()
    model = ray.train.torch.prepare_model(model)

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=LEARNING_RATE)

    rank = ray.train.get_context().get_world_rank()

    for epoch in range(num_epochs):
        if ray.train.get_context().get_world_size() > 1:
            dataloader.sampler.set_epoch(epoch)

        last_loss = None
        for inputs, labels in dataloader:
            optimizer.zero_grad()
            pred = model(inputs)
            loss = criterion(pred, labels)
            loss.backward()
            optimizer.step()
            last_loss = loss.item()

        print(f"epoch: {epoch}, loss: {last_loss}")
        ray.train.report({"loss": last_loss})

        if rank == 0 and last_loss is not None:
            with mlflow.start_run(run_id=mlflow_run_id):
                mlflow.log_metric("loss", float(last_loss), step=epoch)

    if rank == 0:
        unwrapped = _unwrap_model(model).cpu().eval()
        with mlflow.start_run(run_id=mlflow_run_id):
            # Use pickle — MLflow 3.x defaults to pt2, which needs TensorSpec signatures.
            mlflow.pytorch.log_model(
                unwrapped,
                artifact_path="model",
                registered_model_name=registered_model,
                serialization_format="pickle",
            )
        print(
            f"MLflow: logged PyTorch model to run {mlflow_run_id}, "
            f"registered_model_name={registered_model}"
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
