import shutil
from collections import defaultdict
from pathlib import Path
from typing import Union, Callable, Dict, Optional

from torch import nn
from torch.optim import Optimizer, AdamW
from torch.utils.data import DataLoader, Dataset, Sampler, RandomSampler
from tqdm import tqdm

from dnn_cool_train_loop.metrics import _flush_all_metrics, _get_epoch_dir
from dnn_cool_train_loop.task_loop import _process_batch


def train_for_one_epoch(
    epoch: int,
    model: nn.Module,
    train_dataset: Dataset,
    criterion_dict: Dict[str, Callable],
    batch_size_effective: int,
    metrics_dir: Optional[Union[str, Path]] = None,
    metrics_dict: Dict[str, Dict[str, Callable]] = None,
    optimizer: Optional[Optimizer] = None,
    lr: Optional[float] = 1e-4,
    sampler: Optional[Sampler] = None,
    n_flush_metrics: int = 1_000,
    epoch_zfill=4,
) -> None:
    """
    Trains the specified PyTorch model for one epoch on the given dataset.

    Args:
        epoch (int): The current epoch number.
        model (nn.Module): The PyTorch model to train.
        train_dataset (Dataset): The dataset to train on.
        criterion_dict (Dict[str, Callable]): A dictionary of PyTorch loss functions, where
            the keys are the names of the losses and the values are the loss functions.
        batch_size_effective (int): The effective batch size to use for training.
        metrics_dir (Optional[Union[str, Path]]): The directory to save metrics to (e.g. loss,
            accuracy). If None, no metrics will be saved.
        metrics_dict (Dict[str, Dict[str, Callable]]): A dictionary of metrics, where the keys
            are the names of the metrics and the values are dictionaries of additional arguments
            to pass to the metric functions. If None, no metrics will be calculated.
        optimizer (Optional[Optimizer]): The PyTorch optimizer to use. If None, no optimizer
            will be used.
        lr (Optional[float]): The learning rate for the optimizer. Only used if an optimizer is
            provided.
        sampler (Optional[Sampler]): The sampler to use for sampling data from the dataset.
            If None, the dataset will be iterated through sequentially.
        n_flush_metrics (int): The number of batches to train on before flushing metrics to disk.
        epoch_zfill (int): The zero-padding for the epoch number when printing progress.

    Returns:
        None: This function doesn't return anything, but trains the specified model for one epoch
        and saves metrics (if specified).
    """

    model.train()
    epoch = str(epoch).zfill(epoch_zfill)
    epoch_metrics_dir = _get_epoch_dir(epoch, "train", metrics_dir)
    print(f"Train epoch {epoch} ...")
    if sampler is None:
        sampler = RandomSampler(train_dataset)
    if optimizer is None:
        optimizer = AdamW(model.parameters(), lr=lr)
    loader = DataLoader(dataset=train_dataset, batch_size=1, sampler=sampler)
    device = next(model.parameters()).device
    metric_values_dict = defaultdict(list)
    for i, data in enumerate(tqdm(loader)):
        total_loss = _process_batch(
            model=model,
            batch_size_effective=batch_size_effective,
            criterion_dict=criterion_dict,
            metrics_dir=epoch_metrics_dir,
            metrics_dict=metrics_dict,
            metric_values_dict=metric_values_dict,
            data=data,
            device=device,
        )
        total_loss.backward()
        if (i + 1) % batch_size_effective == 0:
            optimizer.step()
            optimizer.zero_grad()
        if (i + 1) % n_flush_metrics == 0:
            _flush_all_metrics(epoch_metrics_dir, metric_values_dict)
    # Optimizer step for the last batch
    if len(train_dataset) % batch_size_effective != 0:
        optimizer.step()
        optimizer.zero_grad()
    # Flush metrics for last batch.
    if len(train_dataset) % n_flush_metrics != 0:
        _flush_all_metrics(epoch_metrics_dir, metric_values_dict)
    model.eval()
