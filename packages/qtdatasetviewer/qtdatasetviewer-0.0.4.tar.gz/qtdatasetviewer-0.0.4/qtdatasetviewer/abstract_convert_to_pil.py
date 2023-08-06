# ! python3
# -*- encoding: utf-8 -*-
# mypy: ignore-errors

from abc import ABC, abstractmethod

from PIL import Image
from torch.utils.data import Dataset


class AbstractConvertToPil(ABC):
    def __init__(self, dataloader: Dataset):
        self.dataloader = dataloader
        super().__init__()

    @abstractmethod
    def convert(self, item) -> Image:
        pass

    def get_dataloader(self) -> Dataset:
        return self.dataloader

    def get_size(self) -> int:
        return len(self.dataloader)
