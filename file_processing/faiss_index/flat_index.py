import faiss
import numpy as np
from file_processing.faiss_index.faiss_strategy import FAISSStrategy


class FlatIndex(FAISSStrategy):
    def _create_index(self, embeddings: np.ndarray):
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings)
        return index

    def query(self, xq: np.ndarray, k: int = 1):
        return super().query(xq, k)
