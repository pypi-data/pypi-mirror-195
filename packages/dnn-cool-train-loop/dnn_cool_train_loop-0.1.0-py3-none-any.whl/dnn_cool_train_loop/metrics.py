from pathlib import Path
from typing import Dict, List, Union, Optional

import numpy as np
from mmap_ninja import numpy as np_ninja


def _flush_all_metrics(metrics_dir: Path, metric_values_dict: Dict[str, List[float]]):
    for k, v in metric_values_dict.items():
        task, metric, key = k
        _flush_datapoint(metrics_dir, task, metric, key, v)
        metric_values_dict[k] = []


def _store_datapoint(metric_values_dict: Dict, task: str, metric: str, idx: int, value: float):
    metric_values_dict[(task, metric, "idx")].append(idx)
    metric_values_dict[(task, metric, "value")].append(value)


def _flush_datapoint(metrics_dir: Path, task: str, metric: str, key: str, values: List[float]):
    out_dir = metrics_dir / task / metric
    out_dir.mkdir(exist_ok=True, parents=True)
    if not (out_dir / key).exists():
        np_ninja.from_ndarray(str(out_dir / key), np.asarray(values))
        return
    np_ninja.extend_dir(str(out_dir / key), np.asarray(values))


def load_metrics(
    metrics_dir: Union[str, Path],
    phase: Optional[str] = "*",
    epoch: Optional[int] = "*",
    task: Optional[str] = "*",
    metric: Optional[str] = "*",
    epoch_zfill=4,
) -> Dict[str, List]:
    metrics_dir = Path(metrics_dir)
    epoch = str(epoch).zfill(epoch_zfill)
    glob_expression = f"{phase}/{epoch}/{task}/{metric}/value"
    data = {"metric": [], "task": [], "epoch": [], "phase": [], "idx": [], "value": []}
    for value_mmap_file in metrics_dir.glob(glob_expression):
        print(f"Opening {value_mmap_file} ...")
        metric_comp = value_mmap_file.parts[-2]
        task_comp = value_mmap_file.parts[-3]
        epoch_comp = value_mmap_file.parts[-4]
        phase_comp = value_mmap_file.parts[-5]
        values = np_ninja.open_existing(value_mmap_file)
        idx_mmap_file = value_mmap_file.parent / "idx"
        indices = np_ninja.open_existing(idx_mmap_file)
        for idx, value in zip(indices, values):
            data["metric"].append(metric_comp)
            data["task"].append(task_comp)
            data["epoch"].append(epoch_comp)
            data["phase"].append(phase_comp)
            data["idx"].append(idx)
            data["value"].append(value)
    return data
