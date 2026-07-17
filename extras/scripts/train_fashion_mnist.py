"""Ray Train lab: FashionMNIST on GPUs via TorchTrainer.

Requires a RayCluster with enough GPU workers for ScalingConfig.num_workers
(workshop default: 2 workers × 1 GPU). Workers need egress (or pre-cached data)
to download FashionMNIST on first run.

Env:
  NUM_EPOCHS   default 3
  NUM_WORKERS  default 2  (must match available GPU Ray workers)
"""

from __future__ import annotations

import os

import ray
import torch
import torch.nn as nn
from ray.train import ScalingConfig
from ray.train.torch import TorchTrainer
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor


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


def train_func_distributed() -> None:
    num_epochs = int(os.environ.get("NUM_EPOCHS", "3"))
    batch_size = 64

    dataset = get_dataset()
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    dataloader = ray.train.torch.prepare_data_loader(dataloader)

    model = NeuralNetwork()
    model = ray.train.torch.prepare_model(model)

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

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


def main() -> None:
    num_workers = int(os.environ.get("NUM_WORKERS", "2"))
    print(f"Starting TorchTrainer: num_workers={num_workers}, use_gpu=True")

    trainer = TorchTrainer(
        train_func_distributed,
        scaling_config=ScalingConfig(
            num_workers=num_workers,
            use_gpu=True,
            resources_per_worker={"CPU": 1},
        ),
    )
    trainer.fit()
    print("Done. Ray Train FashionMNIST finished successfully.")


if __name__ == "__main__":
    main()
