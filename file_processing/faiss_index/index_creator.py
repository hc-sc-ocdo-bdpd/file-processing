import faiss
import numpy as np
from file_processing.faiss_index import flat_index
from file_processing.faiss_index import IVF_flat_index
from file_processing.faiss_index import HNSW_index
from file_processing.faiss_index import general_index


def load_index(file_path: str):
    """
    Load a FAISS index from a specified file path.

    Args:
        file_path (str): The path to the file containing the saved FAISS index.

    Returns:
        An instance of the corresponding index class.
    """
    INDEXES = {
        faiss.swigfaiss.IndexFlat: flat_index.FlatIndex,
        faiss.swigfaiss.IndexIVFFlat: IVF_flat_index.IVFFlatIndex,
        faiss.swigfaiss.IndexHNSWFlat: HNSW_index.HNSWIndex
    }
    index = faiss.read_index(file_path)
    if type(index) in INDEXES:
        index_class = INDEXES.get(type(index))
    else:
        index_class = general_index.GeneralIndex
    return index_class(index=index)


def create_flat_index(embeddings: np.ndarray, file_path: str = None):
    """
    Create a Flat Index using the provided embeddings.

    Args:
        embeddings (np.ndarray): An array of embeddings to index.
        file_path (str, optional): The path to save the index. If None, the index is not saved.

    Returns:
        FlatIndex: An instance of the FlatIndex containing the embeddings.
    """
    index = flat_index.FlatIndex(embeddings)
    if file_path is not None:
        index.save_index(file_path)
    return index


def create_IVF_flat_index(embeddings: np.ndarray, nlist: int = None,
                          file_path: str = None):
    """
    Create an IVF Flat Index using the provided embeddings and parameters.

    Args:
        embeddings (np.ndarray): An array of embeddings to index.
        nlist (int, optional): Number of clusters for the IVF index. If None, a default will be used.
        file_path (str, optional): The path to save the index. If None, the index is not saved.

    Returns:
        IVFFlatIndex: An instance of the IVFFlatIndex containing the embeddings.
    """
    index = IVF_flat_index.IVFFlatIndex(embeddings, nlist)
    if file_path is not None:
        index.save_index(file_path)
    return index


def create_HNSW_index(embeddings: np.ndarray, M: int = 64,
                      efConstruction: int = 64, file_path: str = None):
    """
    Create an HNSW Index using the provided embeddings and parameters.

    Args:
        embeddings (np.ndarray): An array of embeddings to index.
        M (int, optional): Number of bi-directional links created for each new element. Default is 64.
        efConstruction (int, optional): Size of the dynamic list for the nearest neighbors during construction. Default is 64.
        file_path (str, optional): The path to save the index. If None, the index is not saved.

    Returns:
        HNSWIndex: An instance of the HNSWIndex containing the embeddings.
    """
    index = HNSW_index.HNSWIndex(embeddings, M, efConstruction)
    if file_path is not None:
        index.save_index(file_path)
    return index
