import pandas as pd
import pytest
from file_processing import Directory

variable_names = "filters, thresholds, top_n"
values = [
    ({}, 0, 0),
    ({}, 0, 0),
    ({}, 0, 0),
    ({}, 0, 0)
]


@pytest.fixture
def mk_get_rm_dir(filters, tmp_path_factory):
    output_path = str(tmp_path_factory.mktemp("outputs") / "test_output.csv")
    dir1 = Directory('tests/resources/directory_test_files')
    dir1.identify_duplicates(output_path, filters)
    data = pd.read_csv(output_path)
    yield data


def test_empty_report(tmp_path):
    dir1 = Directory('tests/resources/empty_dir')
    with pytest.raises(Exception):
        dir1.generate_report(tmp_path / "test_output.csv")

# Cosine similarity
# - columns
# - all data populated and in range [-1,1]
# Faiss indexes
# - columns
# - all data populated and in range [-1,1]