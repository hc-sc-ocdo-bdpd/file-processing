import faiss
import numpy as np
from file_processing.faiss.faiss_strategy import FAISSStrategy

class FlatIndex(FAISSStrategy):
    def __init__(self, embeddings: np.ndarray) -> None:
        super().__init__(embeddings)
        index = faiss.IndexFlatL2(self.dimension)
        index.add(embeddings)
        self.index = index

    def query(self, xq: np.ndarray, k: int = 1):
        return self.index.search(xq, k)