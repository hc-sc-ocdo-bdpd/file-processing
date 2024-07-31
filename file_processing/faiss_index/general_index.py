import numpy as np
from file_processing.faiss_index.faiss_strategy import FAISSStrategy


class GeneralIndex(FAISSStrategy):
    def _create_index(self):
        raise NotImplementedError()

    def query(self, xq: np.ndarray, k: int = 1):
        return super().query()
