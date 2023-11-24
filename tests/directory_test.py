import sys, os
import pandas as pd
import pytest
import json
sys.path.append(os.path.join(sys.path[0],'file_processing'))
from file_processing.directory import Directory
from errors import FileProcessingFailedError
from unittest.mock import patch

variable_names = "include_text, filters, keywords"
values = [(True, None, None), 
          (False, None, None),
          (True, {}, None), 
          (True, {"extensions": '.csv', "min_size": 50000}, None), 
          (False, {"extensions": ['.docx', '.pptx'], "max_size": 50000}, None),
          (True, None, []), 
          (False, None, ['Canada']), 
          (True, None, ['Canada', 'Health'])]


@pytest.fixture
def mk_get_rm_dir(include_text, filters, keywords, tmp_path_factory):
    output_path = str(tmp_path_factory.mktemp("outputs") / "test_output.csv")
    dir1 = Directory('tests/resources/directory_test_files')
    dir1.generate_report(output_path, include_text, filters, keywords)
    data = pd.read_csv(output_path)
    yield data


@pytest.mark.parametrize(variable_names, values)
def test_text(mk_get_rm_dir, include_text):
    assert mk_get_rm_dir['Metadata'].str.contains("\"text\":").any() == include_text


@pytest.mark.parametrize(variable_names, values)
def test_filters(mk_get_rm_dir, filters):
    if filters:
        if "extensions" in filters.keys():
            assert mk_get_rm_dir["Extension"].str.contains(r'\b(?:{})\b'.format("|".join(filters.get("extensions")))).count() == mk_get_rm_dir.shape[0]
        if "min_size" in filters.keys():
            assert (mk_get_rm_dir["Size"] >= filters.get("min_size")).all()
        if "max_size" in filters.keys():
            assert (mk_get_rm_dir["Size"] <= filters.get("max_size")).all()
    else:
        assert mk_get_rm_dir.shape[0] == sum(len(files) for _, _, files in os.walk(r'tests/resources/directory_test_files'))


@pytest.mark.parametrize(variable_names, values)
def test_keywords(mk_get_rm_dir, keywords):
    if keywords:
        assert "Keywords" in mk_get_rm_dir.columns, "The 'Keywords' column is missing from the DataFrame."
        
        keyword_counts = (
            mk_get_rm_dir["Keywords"]
            .fillna('{}')
            .apply(lambda x: sum(json.loads(x).values()))
        )
        
        metadata_keyword_counts = (
            mk_get_rm_dir["Metadata"]
            .apply(lambda x: json.loads(x).get('text', '') or '')
            .str.lower()
            .apply(lambda x: sum(x.count(key.lower()) for key in keywords))
        )
        
        assert (metadata_keyword_counts == keyword_counts).all(), "Keyword counts do not match."
    else:
        assert "Keywords" not in mk_get_rm_dir.columns, "The 'Keywords' column should not be present in the DataFrame."


invalid_location = [('non_existent_folder/test_output.csv')]
@pytest.mark.parametrize("output_path", invalid_location)
def test_output_location(output_path):
    dir1 = Directory('tests/resources/directory_test_files')
    with pytest.raises(FileNotFoundError):
        dir1.generate_report(output_path)


corrupted_dir = [('tests/resources/directory_test_files_corrupted')]
@pytest.mark.parametrize("path", corrupted_dir)
def test_corrupted_dir(path):
    dir1 = Directory(path)
    with pytest.raises(FileProcessingFailedError):
        dir1.generate_report("test_output.csv")



variable_names = "directory_path"
directories = [
    'tests/resources/directory_test_files',
    'tests/resources',
    'file_processing'
]
@pytest.mark.parametrize(variable_names, directories)
def test_not_opening_files_in_directory(directory_path, tmp_path):
    output_path = tmp_path / "test_output.csv"
    with patch('file_processing.file.File', autospec=True) as mock_file:
        dir1 = Directory(directory_path)
        dir1.generate_report(str(output_path), open_files=False)
        for call in mock_file.mock_calls:
            args, kwargs = call[1], call[2]
            assert kwargs.get('open_file') == False, "File was opened when it should not have been"


@pytest.mark.parametrize(variable_names, directories)
def test_metadata_when_not_opening_files(directory_path, tmp_path):
    output_path = tmp_path / "test_output.csv"
    dir1 = Directory(directory_path)
    dir1.generate_report(str(output_path), open_files=False)
    
    data = pd.read_csv(str(output_path))
    for metadata_str in data['Metadata']:
        metadata = json.loads(metadata_str)
        assert len(metadata) == 1, "There should be only one key in the metadata"
        assert 'message' in metadata, "'message' key should be present in the metadata"
        assert "File was not opened" in metadata['message'], "'File was not opened' should be part of the message"