import faiss
import numpy as np
from file_processing.faiss_index import faiss_strategy
from importlib import reload
reload(faiss_strategy)

class IVFFlatIndex(faiss_strategy.FAISSStrategy):
    def _create_index(self, embeddings: np.ndarray, nlist: int):
        dimension = embeddings.shape[1]
        if nlist is None:
            nlist = int(np.sqrt(embeddings.shape[0] / 2))
        quantizer = faiss.IndexFlatL2(dimension)
        index = faiss.IndexIVFFlat(quantizer, dimension, nlist)
        index.train(embeddings)
        index.add(embeddings)
        return index

    def query(self, xq: np.ndarray, k: int = 1, nprobe: int = 1):
        self.index.nprobe = nprobe
        return self.index.search(xq, k)