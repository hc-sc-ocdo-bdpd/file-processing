from unittest.mock import patch
from errors import FileProcessingFailedError
import sys
from file_processing.directory import Directory
import os
import pandas as pd
import pytest
import json
sys.path.append(os.path.join(sys.path[0],'file_processing'))

variable_names = "include_text, filters, keywords, migrate_filters"
values = [(True, None, None, {"extensions": ['.csv']}),
          (False, None, None, {"max_size": 50000}),
          (True, {}, None, {"min_size": 50000}),
          (True, {"extensions": ['.csv'], "min_size": 50000}, None, None),
          (False, {"extensions": ['.docx', '.pptx'], "max_size": 50000}, None, None),
          (True, None, [], None),
          (False, None, ['Canada'], None),
          (True, None, ['Canada', 'Health'], None)]


@pytest.fixture
def mk_get_rm_dir(include_text, filters, keywords, migrate_filters, tmp_path_factory):
    output_path = str(tmp_path_factory.mktemp("outputs") / "test_output.csv")
    dir1 = Directory('tests/resources/directory_test_files')
    dir1.generate_report(output_path, include_text, filters, keywords, migrate_filters)
    data = pd.read_csv(output_path)
    yield data


@pytest.mark.parametrize(variable_names, values)
def test_text(mk_get_rm_dir, include_text):
    assert mk_get_rm_dir['Metadata'].str.contains(
        "\"text\":").any() == include_text


@pytest.mark.parametrize(variable_names, values)
def test_filters(mk_get_rm_dir, filters):
    if filters:
        if "extensions" in filters.keys():
            assert mk_get_rm_dir["Extension"].str.contains(r'\b(?:{})\b'.format(
                "|".join(filters.get("extensions")))).count() == mk_get_rm_dir.shape[0]
        if "min_size" in filters.keys():
            assert (mk_get_rm_dir["Size"] >= filters.get("min_size")).all()
        if "max_size" in filters.keys():
            assert (mk_get_rm_dir["Size"] <= filters.get("max_size")).all()
    else:
        assert mk_get_rm_dir.shape[0] == sum(
            len(files) for _, _, files in os.walk(r'tests/resources/directory_test_files'))


@pytest.mark.parametrize(variable_names, values)
def test_columns(mk_get_rm_dir):
    assert set(["File Path", "File Name", "Extension", "Size", "Modification Time", "Access Time", "Creation Time", 
               "Parent Directory", "Is File?", "Is Symlink?", "Absolute Path", "Metadata"]).issubset(mk_get_rm_dir.columns)


@pytest.mark.parametrize(variable_names, values)
def test_migrate_filters(mk_get_rm_dir, migrate_filters):
    if migrate_filters:
        assert "Migrate?" in mk_get_rm_dir.columns, "The 'Migrate' column is missing from the DataFrame."

        if "extensions" in migrate_filters.keys():
            assert mk_get_rm_dir[mk_get_rm_dir["Extension"].isin(migrate_filters.get("extensions"))]["Migrate?"].eq(1).all()
            assert mk_get_rm_dir[~mk_get_rm_dir["Extension"].isin(migrate_filters.get("extensions"))]["Migrate?"].eq(0).all()
        if "min_size" in migrate_filters.keys():
            assert mk_get_rm_dir[mk_get_rm_dir["Size"] >= migrate_filters.get("min_size")]["Migrate?"].eq(1).all()
            assert mk_get_rm_dir[~mk_get_rm_dir["Size"] >= migrate_filters.get("min_size")]["Migrate?"].eq(0).all()
        if "max_size" in migrate_filters.keys():
            assert mk_get_rm_dir[mk_get_rm_dir["Size"] <= migrate_filters.get("min_size")]["Migrate?"].eq(1).all()
            assert mk_get_rm_dir[~mk_get_rm_dir["Size"] <= migrate_filters.get("min_size")]["Migrate?"].eq(0).all()
    else:
        assert "Migrate?" not in mk_get_rm_dir.columns, "The 'Keywords' column should not be present in the DataFrame."


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

        assert (metadata_keyword_counts == keyword_counts).all(
        ), "Keyword counts do not match."
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
            assert kwargs.get(
                'open_file') == False, "File was opened when it should not have been"


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
