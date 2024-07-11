import faiss
import numpy as np
from abc import ABC, abstractmethod

class FAISSStrategy(ABC):
    def __init__(self, embeddings: np.ndarray, k):
        self.DIMENSION = embeddings.shape[1]
        self.index = self._create_index(self)

    @abstractmethod
    def _create_index(self, embeddings: np.ndarray):
        pass

    def query(self, xq: np.ndarray, k: int):
        return self.index.search(xq, k)
