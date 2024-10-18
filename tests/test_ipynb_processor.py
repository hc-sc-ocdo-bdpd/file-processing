import os
from unittest.mock import patch
import pytest
from file_processing import File
from file_processing.errors import FileProcessingFailedError
from file_processing_test_data import get_test_files_path

test_files_path = get_test_files_path()

variable_names = "path, text_length, num_cells, num_code_cells, num_markdown_cells"
values = [
    (test_files_path / 'convolutional_network_raw.ipynb', 5312, 7, 5, 2),
    (test_files_path / 'neural_network.ipynb', 4404, 11, 9, 2)
]

@pytest.mark.parametrize(variable_names, values)
def test_ipynb_metadata(path, text_length, num_cells, num_code_cells, num_markdown_cells):
    file_obj = File(path)
    assert len(file_obj.metadata['text']) == text_length
    assert file_obj.metadata['num_cells'] == num_cells
    assert file_obj.metadata['num_code_cells'] == num_code_cells
    assert file_obj.metadata['num_markdown_cells'] == num_markdown_cells

@pytest.mark.parametrize(variable_names, values)
def test_save_ipynb_metadata(copy_file, text_length, num_cells, num_code_cells, num_markdown_cells):
    test_ipynb_metadata(copy_file, text_length, num_cells, num_code_cells, num_markdown_cells)

@pytest.mark.parametrize("valid_path", [path for path, *_ in values])
def test_ipynb_invalid_save_location(valid_path):
    ipynb_file = File(valid_path)
    invalid_save_path = '/non_existent_folder/' + os.path.basename(valid_path)
    with pytest.raises(FileProcessingFailedError):
        ipynb_file.processor.save(invalid_save_path)

@pytest.mark.parametrize(variable_names, values)
def test_not_opening_file(path, text_length, num_cells, num_code_cells, num_markdown_cells):
    with patch('builtins.open', autospec=True) as mock_open:
        File(path, open_file=False)
        mock_open.assert_not_called()
