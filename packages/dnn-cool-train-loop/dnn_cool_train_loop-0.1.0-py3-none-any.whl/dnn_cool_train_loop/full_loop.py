from functools import partial
from pathlib import Path
from typing import Union, Callable, Dict, Optional

from torch import nn
from torch.optim import Optimizer
from torch.utils.data import Dataset, Sampler

from dnn_cool_train_loop.valid_loop import validate_for_one_epoch
from dnn_cool_train_loop.train_loop import train_for_one_epoch


def train_for_epochs(
    start_epoch: int,
    n_epochs: int,
    model: nn.Module,
    train_dataset: Dataset,
    val_dataset: Dataset,
    criterion_dict: Dict[str, Callable],
    batch_size_effective: int,
    metrics_dir: Optional[Union[str, Path]] = None,
    metrics_dict: Dict[str, Dict[str, Callable]] = None,
    optimizer: Optional[Optimizer] = None,
    lr: Optional[float] = 1e-4,
    sampler: Optional[Sampler] = None,
    n_flush_metrics: int = 1_000,
):
    train_fn = partial(
        train_for_one_epoch,
        model=model,
        train_dataset=train_dataset,
        criterion_dict=criterion_dict,
        batch_size_effective=batch_size_effective,
        metrics_dir=metrics_dir,
        metrics_dict=metrics_dict,
        optimizer=optimizer,
        lr=lr,
        sampler=sampler,
        n_flush_metrics=n_flush_metrics,
    )
    valid_fn = partial(
        validate_for_one_epoch,
        model=model,
        val_dataset=val_dataset,
        criterion_dict=criterion_dict,
        batch_size_effective=batch_size_effective,
        metrics_dir=metrics_dir,
        metrics_dict=metrics_dict,
        n_flush_metrics=n_flush_metrics,
    )
    for i in range(start_epoch, start_epoch + n_epochs):
        train_fn(i)
        valid_fn(i)
