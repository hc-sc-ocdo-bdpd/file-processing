import os
from unittest.mock import patch
import pytest
from file_processing import File
from file_processing.errors import FileProcessingFailedError
from file_processing_test_data import get_test_files_path

test_files_path = get_test_files_path()

variable_names = "path, text_length, encoding, num_rows, num_cols, num_cells, empty_cells"
values = [
   (test_files_path / '2021_Census_English.csv', 6084302, 'ISO-8859-1', 36835, 23, 847205, 253932),
   (test_files_path / 'Approved_Schools_2023_10_01.csv', 1403268, 'UTF-8-SIG', 5385, 13, 70005, 73)
]


@pytest.mark.parametrize(variable_names, values)
def test_csv_metadata(path, text_length, encoding, num_rows, num_cols, num_cells, empty_cells):
    file_obj = File(path)
    assert len(file_obj.metadata['text']) == text_length
    assert file_obj.metadata['encoding'] == encoding
    assert file_obj.metadata['num_rows'] == num_rows
    assert file_obj.metadata['num_cols'] == num_cols
    assert file_obj.metadata['num_cells'] == num_cells
    assert file_obj.metadata['empty_cells'] == empty_cells


@pytest.mark.parametrize(variable_names, values)
def test_save_csv_metadata(copy_file, text_length, encoding, num_rows, num_cols, num_cells, empty_cells):
    test_csv_metadata(copy_file, text_length, encoding, num_rows, num_cols, num_cells, empty_cells)


@pytest.mark.parametrize("valid_path", [path for path, *_ in values])
def test_csv_invalid_save_location(valid_path):
    csv_file = File(valid_path)
    invalid_save_path = '/non_existent_folder/' + os.path.basename(valid_path)
    with pytest.raises(FileProcessingFailedError):
        csv_file.processor.save(invalid_save_path)


@pytest.mark.parametrize(variable_names, values)
def test_not_opening_file(path, text_length, encoding, num_rows, num_cols, num_cells, empty_cells):
    with patch('builtins.open', autospec=True) as mock_open:
        File(path, open_file=False)
        mock_open.assert_not_called()
