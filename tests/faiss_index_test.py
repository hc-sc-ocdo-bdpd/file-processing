import os
import pytest
import faiss
import numpy as np
from file_processing import faiss_index

test_embeddings = np.load("tests/resources/faiss_test_files/sample_embeddings.npy")
query_vec = np.load("tests/resources/faiss_test_files/sample_query_vector.npy")


create_flat_variable_names = "embeddings, file_path"
create_flat_values = [
    (test_embeddings, None),
    (test_embeddings, "tests/resources/faiss_test_files/flat_index.faiss"),
    (test_embeddings[:1,:], None)
]
@pytest.mark.parametrize(create_flat_variable_names, create_flat_values)
def test_create_flat_index(embeddings, file_path):
    index = faiss_index.create_flat_index(embeddings, file_path)
    assert isinstance(index.index, faiss.IndexFlat)
    if file_path is not None:
        assert os.path.exists(file_path)
        os.remove(file_path)

query_flat_variable_names = "embeddings, xq, k"
query_flat_values = [
    (test_embeddings, query_vec, 0),
    (test_embeddings, query_vec, 3),
    (test_embeddings, query_vec, test_embeddings.shape[0]),
    (test_embeddings, query_vec, test_embeddings.shape[0] + 1)
]
@pytest.mark.parametrize(query_flat_variable_names, query_flat_values)
def test_flat_query(embeddings, xq, k):
    index = faiss_index.create_flat_index(embeddings)
    if k < 1:
        with pytest.raises(Exception):
            index.query(xq, k)
    else:
        D, I = index.query(xq, k)
        assert D.shape == I.shape
        assert D.shape[1] == k

create_ivf_variable_names = "embeddings, nlist, file_path"
create_ivf_values = [
    (test_embeddings, None, None),
    (test_embeddings, None, "tests/resources/faiss_test_files/ivf_index.faiss"),
    (test_embeddings, 1, None),
    (test_embeddings, 2, None),
    (test_embeddings, 10, "tests/resources/faiss_test_files/ivf_index.faiss"),
    (test_embeddings, test_embeddings.shape[0], None),
    (test_embeddings, test_embeddings.shape[0] // 2, None),
    (test_embeddings[:1,:], None, None)
]
@pytest.mark.parametrize(create_ivf_variable_names, create_ivf_values)
def test_create_ivf_flat_index(embeddings, nlist, file_path):
    index = faiss_index.create_IVF_flat_index(embeddings, nlist, file_path)
    assert isinstance(index.index, faiss.IndexIVFFlat)
    if nlist is not None:
        assert index.index.nlist == nlist
    if file_path is not None:
        assert os.path.exists(file_path)
        os.remove(file_path)

create_ivf_error_values = [
    (test_embeddings, test_embeddings.shape[0] + 1, None),
    (test_embeddings, -1, None),
    (test_embeddings, 2.5, None)
]
@pytest.mark.parametrize(create_ivf_variable_names, create_ivf_error_values)
def test_create_ivf_flat_index_hyperparameter_errors(embeddings, nlist, file_path):
    with pytest.raises(Exception):
        faiss_index.create_IVF_flat_index(embeddings, nlist, file_path)

query_ivf_variable_names = "embeddings, nlist, xq, k, nprobe"
query_ivf_values = [
    (test_embeddings, 5, query_vec, 0, None),
    (test_embeddings, 5, query_vec, 3, None),
    (test_embeddings, 5, query_vec, test_embeddings.shape[0], None),
    (test_embeddings, 5, query_vec, test_embeddings.shape[0] + 1, None),
    (test_embeddings, 5, query_vec, 1, 0),
    (test_embeddings, 3, query_vec, 1, 4),
    (test_embeddings, 3, query_vec, 2, 1),
    (test_embeddings, 3, query_vec, 5, 1),
    (test_embeddings, 3, query_vec, 1, 5),
    (test_embeddings, 3, query_vec, 4, 5),
    (test_embeddings, 3, query_vec, 5, 4),
    (test_embeddings, 1, query_vec, 3, 1),
    (test_embeddings, 3, query_vec, 3, 3),
    (test_embeddings, test_embeddings.shape[0], query_vec, 3, test_embeddings.shape[0])
]
@pytest.mark.parametrize(query_ivf_variable_names, query_ivf_values)
def test_ivf_query(embeddings, nlist, xq, k, nprobe):
    index = faiss_index.create_IVF_flat_index(embeddings, nlist)
    if k < 1:
        with pytest.raises(Exception):
            index.query(xq, k, nprobe)
    elif (nprobe is not None) and (nprobe not in range(1, nlist + 1)):
        with pytest.raises(Exception):
            index.query(xq, k, nprobe)
    else:
        D, I = index.query(xq, k, nprobe)
        assert D.shape == I.shape
        assert D.shape[1] == k
        # check against the flat index
        if nlist == nprobe:
            flat = faiss_index.create_flat_index(embeddings)
            Df, If = flat.query(query_vec, k)
            assert np.array_equal(D, Df)
            assert np.array_equal(I, If)

create_hnsw_variable_names = "embeddings, M, efConstruction, file_path"
create_hnsw_values = [
    (test_embeddings, None, None, None),
    (test_embeddings, None, None, "tests/resources/faiss_test_files/hnsw_index.faiss"),
    (test_embeddings, 32, None, None),
    (test_embeddings, None, 40, None),
    (test_embeddings, 128, 40, None),
    (test_embeddings, 128, 40, "tests/resources/faiss_test_files/hnsw_index.faiss"),
    (test_embeddings[:1,:], None, None, None)
]
@pytest.mark.parametrize(create_hnsw_variable_names, create_hnsw_values)
def test_create_hnsw_index(embeddings, M, efConstruction, file_path):
    index = faiss_index.create_HNSW_index(embeddings, M, efConstruction, file_path)
    assert isinstance(index.index, faiss.IndexHNSWFlat)
    if file_path is not None:
        assert os.path.exists(file_path)
        os.remove(file_path)

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

query_hnsw_variable_names = "embeddings, M, efConstruction, xq, k, efSearch"
query_hnsw_values = [
    (test_embeddings, 32, 32, query_vec, 0, None),
    (test_embeddings, 32, 32, query_vec, 3, None),
    (test_embeddings, 32, 32, query_vec, test_embeddings.shape[0], None),
    (test_embeddings, 32, 32, query_vec, test_embeddings.shape[0] + 1, None),
    (test_embeddings, 32, 32, query_vec, 1, 0),
    (test_embeddings, 32, 32, query_vec, 1, 16),
    (test_embeddings, 32, 32, query_vec, 2, 1),
    (test_embeddings, 32, 32, query_vec, 3, 64)
]
@pytest.mark.parametrize(query_hnsw_variable_names, query_hnsw_values)
def test_hnsw_query(embeddings, M, efConstruction, xq, k, efSearch):
    index = faiss_index.create_HNSW_index(embeddings, M, efConstruction)
    if k < 1:
        with pytest.raises(Exception):
            index.query(xq, k, efSearch)
    elif (efSearch is not None) and (efSearch < 1):
        with pytest.raises(Exception):
            index.query(xq, k, efSearch)
    else:
        D, I = index.query(xq, k, efSearch)
        assert D.shape == I.shape
        assert D.shape[1] == k

load_index_variable_names = "file_path, index_type"
load_index_values = [
    ("tests/resources/faiss_test_files/flat.faiss", faiss_index.flat_index.FlatIndex),
    ("tests/resources/faiss_test_files/ivf.faiss", faiss_index.IVF_flat_index.IVFFlatIndex),
    ("tests/resources/faiss_test_files/hnsw.faiss", faiss_index.HNSW_index.HNSWIndex),
    ("tests/resources/faiss_test_files/ivfpq.faiss", faiss_index.general_index.GeneralIndex)
]
@pytest.mark.parametrize(load_index_variable_names, load_index_values)
def test_load_index(file_path, index_type):
    index = faiss_index.load_index(file_path)
    assert isinstance(index, index_type)
