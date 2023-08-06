import torch

from torch.utils.data import Dataset


class DictStyle(Dataset):

    def __init__(self, tuple_dataset, input_name, target_name):
        self.tuple_dataset = tuple_dataset
        self.input_name = input_name
        self.target_name = target_name

    def __getitem__(self, item):
        x, y = self.tuple_dataset[item]
        return {
            self.input_name: torch.as_tensor(x),
            self.target_name: torch.as_tensor(y),
            'tasks': [self.target_name],
            'idx': item
        }

    def __len__(self):
        return len(self.tuple_dataset)
