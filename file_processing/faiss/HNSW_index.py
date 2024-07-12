import faiss
import numpy as np
from file_processing.faiss import faiss_strategy
from importlib import reload
reload(faiss_strategy)

class FlatIndex(faiss_strategy.FAISSIndex):
    def __init__(self, embeddings: np.ndarray = None, M: int = 64, efConstruction: int = 64, file_path: str = None) -> None:
        super().__init__(embeddings, file_path)
        if embeddings is not None:
            index = faiss.IndexHNSW(self.dimension, M)
            index.hnsw.efConstruction = efConstruction
            index.add(embeddings)
            self.index = index

    def query(self, xq: np.ndarray, k: int = 1, efSearch: int = 128):
        self.index.hnsw.efSearch = efSearch
        return self.index.search(xq, k)