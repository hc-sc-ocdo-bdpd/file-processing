import os
import pytest
import shutil
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

def test_load_chunks_with_name_issues(tmp_path):
    search = SearchDirectory(tmp_path)
    with pytest.raises(Exception):
        search.chunk_text("tests/resources/directory_test_files/2021_Census_English.csv")
    
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

def test_load_chunks_different_column_names(directory_with_chunks, tmp_path):
    search1 = SearchDirectory(tmp_path)
    search1.chunk_text("tests/resources/document_search_test_files/report_modified.csv",
                       "path",
                       "content")
    search2 = SearchDirectory(directory_with_chunks)
    assert search2.n_chunks == search1.n_chunks

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

variable_names = "start, end, batch, clean_files, expected_files, combined"
values = [
    (0, None, 100, False, ["0-76"], True),
    (0, None, 100, False, ['0-76'], True),
    (10, 40, 10, True, ['0-76'], True),
    (0, None, 20, True, ["0-20", '20-40', '40-60', '60-76'], True),
    (10, None, 30, False, ["10-40", "40-70", "70-76"], False),
    (15, 25, 5, True, ["10-40", "40-70", "70-76"], False),
    (20, 25, 1, True, ["20-21", '21-22', '22-23', '23-24', '24-25'], False),
    (25, 60, 20, False, ['25-45', '45-60'], False),
    (0, None, 15, True, ['0-15', '15-25', '25-45', '45-60', '60-75', '75-76'], True),
    (25, 60, 20, False, ['25-45', '45-60'], False),
    (0, 30, 20, False, ['0-20', '20-25', '25-45', '45-60'], False),
    (50, 100, 15, True, ['0-20', '20-25', '25-45', '45-60', '60-75', '75-76'], True),
    (0, 80, 40, True, ['0-40', '40-76'], True),
    (0, -1, 100, True, ['0-76'], True),
    (-4, -1, 2, True, ['73-75', '75-76'], False),
    (-77, -1, 100, True, ['0-76'], True),
    (-77, 76, 100, True, ['0-76'], True),
    (10, -2, 100, True, ['10-75'], False),
    (-78, None, 100, True, [], False),
    (0, 0, 100, True, [], False),
    (-1, None, 100, True, [], False),
    (76, 80, 100, True, [], False),
    (75, 80, 100, True, ['75-76'], False),
    (0, -77, 100, True, [], False)
]

@pytest.mark.parametrize(variable_names, values)
def test_embedding_creation(directory_with_embeding_module, start, end, batch, clean_files, expected_files, combined):
    search = SearchDirectory(directory_with_embeding_module)
    try:
        if len(expected_files) == 0:
            with pytest.raises(Exception):
                search.embed_text(start, end, batch)
        else:
            search.embed_text(start, end, batch)
        for file in expected_files:
            assert f"embeddings ({file}).npy" in os.listdir(directory_with_embeding_module / "embedding_batches")
        assert os.path.exists(directory_with_embeding_module / "embeddings.npy") == combined
    finally:
        # remove created files
        if clean_files:
            shutil.rmtree(directory_with_embeding_module / "embedding_batches")
            if os.path.exists(directory_with_embeding_module / "embeddings.npy"):
                os.remove(directory_with_embeding_module / "embeddings.npy")
