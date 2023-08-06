# dnn_cool_train_loop

Here, you can find a full list of the things you can do with `dnn_cool_train_loop`.
`dnn_cool_train_loop` is a microlib, which allows you to train multi-task neural networks.
The train/valid loop is done by predicting always with batch size equal to 1, and using gradient accumulation to 
simulate the effective batch size. 
This means that custom collator is not needed, even for inputs of different shapes, but training is a little slower.
The dataset should be a `dict`-based dataset, which has two additional keys: `idx` (the index in the global dataset)
and `tasks` - the targets, for which a backward pass should be done.

## Contents

Main API

1. [Train for one epoch](#train-for-one-epoch)
2. [Validate for one epoch](#validate-for-one-epoch)
3. [Full training loop](#full-training-loop)

### Train for one epoch

To train for one epoch, use the `train_for_one_epoch` function.
For example:


```python
from dnn_cool_train_loop.train_loop import train_for_one_epoch

train_for_one_epoch(
    epoch=0,
    model=model,
    train_dataset=train_dataset,
    criterion_dict=criterion_dict,
    batch_size_effective=batch_size_effective,
    metrics_dir=metrics_dir,
    metrics_dict=metrics_dict,
    lr=lr,
)
```

### Validate for one epoch

To validate for one epoch, use the `train_for_one_epoch` function.
For example:

```python
from dnn_cool_train_loop.valid_loop import validate_for_one_epoch

validate_for_one_epoch(
    epoch=0,
    model=model,
    valid_dataset=valid_dataset,
    criterion_dict=criterion_dict,
    batch_size_effective=batch_size_effective,
    metrics_dir=metrics_dir,
    metrics_dict=metrics_dict,
)
```


### Full training loop

To run a full training loop, you may just use the `train_for_one_epoch` and `validate_for_one_epoch`
functions with `functools.partial` and iterate over epochs.
An example would be:

```python
train_fn = partial(
    train_for_one_epoch,
    model=model,
    train_dataset=train_dataset,
    criterion_dict=criterion_dict,
    batch_size_effective=batch_size_effective,
    metrics_dir=metrics_dir,
    metrics_dict=metrics_dict,
    lr=lr,
)
valid_fn = partial(
    validate_for_one_epoch,
    model=model,
    valid_dataset=valid_dataset,
    criterion_dict=criterion_dict,
    batch_size_effective=batch_size_effective,
    metrics_dir=metrics_dir,
    metrics_dict=metrics_dict,
)
valid_fn("init")
for i in range(5):
    train_fn(i)
    valid_fn(i)

```