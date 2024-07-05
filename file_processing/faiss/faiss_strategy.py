import faiss
import numpy as np
from abc import ABC, abstractmethod

class FAISSStrategy(ABC):
    def __init__(self, vectors: np.ndarray):
        self.DIMENSION = vectors.shape[1]

    @abstractmethod
    def query(self, xq: np.ndarray):
        pass
