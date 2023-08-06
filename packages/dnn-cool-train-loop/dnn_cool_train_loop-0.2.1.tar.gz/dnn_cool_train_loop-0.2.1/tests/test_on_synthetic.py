# %%
from functools import partial

import torch

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from torch import nn

from dnn_cool_synthetic_dataset.base import create_dataset
from torch.utils.data import Dataset, Subset
from pathlib import Path
from mmap_ninja import numpy as np_ninja
from mmap_ninja.ragged import RaggedMmap
from mmap_ninja.string import StringsMmap
from collections import defaultdict
from mmap_ninja_dataframe.sparse import SparseDataFrameMmap

from dnn_cool_train_loop.train_loop import train_for_one_epoch
from dnn_cool_train_loop.valid_loop import validate_for_one_epoch


def img_normalize_255(x):
    return torch.tensor(x, dtype=torch.float32).permute(2, 0, 1) / 255.0


def binary_target(x):
    return torch.tensor(x, dtype=torch.float32).unsqueeze(0)


def regression_target(x):
    return torch.tensor(x, dtype=torch.float32).unsqueeze(0) / 64


def multilabel_classification_target(x):
    return torch.tensor(x, dtype=torch.float32)


def binary_accuracy(outputs, labels):
    predicted = outputs.item() > 0.5
    actual = labels.item()
    return predicted == actual


class SyntheticDatasetModule(nn.Module):
    def __init__(self):
        super().__init__()
        self.seq = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=5),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 128, kernel_size=5),
            nn.ReLU(inplace=True),
            nn.AvgPool2d(2),
            nn.Conv2d(128, 128, kernel_size=5),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 256, kernel_size=5),
            nn.AvgPool2d(2),
            nn.ReLU(inplace=True),
        )

        self.features_seq = nn.Sequential(
            nn.Conv2d(256, 256, kernel_size=5),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=5),
            nn.ReLU(inplace=True),
            nn.AdaptiveAvgPool2d(1),
            nn.Flatten(),
        )

        self.camera_blocked = nn.Linear(256, 1)
        self.door_open = nn.Linear(256, 1)
        self.door_locked = nn.Linear(256, 1)
        self.person_present = nn.Linear(256, 1)

        self.body_x1 = nn.Linear(256, 1)
        self.body_y1 = nn.Linear(256, 1)
        self.body_w = nn.Linear(256, 1)
        self.body_h = nn.Linear(256, 1)

        self.face_x1 = nn.Linear(256, 1)
        self.face_y1 = nn.Linear(256, 1)
        self.face_w = nn.Linear(256, 1)
        self.face_h = nn.Linear(256, 1)

        self.shirt_type = nn.Linear(256, 7)
        self.facial_characteristics = nn.Linear(256, 3)

    def forward(self, input_dict):
        x = input_dict["img"]
        common = self.seq(x)
        features = self.features_seq(common)

        return {
            "camera_blocked": self.camera_blocked(features),
            "door_open": self.door_open(features),
            "door_locked": self.door_locked(features),
            "person_present": self.person_present(features),
            "person_regression.body_regression.body_x1": self.body_x1(features).sigmoid(),
            "person_regression.body_regression.body_y1": self.body_y1(features).sigmoid(),
            "person_regression.body_regression.body_w": self.body_w(features).sigmoid(),
            "person_regression.body_regression.body_h": self.body_h(features).sigmoid(),
            "person_regression.face_regression.face_x1": self.face_x1(features).sigmoid(),
            "person_regression.face_regression.face_y1": self.face_y1(features).sigmoid(),
            "person_regression.face_regression.face_w": self.face_w(features).sigmoid(),
            "person_regression.face_regression.face_h": self.face_h(features).sigmoid(),
            "person_regression.body_regression.shirt_type": self.shirt_type(features),
            "person_regression.face_regression.facial_characteristics": self.facial_characteristics(features),
        }


def test_synthetic(tmp_path):
    dicts = create_dataset(10_000)
    SparseDataFrameMmap.from_list_of_dicts(tmp_path / "dataset", dicts)
    wrapper_fn_dict = {
        "img": img_normalize_255,
        "camera_blocked": binary_target,
        "door_open": binary_target,
        "door_locked": binary_target,
        "person_present": binary_target,
        "person_regression.body_regression.body_x1": regression_target,
        "person_regression.body_regression.body_y1": regression_target,
        "person_regression.body_regression.body_w": regression_target,
        "person_regression.body_regression.body_h": regression_target,
        "person_regression.face_regression.face_x1": regression_target,
        "person_regression.face_regression.face_y1": regression_target,
        "person_regression.face_regression.face_w": regression_target,
        "person_regression.face_regression.face_h": regression_target,
        "person_regression.body_regression.shirt_type": torch.tensor,
        "person_regression.face_regression.facial_characteristics": multilabel_classification_target,
    }
    target_keys = list(wrapper_fn_dict)
    target_keys.remove("img")

    dataset = SparseDataFrameMmap(tmp_path / "dataset", wrapper_fn_dict=wrapper_fn_dict, target_keys=target_keys)
    model = SyntheticDatasetModule()

    train_dataset = Subset(dataset, np.arange(8000))
    valid_dataset = Subset(dataset, np.arange(8000, 10_000))
    model = model.cuda()
    batch_size_effective = 64
    criterion_dict = {
        "camera_blocked": nn.BCEWithLogitsLoss(),
        "door_open": nn.BCEWithLogitsLoss(),
        "door_locked": nn.BCEWithLogitsLoss(),
        "person_present": nn.BCEWithLogitsLoss(),
        "person_regression.body_regression.body_x1": nn.MSELoss(),
        "person_regression.body_regression.body_y1": nn.MSELoss(),
        "person_regression.body_regression.body_w": nn.MSELoss(),
        "person_regression.body_regression.body_h": nn.MSELoss(),
        "person_regression.face_regression.face_x1": nn.MSELoss(),
        "person_regression.face_regression.face_y1": nn.MSELoss(),
        "person_regression.face_regression.face_w": nn.MSELoss(),
        "person_regression.face_regression.face_h": nn.MSELoss(),
        "person_regression.body_regression.shirt_type": nn.CrossEntropyLoss(),
        "person_regression.face_regression.facial_characteristics": nn.BCEWithLogitsLoss(),
    }
    metrics_dir = Path(tmp_path / "metrics")
    metrics_dict = {
        "camera_blocked": {
            "accuracy": binary_accuracy,
        }
    }

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
