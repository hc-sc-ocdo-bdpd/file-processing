import os
from unittest.mock import patch
import pytest
from file_processing import File
from file_processing.errors import FileProcessingFailedError
from file_processing_test_data import get_test_files_path

test_files_path = get_test_files_path()

variable_names = "path, text_length, num_lines, num_words"
values = [
    (test_files_path / 'government_of_canada_wikipedia.txt', 38983, 306, 5691),
    (test_files_path / 'usa_government_wikipedia.txt', 47819, 383, 7160)
]


@pytest.mark.parametrize(variable_names, values)
def test_txt_metadata(path, text_length, num_lines, num_words):
    file_obj = File(path)
    assert len(file_obj.metadata['text']) == text_length
    assert file_obj.metadata['num_lines'] == num_lines
    assert file_obj.metadata['num_words'] == num_words


@pytest.mark.parametrize(variable_names, values)
def test_not_opening_file(path, text_length, num_lines, num_words):
    with patch('builtins.open', autospec=True) as mock_open:
        File(path, open_file=False)
        mock_open.assert_not_called()


@pytest.mark.parametrize(variable_names, values)
def test_save_txt_metadata(copy_file, text_length, num_lines, num_words):
    test_txt_metadata(copy_file, text_length, num_lines, num_words)


@pytest.mark.parametrize("path", map(lambda x: x[0], values))
def test_txt_invalid_save_location(path):
    txt_file = File(path)
    invalid_save_path = '/non_existent_folder/' + os.path.basename(path)
    with pytest.raises(FileProcessingFailedError):
        txt_file.save(invalid_save_path)
