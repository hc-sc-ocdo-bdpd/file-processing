from datetime import datetime
from pathlib import Path
import pandas as pd
import pytest
from file_processing import Directory

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
def test_columns(mk_get_rm_dir):
    assert set(["extension", "size (MB)", "count"]
               ) == set(mk_get_rm_dir.columns)


def test_empty_report(tmp_path):
    dir1 = Directory('tests/resources/empty_dir')
    with pytest.raises(Exception):
        dir1.generate_report(tmp_path / "test_output.csv")


variable_names = "directory_path"
directories = [
    'tests/resources/directory_test_files',
    'tests/resources',
    'file_processing'
]


@pytest.mark.parametrize(variable_names, directories)
def test_not_opening_files_in_directory(directory_path, tmp_path):
    output_path = tmp_path / "test_output.csv"
    dir1 = Directory(directory_path)
    dir1.generate_report(str(output_path), open_files=False)

    data = pd.read_csv(str(output_path))
    now = datetime.now().timestamp()
    data = data[~data['Extension'].isin(['.py', '.pyc'])]
    data = data.reset_index(drop=True)
    file_names = data['Absolute Path']

    for file_name in file_names:
        unix = Path(str(file_name)).stat().st_atime
        assert now > unix, f"File was opened when it should not have been ({file_name})"
