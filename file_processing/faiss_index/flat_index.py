import faiss
import numpy as np
from file_processing.faiss_index import faiss_strategy
from file_processing.tools.errors import UnsupportedHyperparameterError


class FlatIndex(faiss_strategy.FAISSStrategy):
    def _create_index(self, embeddings: np.ndarray):
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings)
        return index

    def query(self, xq: np.ndarray, k: int = 1):
        if k < 1:
            raise UnsupportedHyperparameterError("k cannot be less than 1")
        return self.index.search(xq, k)
