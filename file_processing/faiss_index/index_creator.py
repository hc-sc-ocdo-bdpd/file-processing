import faiss
import numpy as np
from file_processing.faiss_index import flat_index
from file_processing.faiss_index import IVF_flat_index
from file_processing.faiss_index import HNSW_index
from file_processing.faiss_index import general_index

def load_index(file_path: str):
    INDEXES = {
        faiss.swigfaiss.IndexFlat: flat_index.FlatIndex,
        faiss.swigfaiss.IndexIVFFlat: IVF_flat_index.IVFFlatIndex,
        faiss.swigfaiss.IndexHNSW: HNSW_index.HNSWFlatIndex
    }
    index = faiss.read_index(file_path)
    if type(index) in INDEXES:
        index_class = INDEXES.get(type(index))
    else:
        index_class = general_index.GeneralIndex
    return index_class(index=index)

def create_flat_index(embeddings: np.ndarray, file_path: str = None):
    index = flat_index.FlatIndex(embeddings)
    if file_path is not None:
        index.save_index(file_path)
    return index

def create_IVF_flat_index(embeddings: np.ndarray, nlist: int = None, file_path: str = None):
    index = IVF_flat_index.IVFFlatIndex(embeddings, nlist)
    if file_path is not None:
        index.save_index(file_path)
    return index
    
def create_HNSW_index(embeddings: np.ndarray, M: int = 64, efConstruction: int = 64, file_path: str = None):
    index = HNSW_index.HNSWIndex(embeddings, M, efConstruction)
    if file_path is not None:
        index.save_index(file_path)
    return index