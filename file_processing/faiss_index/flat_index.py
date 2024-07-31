import faiss
import numpy as np
from file_processing.faiss_index.faiss_strategy import FAISSStrategy


class FlatIndex(FAISSStrategy):
    def _create_index(self, embeddings: np.ndarray, metric: int):
        dimension = embeddings.shape[1]
        index = faiss.IndexFlat(dimension, metric)
        index.add(embeddings)
        return index

    def query(self, xq: np.ndarray, k: int = 1):
        return super().query(xq, k)
