import shutil
from collections import defaultdict
from pathlib import Path
from typing import Union, Callable, Dict, Optional

from torch import nn
from torch.optim import Optimizer, AdamW
from torch.utils.data import DataLoader, Dataset, Sampler, RandomSampler
from tqdm import tqdm

from dnn_cool_train_loop.metrics import _flush_all_metrics
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
):
    epoch = str(epoch).zfill(epoch_zfill)
    train_metrics_dir = None
    if metrics_dir is not None:
        train_metrics_dir = metrics_dir / "train" / epoch
        train_metrics_dir.mkdir(exist_ok=True, parents=True)
    print(f"Train epoch {epoch} ...")
    model.train()
    if metrics_dir is not None and train_metrics_dir.exists():
        shutil.rmtree(train_metrics_dir)
        train_metrics_dir = Path(train_metrics_dir)
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
            metrics_dir=train_metrics_dir,
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
            _flush_all_metrics(train_metrics_dir, metric_values_dict)
    # Optimizer step for the last batch
    if len(train_dataset) % batch_size_effective != 0:
        optimizer.step()
        optimizer.zero_grad()
    # Flush metrics for last batch.
    if len(train_dataset) % n_flush_metrics != 0:
        _flush_all_metrics(train_metrics_dir, metric_values_dict)
