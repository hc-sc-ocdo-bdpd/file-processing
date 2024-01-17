from unittest.mock import patch
from errors import FileProcessingFailedError
from file_processing.directory2 import Directory
import sys
import os
import pandas as pd
import pytest
import json
sys.path.append(os.path.join(sys.path[0], 'file_processing'))

variable_names = "filters"
values = [
    ({"max_size": 50000}),
    ({"min_size": 50000}),
    ({"extensions": ['.csv'], "min_size": 50000}),
    ({})
]


@pytest.fixture
def mk_get_rm_dir(filters, tmp_path_factory):
    output_path = str(tmp_path_factory.mktemp("outputs") / "test_output.csv")
    dir1 = Directory('tests/resources/directory_test_files')
    dir1.generate_analytics(output_path, filters)
    data = pd.read_csv(output_path)
    yield data


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
    assert set(["Extension", "Size", "Count"]) == set(mk_get_rm_dir.columns)


invalid_location = [('non_existent_folder/test_output.csv')]


@pytest.mark.parametrize("output_path", invalid_location)
def test_output_location(output_path):
    dir1 = Directory('tests/resources/directory_test_files')
    with pytest.raises(FileNotFoundError):
        dir1.generate_analytics(output_path)
