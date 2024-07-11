import numpy as np
from abc import ABC, abstractmethod

class FAISSStrategy(ABC):
    def __init__(self, embeddings: np.ndarray) -> None:
        self.dimension = embeddings.shape[1]
        self.index = None

    @abstractmethod
    def query(self):
        pass
