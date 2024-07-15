import faiss
from abc import ABC, abstractmethod

class FAISSStrategy(ABC):
    def __init__(self, *args, index = None):
        if index is not None:
            self.index = index
        else:
            self.index = self._create_index(*args)

    def save_index(self, output_path: str):
        faiss.write_index(self.index, output_path)

    @abstractmethod
    def _create_index(self):
        pass

    @abstractmethod
    def query(self):
        pass
