import os
import pytest
import faiss
import numpy as np
from file_processing import faiss_index

test_embeddings = np.load("resources/faiss_test_files/sample_embeddings.npy")
query_vec = np.load("resources/faiss_test_files/sample_query_vector.npy")
flat_variable_names = "embeddings, file_path"
flat_values = [
    (test_embeddings, None),
    (test_embeddings, "reources/faiss_test_files/flat.faiss")
]

@pytest.mark.parametrize(flat_variable_names, flat_values)
def test_create_flat_index(embeddings, file_path):
    index = faiss_index.create_flat_index(test_embeddings, file_path)
    assert isinstance(index, faiss.swigfaiss.IndexIVFFlat)

