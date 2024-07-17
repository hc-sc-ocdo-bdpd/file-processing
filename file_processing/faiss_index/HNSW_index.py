import faiss
import numpy as np
from file_processing.faiss_index import faiss_strategy
from file_processing.tools.errors import UnsupportedHyperparameterError


class HNSWIndex(faiss_strategy.FAISSStrategy):
    def _create_index(self, embeddings: np.ndarray, M: int,
                      efConstruction: int):
        if M is None:
            M = 64
        if efConstruction is None:
            efConstruction = 64
        if not isinstance(M, int):
            raise TypeError("M must be an int type")
        if not isinstance(efConstruction, int):
            raise TypeError("efConstruction must be an int type")
        if M < 1:
            raise UnsupportedHyperparameterError(
                "M cannot be less than 1")
        if efConstruction < 1:
            raise UnsupportedHyperparameterError(
                "efConstruction cannot be less than 1")
        dimension = embeddings.shape[1]
        index = faiss.IndexHNSWFlat(dimension, M)
        index.hnsw.efConstruction = efConstruction
        index.add(embeddings)
        return index

    def query(self, xq: np.ndarray, k: int = 1, efSearch: int = None):
        if k < 1:
            raise UnsupportedHyperparameterError("k cannot be less than 1")
        if efSearch is not None:
            if efSearch < 1:
                raise UnsupportedHyperparameterError(
                    "efSearch cannot be less than 1")
            self.index.hnsw.efSearch = efSearch
        return self.index.search(xq, k)
