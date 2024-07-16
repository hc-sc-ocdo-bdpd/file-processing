import faiss
import numpy as np
from file_processing.faiss_index import faiss_strategy
from importlib import reload
reload(faiss_strategy)

class HNSWIndex(faiss_strategy.FAISSStrategy):
    def _create_index(self, embeddings: np.ndarray, M: int, efConstruction: int):
        dimension = embeddings.shape[1]
        index = faiss.IndexHNSWFlat(dimension, M)
        index.hnsw.efConstruction = efConstruction
        index.add(embeddings)
        return index

    def query(self, xq: np.ndarray, k: int = 1, efSearch: int = 128):
        self.index.hnsw.efSearch = efSearch
        return self.index.search(xq, k)