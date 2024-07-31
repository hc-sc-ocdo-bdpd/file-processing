import os
import pytest
import pandas as pd
from file_processing import SearchDirectory

@pytest.fixture(scope="module")
def resource_folder():
    return "tests/resources/similarity_test_files"

@pytest.fixture(scope="module")
def embedding_model():
    return "paraphrase-MiniLM-L3-v2"

# Test chunking step

def test_empty_directory(tmp_path):
    SearchDirectory(tmp_path)
    assert not any(os.scandir(tmp_path))
    
def test_chunk_from_report(resource_folder, tmp_path):
    search = SearchDirectory(tmp_path)
    search.report_from_directory(resource_folder)
    assert os.path.exists(tmp_path / "report.csv")
    search.chunk_text()
    assert os.path.exists(tmp_path / "data_chunked.csv")
    assert os.path.exists(tmp_path / "setup_data.json")

def test_chunk_without_file(tmp_path):
    search = SearchDirectory(tmp_path)
    with pytest.raises(Exception):
        search.chunk_text()

def test_load_chunks_without_csv(tmp_path):
    search = SearchDirectory(tmp_path)
    with pytest.raises(Exception):
        search.chunk_text("tests/resources/directory_test_files/Test_excel_file.xlsx")

@pytest.fixture(scope="module")
def directory_with_chunks(resource_folder, tmp_path_factory):
    file_path = tmp_path_factory.mktemp("just_chunks")
    search = SearchDirectory(file_path)
    search.report_from_directory(resource_folder)
    search.chunk_text()
    return file_path

def test_load_with_chunks(directory_with_chunks):
    search = SearchDirectory(directory_with_chunks)
    assert search.n_chunks is not None

# Test load embedding step

def test_load_embedding_model(directory_with_chunks, embedding_model):
    search = SearchDirectory(directory_with_chunks)
    search.load_embedding_model(embedding_model)
    assert search.encoder is not None
    assert search.encoding_name == embedding_model

@pytest.fixture(scope="module")
def directory_with_embeding_module(resource_folder, tmp_path_factory, embedding_model):
    file_path = tmp_path_factory.mktemp("with_embedding_module")
    search = SearchDirectory(file_path)
    search.report_from_directory(resource_folder)
    search.chunk_text()
    search.load_embedding_model(embedding_model)
    return file_path

def test_load_after_model_defined(directory_with_embeding_module, embedding_model):
    search = SearchDirectory(directory_with_embeding_module)
    assert search.encoder is not None
    assert search.encoding_name == embedding_model

# Test embedding step
