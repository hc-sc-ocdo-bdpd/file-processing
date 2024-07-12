import faiss
import numpy as np
from file_processing.faiss import faiss_strategy
from importlib import reload
reload(faiss_strategy)

class FlatIndex(faiss_strategy.FAISSIndex):
    def __init__(self, embeddings: np.ndarray = None, file_path: str = None) -> None:
        super().__init__(embeddings, file_path)
        if embeddings is not None:
            index = faiss.IndexFlatL2(self.dimension)
            index.add(embeddings)
            self.index = index

    def query(self, xq: np.ndarray, k: int = 1):
        return self.index.search(xq, k)