from unittest.mock import patch
from file_processing.directory import Directory
import os
import pandas as pd
import pytest
import json

# TODO: Corrupted file
# TODO: Full test coverage

variable_names = "include_text, filters, keywords, migrate_filters, open_files, split_metadata"
values = [
    (False, None, None, None, True, False),
    (True, None, None, {"extensions": [".csv"]}, True, True),
    (False, None, None, {"max_size": 50000}, False, False),
    (True, {}, None, {"min_size": 50000}, True, True),
    (True, {"extensions": [".csv"], "include_str": ["directory_test_files"],
            "min_size": 50000}, None, None, True, False),
    (False, {"extensions": [".docx", ".pptx"], "exclude_str": ["0.1.2.3.4.5"],
             "max_size": 50000}, None, None, True, True),
    (True, {"exclude_extensions": [".csv", ".pptx"]}, [], None, True, False),
    (False, None, ["Canada"], None, True, True),
    (True, None, ["Canada", "Health"], None, True, False),]


@pytest.fixture
def mk_get_rm_dir(include_text, filters, keywords, migrate_filters, open_files, split_metadata, tmp_path_factory):
    output_path = str(tmp_path_factory.mktemp("outputs") / "test_output.csv")
    dir1 = Directory("tests/resources/directory_test_files")
    dir1.generate_report(output_path, include_text, filters,
                         keywords, migrate_filters, open_files, split_metadata)
    data = pd.read_csv(output_path)
    yield data


@pytest.mark.parametrize(variable_names, values)
def test_columns(mk_get_rm_dir, include_text, filters, keywords, open_files, split_metadata, migrate_filters):

    assert set(["File Path", "File Name", "Owner", "Extension", "Size (MB)", "Modification Time", "Access Time", "Creation Time",
                "Parent Directory", "Permissions", "Is File", "Is Symlink", "Absolute Path"]).issubset(mk_get_rm_dir.columns)

    if split_metadata and not open_files:
        assert "Message" in mk_get_rm_dir.columns
        assert "Metadata" not in mk_get_rm_dir
    elif split_metadata and open_files and not filters:
        assert set(["Encoding", "Num Rows", "Num Cols", "Num Cells", "Empty Cells", "Has Password", "Num Lines",
                    "Num Words", "Author", "Last Modified By", "Original Format", "Mode", "Width", "Height",
                    "Num Slides", "Subject", "Date", "Sender", "Active Sheet", "Sheet Names", "Creator", "Num Files",
                    "File Types", "File Names"]).issubset(mk_get_rm_dir.columns)
    elif not split_metadata:
        assert "Metadata" in mk_get_rm_dir.columns

    if include_text and split_metadata and not filters:
        assert set(["Text", "Lines", "Words"]).issubset(mk_get_rm_dir.columns)

    if include_text and keywords and not split_metadata:
        assert "Keywords" in mk_get_rm_dir.columns

    if migrate_filters:
        assert "Migrate" in mk_get_rm_dir.columns


@pytest.mark.parametrize(variable_names, values)
def test_text(mk_get_rm_dir, include_text, split_metadata):
    if include_text and not split_metadata:
        assert mk_get_rm_dir["Metadata"].str.contains(
            "\"text\":").any() == include_text


@pytest.mark.parametrize(variable_names, values)
def test_filters(mk_get_rm_dir, filters):
    if filters:
        if "extensions" in filters.keys() and filters['extensions']:
            assert mk_get_rm_dir["Extension"].str.contains(r"\b(?:{})\b".format(
                "|".join(filters.get("extensions")))).count() == mk_get_rm_dir.shape[0]
        if "exclude_extensions" in filters.keys() and filters['exclude_extensions']:
            assert not mk_get_rm_dir["Extension"].isin(
                filters.get("exclude_extensions")).any()
        if "min_size" in filters.keys():
            assert (mk_get_rm_dir["Size (MB)"] * 1e6 >= filters.get("min_size")).all()
        if "max_size" in filters.keys():
            assert (mk_get_rm_dir["Size (MB)"] * 1e6 <= filters.get("max_size")).all()
        if "exclude_str" in filters.keys():
            assert not mk_get_rm_dir["Absolute Path"].str.contains(
                "|".join(filters.get("exclude_str"))).any()
        if "include_str" in filters.keys():
            assert mk_get_rm_dir["Absolute Path"].str.contains(
                "|".join(filters.get("include_str"))).any()

    else:
        assert mk_get_rm_dir.shape[0] == sum(
            len(files) for _, _, files in os.walk(r"tests/resources/directory_test_files"))


@pytest.mark.parametrize(variable_names, values)
def test_migrate_filters(mk_get_rm_dir, migrate_filters):
    if migrate_filters:
        if "extensions" in migrate_filters.keys():
            assert mk_get_rm_dir[mk_get_rm_dir["Extension"].isin(
                migrate_filters.get("extensions"))]["Migrate"].eq(1).all()
            assert mk_get_rm_dir[~mk_get_rm_dir["Extension"].isin(
                migrate_filters.get("extensions"))]["Migrate"].eq(0).all()
        if "min_size" in migrate_filters.keys():
            assert mk_get_rm_dir[mk_get_rm_dir["Size (MB)"] >= migrate_filters["min_size"] / 1e6]["Migrate"].eq(1).all()
            assert mk_get_rm_dir[mk_get_rm_dir["Size (MB)"] < migrate_filters["min_size"] / 1e6]["Migrate"].eq(0).all()
        if "max_size" in migrate_filters.keys():
            assert mk_get_rm_dir[mk_get_rm_dir["Size (MB)"] <= migrate_filters["max_size"] / 1e6]["Migrate"].eq(1).all()
            assert mk_get_rm_dir[mk_get_rm_dir["Size (MB)"] > migrate_filters["max_size"] / 1e6]["Migrate"].eq(0).all()
    else:
        assert "Migrate" not in mk_get_rm_dir.columns, "The 'Keywords' column should not be present in the DataFrame."


@pytest.mark.parametrize(variable_names, values)
def test_keywords(mk_get_rm_dir, include_text, split_metadata, keywords):
    if keywords and include_text and not split_metadata:

        keyword_counts = (
            mk_get_rm_dir["Keywords"]
            .fillna('{}')
            .apply(lambda x: sum(json.loads(x.replace("'", '"')).values()))
        )

        metadata_keyword_counts = (
            mk_get_rm_dir["Metadata"]
            .apply(lambda x: json.loads(x).get('text', '') or '')
            .str.lower()
            .apply(lambda x: sum(x.count(key.lower()) for key in ['Health', 'Canada']))
        )

        assert (metadata_keyword_counts == keyword_counts).all(
        ), "Keyword counts do not match."
    else:
        assert "Keywords" not in mk_get_rm_dir.columns, "The 'Keywords' column should not be present in the DataFrame."


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
