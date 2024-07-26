import faiss
import numpy as np
from file_processing.tools.errors import UnsupportedHyperparameterError
from abc import ABC, abstractmethod


class FAISSStrategy(ABC):
    METRICS = {
        "L2": 1,
        "IP": 0,
    }

    def __init__(self, *args, metric: str, index=None):
        if index is not None:
            self.index = index
        else:
            self.index = self._create_index(*args, self.METRICS[metric])

    def save_index(self, output_path: str):
        faiss.write_index(self.index, output_path)

    @abstractmethod
    def _create_index(self):
        pass

    @abstractmethod
    def query(self, xq: np.ndarray, k: int):
        if k < 1:
            raise UnsupportedHyperparameterError("k cannot be less than 1")
        return self.index.search(xq, k)
