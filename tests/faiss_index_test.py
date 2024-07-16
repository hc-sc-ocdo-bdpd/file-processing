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
    (test_embeddings, "resources/faiss_test_files/flat.faiss"),
    (test_embeddings[:1,:], None)
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
    (test_embeddings, 10, "resources/faiss_test_files/ivf.faiss"),
    (test_embeddings, test_embeddings.shape[0], None),
    (test_embeddings, test_embeddings.shape[0] // 2, None),
    (test_embeddings[:1,:], None, None)
]
@pytest.mark.parametrize(create_ivf_variable_names, create_ivf_values)
def test_create_ivf_flat_index(embeddings, nlist, file_path):
    index = faiss_index.create_IVF_flat_index(embeddings, nlist, file_path)
    assert isinstance(index.index, faiss.swigfaiss.IndexIVFFlat)
    if nlist is not None:
        assert index.index.nlist == nlist

create_ivf_error_values = [
    (test_embeddings, test_embeddings.shape[0] + 1, None),
    (test_embeddings, -1, None),
    (test_embeddings, 2.5, None)
]
@pytest.mark.parametrize(create_ivf_variable_names, create_ivf_error_values)
def test_create_ivf_flat_index_hyperparameter_errors(embeddings, nlist, file_path):
    with pytest.raises(Exception):
        faiss_index.create_IVF_flat_index(embeddings, nlist, file_path)

create_hnsw_variable_names = "embeddings, M, efConstruction, file_path"
create_hnsw_values = [
    (test_embeddings, None, None, None),
    (test_embeddings, None, None, "resources/faiss_test_files/hnsw.faiss"),
    (test_embeddings, 32, None, None),
    (test_embeddings, None, 40, None),
    (test_embeddings, 128, 40, None),
    (test_embeddings, 128, 40, "resources/faiss_test_files/hnsw.faiss"),
    (test_embeddings[:1,:], None, None, None)
]
@pytest.mark.parametrize(create_hnsw_variable_names, create_hnsw_values)
def test_create_hnsw_index(embeddings, M, efConstruction, file_path):
    index = faiss_index.create_HNSW_index(embeddings, M, efConstruction, file_path)
    assert isinstance(index.index, faiss.swigfaiss.IndexHNSWFlat)

create_hnsw_error_values = [
    (test_embeddings, -1, None, None),
    (test_embeddings, -1, -1, None),
    (test_embeddings, None, -1, None),
    (test_embeddings, 5.5, 10, None),
    (test_embeddings, 5, 7.5, None),
    (test_embeddings, 2.5, 2.5, None),
    (test_embeddings, -1, 2.5, None)
]
@pytest.mark.parametrize(create_hnsw_variable_names, create_hnsw_error_values)
def test_create_hnsw_index_hyperparameter_errors(embeddings, M, efConstruction, file_path):
    with pytest.raises(Exception):
        faiss_index.create_HNSW_index(embeddings, M, efConstruction, file_path)
