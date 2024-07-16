import os
import pytest
import faiss
import numpy as np
from file_processing import faiss_index

test_embeddings = np.load("resources/faiss_test_files/sample_embeddings.npy")
query_vec = np.load("resources/faiss_test_files/sample_query_vector.npy")

create_flat_variable_names = "embeddings, file_path"
create_flat_values = [
    (test_embeddings, None),
    (test_embeddings, "resources/faiss_test_files/flat.faiss")
]
@pytest.mark.parametrize(create_flat_variable_names, create_flat_values)
def test_create_flat_index(embeddings, file_path):
    index = faiss_index.create_flat_index(embeddings, file_path)
    assert isinstance(index.index, faiss.swigfaiss.IndexFlat)

create_ivf_variable_names = "embeddings, nlist, file_path"
create_ivf_values = [
    (test_embeddings, None, None),
    (test_embeddings, None, "resources/faiss_test_files/ivf.faiss"),
    (test_embeddings, 1, None),
    (test_embeddings, 2, None),
    (test_embeddings, test_embeddings.shape[0], None),
    (test_embeddings, test_embeddings.shape[0] // 2, None)
    # (test_embeddings, test_embeddings.shape[0] + 1, None)
]

@pytest.mark.parametrize(create_ivf_variable_names, create_ivf_values)
def test_create_ivf_flat_index(embeddings, nlist, file_path):
    index = faiss_index.create_IVF_flat_index(embeddings, nlist, file_path)
    assert isinstance(index.index, faiss.swigfaiss.IndexIVFFlat)
    if nlist is not None:
        assert index.index.nlist == nlist