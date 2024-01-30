import pandas as pd
import pytest
from file_processing.directory import Directory

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
    assert set(["extension", "size (MB)", "count"]) == set(mk_get_rm_dir.columns)
