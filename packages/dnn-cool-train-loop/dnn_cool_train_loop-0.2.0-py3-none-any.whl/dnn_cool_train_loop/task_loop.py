from pathlib import Path
from typing import Dict, Callable, List, Optional

import torch
from torch import nn
from torch.types import Device

from dnn_cool_train_loop.metrics import _store_datapoint


def _task_loop(
    task: str,
    criterion_dict: Dict[str, Callable],
    labels_dict: Dict[str, torch.Tensor],
    output_dict: Dict[str, torch.Tensor],
    batch_size_effective: int,
    metrics_dir: Optional[Path],
    metrics_dict: Dict[str, Dict[str, Callable]],
    metric_values_dict: Dict[str, List[float]],
) -> torch.Tensor:
    labels = labels_dict[task]
    criterion = criterion_dict[task]
    idx = labels_dict["idx"].item()
    outputs = output_dict[task]
    loss = criterion(outputs, labels)
    loss = loss / batch_size_effective
    if metrics_dir is None:
        return loss
    _store_datapoint(metric_values_dict, task, "loss", idx, loss.item())
    if metrics_dict is None:
        return loss
    metrics_dict: Dict[str, Callable] = metrics_dict.get(task)
    if metrics_dict is None:
        return loss
    for metric_name, metric_fn in metrics_dict.items():
        value = metric_fn(outputs, labels)
        _store_datapoint(metric_values_dict, task, metric_name, idx, value)
    return loss


def _process_batch(
    model: nn.Module,
    batch_size_effective: int,
    criterion_dict: Dict[str, Callable],
    metrics_dir: Path,
    metrics_dict: Dict[str, Dict[str, Callable]],
    metric_values_dict: Dict[str, List[float]],
    data: Dict,
    device: Device,
):
    dct = {k: v.to(device) for k, v in data.items() if isinstance(v, torch.Tensor)}
    output_dict = model(dct)
    total_loss = None
    for task_list in data["tasks"]:
        loss = _task_loop(
            task=task_list[0],
            criterion_dict=criterion_dict,
            labels_dict=dct,
            output_dict=output_dict,
            batch_size_effective=batch_size_effective,
            metrics_dir=metrics_dir,
            metrics_dict=metrics_dict,
            metric_values_dict=metric_values_dict,
        )
        if total_loss is None:
            total_loss = loss
        else:
            total_loss += loss
    if metrics_dict is not None:
        _store_datapoint(metric_values_dict, "overall", "loss", data["idx"].item(), total_loss.item())
    return total_loss
