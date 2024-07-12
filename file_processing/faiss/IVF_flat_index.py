import faiss
import numpy as np
from file_processing.faiss import faiss_strategy
from importlib import reload
reload(faiss_strategy)

class IVFFlatIndex(faiss_strategy.FAISSIndex):
    def __init__(self, embeddings: np.ndarray = None, nlist: int = None, file_path: str = None) -> None:
        super().__init__(embeddings, file_path)
        if embeddings is not None:
            if nlist is None:
                nlist = int(np.sqrt(embeddings.shape[0] / 2))
            quantizer = faiss.IndexFlatL2(self.dimension)
            index = faiss.IndexIVFFlat(quantizer, self.dimension, nlist)
            index.train(embeddings)
            index.add(embeddings)
            self.index = index

    def query(self, xq: np.ndarray, k: int = 1, nprobe: int = 1):
        self.index.nprobe = nprobe
        return self.index.search(xq, k)