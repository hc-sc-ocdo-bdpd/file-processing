import os
import json
from datetime import datetime
from pathlib import Path
import pandas as pd
import pytest
from file_processing import Directory

dir_variable_names = "dir_path"
dir_values = [
    ('tests/resources/directory_test_files'),
    ('tests/resources'),
    ('file_processing')
]

@pytest.fixture
def mk_get_rm_dir_2(dir_path, tmp_path_factory):
    output_path = str(tmp_path_factory.mktemp("outputs") / "test_output.csv")
    dir1 = Directory(dir_path)
    dir1.generate_report(output_path, False, None, None, None, False, False)
    data = pd.read_csv(output_path)
    yield data


@pytest.mark.order(1)
@pytest.mark.parametrize(dir_variable_names, dir_values)
def test_not_opening_files_in_directory(mk_get_rm_dir_2):
    now = datetime.now().timestamp()
    data = mk_get_rm_dir_2[~mk_get_rm_dir_2['Extension'].isin(['.py', '.pyc'])]
    data = data.reset_index(drop=True)
    file_names = data['Absolute Path']

    for file_name in file_names:
        unix = Path(str(file_name)).stat().st_atime
        assert now > (unix + 1.5 * 60), f"File was opened when it should not have been ({file_name})"


@pytest.mark.parametrize(dir_variable_names, dir_values)
def test_metadata_when_not_opening_files(mk_get_rm_dir_2):
    for metadata_str in mk_get_rm_dir_2['Metadata']:
        metadata = json.loads(metadata_str)
        assert len(metadata) == 1, "There should be only one key in the metadata"
        assert 'message' in metadata, "'message' key should be present in the metadata"
        assert "File was not opened" in metadata['message'], "'File was not opened' should be part of the message"


variable_names = "include_text, filters, keywords, check_title_keywords, migrate_filters, open_files, split_metadata"
values = [
    (False, None, None, False, None, True, False),
    (True, None, None, False, {"extensions": [".csv"]}, True, True),
    (False, None, None, False, {"max_size": 50000}, False, False),
    (True, {}, None, False, {"min_size": 50000}, True, True),
    (True, {"extensions": [".csv"], "include_str": ["directory_test_files"], "min_size": 50000}, None, False, None, True, False),
    (False, {"extensions": [".docx", ".pptx"], "exclude_str": ["0.1.2.3.4.5"], "max_size": 50000}, None, False, None, True, True),
    (True, {"exclude_extensions": [".csv", ".pptx"]}, [], False, None, True, False),
    (False, None, ["Canada"], True, None, True, True),
    (True, None, ["Canada", "Health"], True, None, True, False),]


@pytest.fixture
def mk_get_rm_dir(include_text, filters, keywords, check_title_keywords, migrate_filters, open_files, split_metadata, tmp_path_factory):
    output_path = str(tmp_path_factory.mktemp("outputs") / "test_output.csv")
    dir1 = Directory("tests/resources/directory_test_files")
    dir1.generate_report(output_path, include_text, filters, keywords, check_title_keywords, migrate_filters, open_files, split_metadata)
    data = pd.read_csv(output_path)
    yield data


@pytest.mark.parametrize(variable_names, values)
def test_columns(mk_get_rm_dir, include_text, filters, keywords, check_title_keywords, open_files, split_metadata, migrate_filters):

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

    if include_text and keywords:
        if not split_metadata:
            assert "Keywords" in mk_get_rm_dir.columns
        elif split_metadata:
            assert sum(mk_get_rm_dir.columns.str.contains('Text.')) == len(keywords)

    if keywords and check_title_keywords:
        if not split_metadata:
            assert "Title Keywords" in mk_get_rm_dir.columns
        elif split_metadata:
            assert sum(mk_get_rm_dir.columns.str.contains('Title.')) == len(keywords)

    if migrate_filters:
        assert "Migrate" in mk_get_rm_dir.columns


@pytest.mark.parametrize(variable_names, values)
def test_text(mk_get_rm_dir, include_text, split_metadata):
    if include_text and not split_metadata:
        assert mk_get_rm_dir["Metadata"].str.contains("\"text\":").any() == include_text


@pytest.mark.parametrize(variable_names, values)
def test_filters(mk_get_rm_dir, filters):
    if filters:
        if "extensions" in filters.keys() and filters['extensions']:
            assert mk_get_rm_dir["Extension"].str.contains(r"\b(?:{})\b".format(
                "|".join(filters.get("extensions")))).count() == mk_get_rm_dir.shape[0]
        if "exclude_extensions" in filters.keys() and filters['exclude_extensions']:
            assert not mk_get_rm_dir["Extension"].isin(filters.get("exclude_extensions")).any()
        if "min_size" in filters.keys():
            assert (mk_get_rm_dir["Size (MB)"] * 1e6 >= filters.get("min_size")).all()
        if "max_size" in filters.keys():
            assert (mk_get_rm_dir["Size (MB)"] * 1e6 <= filters.get("max_size")).all()
        if "exclude_str" in filters.keys():
            assert not mk_get_rm_dir["Absolute Path"].str.contains("|".join(filters.get("exclude_str"))).any()
        if "include_str" in filters.keys():
            assert mk_get_rm_dir["Absolute Path"].str.contains("|".join(filters.get("include_str"))).any()

    else:
        num_files = sum(len(files) for _, _, files in os.walk(r"tests/resources/directory_test_files"))
        assert mk_get_rm_dir.shape[0] == num_files


@pytest.mark.parametrize(variable_names, values)
def test_migrate_filters(mk_get_rm_dir, migrate_filters):
    if migrate_filters:
        if "extensions" in migrate_filters.keys():
            assert mk_get_rm_dir[mk_get_rm_dir["Extension"].isin(migrate_filters.get("extensions"))]["Migrate"].eq(1).all()
            assert mk_get_rm_dir[~mk_get_rm_dir["Extension"].isin(migrate_filters.get("extensions"))]["Migrate"].eq(0).all()
        if "min_size" in migrate_filters.keys():
            assert mk_get_rm_dir[mk_get_rm_dir["Size (MB)"] >= migrate_filters["min_size"] / 1e6]["Migrate"].eq(1).all()
            assert mk_get_rm_dir[mk_get_rm_dir["Size (MB)"] < migrate_filters["min_size"] / 1e6]["Migrate"].eq(0).all()
        if "max_size" in migrate_filters.keys():
            assert mk_get_rm_dir[mk_get_rm_dir["Size (MB)"] <= migrate_filters["max_size"] / 1e6]["Migrate"].eq(1).all()
            assert mk_get_rm_dir[mk_get_rm_dir["Size (MB)"] > migrate_filters["max_size"] / 1e6]["Migrate"].eq(0).all()
    else:
        assert "Migrate" not in mk_get_rm_dir.columns, \
            "The 'Keywords' column should not be present in the DataFrame."


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

        assert (metadata_keyword_counts == keyword_counts).all(), \
            "Keyword counts do not match."
    else:
        assert "Keywords" not in mk_get_rm_dir.columns, \
            "The 'Keywords' column should not be present in the DataFrame."


@pytest.mark.parametrize(variable_names, values)
def test_title_keywords(mk_get_rm_dir, keywords, check_title_keywords, split_metadata):
    if keywords and check_title_keywords and not split_metadata:

        keyword_counts = (
            mk_get_rm_dir["Title Keywords"]
            .fillna('{}')
            .apply(lambda x: sum(json.loads(x.replace("'", '"')).values()))
        )

        metadata_keyword_counts = (
            mk_get_rm_dir["File Name"]
            .str.lower()
            .apply(lambda x: sum(x.count(key.lower()) for key in ['Health', 'Canada']))
        )

        assert (metadata_keyword_counts == keyword_counts).all(), \
            "Title keyword counts do not match."
    else:
        assert "Title Keywords" not in mk_get_rm_dir.columns, \
            "The 'Title Keywords' column should not be present in the DataFrame."


def test_corrupted_dir(tmp_path):
    temp_file = tmp_path / "test_output.csv"
    dir1 = Directory('tests/resources/directory_test_files_corrupted')
    dir1.generate_report(temp_file, split_metadata=True)
    data = pd.read_csv(temp_file)
    assert 'Error' in data
    assert (data['Error'] == 'FileProcessingFailedError').all()


def test_empty_report(tmp_path):
    dir1 = Directory('tests/resources/empty_dir')
    with pytest.raises(Exception):
        dir1.generate_report(tmp_path / "test_output.csv")
