import faiss
import numpy as np
from abc import ABC, abstractmethod

class FAISSIndex(ABC):
    def __init__(self, embeddings: np.ndarray = None, file_path: str = None) -> None:
        self.file_path = file_path
        if embeddings is None:
            self.read_index()
        else:
            self.dimension = embeddings.shape[1]
            self.index = None

    def save_index(self, output_path: str = None):
        if not output_path:
            output_path = self.file_path
        faiss.write_index(self.index, output_path)

    def read_index(self, input_path: str = None):
        if not input_path:
            input_path = self.file_path
        self.index = faiss.read_index(input_path)

    @abstractmethod
    def query(self):
        pass
