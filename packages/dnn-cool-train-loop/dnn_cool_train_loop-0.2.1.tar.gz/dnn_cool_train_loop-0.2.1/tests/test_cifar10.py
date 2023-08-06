from functools import partial
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Subset
from torchvision import transforms
from torchvision.datasets import CIFAR10
from mmap_ninja_dataframe.dense import DataFrameMmap
from mmap_ninja import numpy as np_ninja

from dnn_cool_train_loop.train_loop import train_for_one_epoch
from dnn_cool_train_loop.valid_loop import validate_for_one_epoch


def generate_samples(trainset, testset):
    for X, y in trainset:
        yield {"img": np.asarray(X), "label": y}
    for X, y in testset:
        yield {"img": np.asarray(X), "label": y}


class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, input_dict):
        x = input_dict["img"]
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = torch.flatten(x, 1)  # flatten all dimensions except batch
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return {"label": x}


def correct_idx_probability(outputs, labels):
    idx = labels.item()
    return outputs[0, idx].sigmoid().item()


def accuracy(outputs, labels):
    return outputs[0].detach().cpu().numpy().argmax() == labels.item()


def prepare_cifar10_dataset(tmp_path):
    trainset = CIFAR10(root="./data", train=True, download=True)
    testset = CIFAR10(root="./data", train=False, download=True)
    out_dir = tmp_path
    DataFrameMmap.from_generator(
        out_dir / "df_mmap", generate_samples(trainset, testset), mode="sample", batch_size=1024, verbose=True
    )
    transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
    wrapper_fn_dict = {"img": transform}
    df = DataFrameMmap(out_dir / "df_mmap", wrapper_fn_dict=wrapper_fn_dict, target_keys=["label"])
    model = Net()
    train_dataset = Subset(df, list(range(len(trainset))))
    valid_dataset = Subset(df, list(range(len(trainset), len(df))))
    model = model.cuda()
    criterion_dict = {"label": nn.CrossEntropyLoss()}
    batch_size_effective = 64
    return batch_size_effective, criterion_dict, model, out_dir, train_dataset, valid_dataset


def test_cifar10(tmp_path):
    batch_size_effective, criterion_dict, model, out_dir, train_dataset, valid_dataset = prepare_cifar10_dataset(
        tmp_path
    )
    metrics_dir = Path(out_dir / "./metrics")
    metrics_dict = {"label": {"accuracy": accuracy, "correct_class_probability": correct_idx_probability}}

    train_fn = partial(
        train_for_one_epoch,
        model=model,
        train_dataset=train_dataset,
        criterion_dict=criterion_dict,
        batch_size_effective=batch_size_effective,
        metrics_dir=metrics_dir,
        metrics_dict=metrics_dict,
        lr=1e-3,
        n_flush_metrics=999,
    )
    valid_fn = partial(
        validate_for_one_epoch,
        model=model,
        valid_dataset=valid_dataset,
        criterion_dict=criterion_dict,
        batch_size_effective=batch_size_effective,
        metrics_dir=metrics_dir,
        metrics_dict=metrics_dict,
        n_flush_metrics=999,
    )

    valid_fn("init")
    for i in range(5):
        train_fn(i)
        valid_fn(i)
    loss_mmap = np_ninja.open_existing(metrics_dir / "valid" / "0004" / "label" / "accuracy" / "value")
    assert loss_mmap.mean() > 0.40


def test_cifar10_without_metrics(tmp_path):
    batch_size_effective, criterion_dict, model, out_dir, train_dataset, valid_dataset = prepare_cifar10_dataset(
        tmp_path
    )
    train_for_one_epoch(
        epoch=0,
        model=model,
        train_dataset=train_dataset,
        criterion_dict=criterion_dict,
        batch_size_effective=batch_size_effective,
        metrics_dir=None,
        metrics_dict=None,
        lr=1e-3,
        n_flush_metrics=999,
    )
    train_for_one_epoch(
        epoch=1,
        model=model,
        train_dataset=train_dataset,
        criterion_dict=criterion_dict,
        batch_size_effective=batch_size_effective,
        metrics_dir=Path(out_dir / "./metrics"),
        metrics_dict=None,
        lr=1e-3,
        n_flush_metrics=999,
    )
    train_for_one_epoch(
        epoch=1,
        model=model,
        train_dataset=train_dataset,
        criterion_dict=criterion_dict,
        batch_size_effective=batch_size_effective,
        metrics_dir=Path(out_dir / "./metrics"),
        metrics_dict={},
        lr=1e-3,
        n_flush_metrics=999,
    )
