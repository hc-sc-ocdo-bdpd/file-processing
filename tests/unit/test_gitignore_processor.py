import os
from unittest.mock import patch
import pytest
from file_processing import File
from file_processing.errors import FileProcessingFailedError
from file_processing_test_data import get_test_files_path

test_files_path = get_test_files_path()

# Define the variable names and values specific to .gitignore files
variable_names = "path, text_length, num_lines, num_words"
values = [
    (test_files_path / 'Python.gitignore', 3139, 163, 403),
    (test_files_path / 'tensorflow.gitignore', 939, 53, 52)
]

@pytest.mark.parametrize(variable_names, values)
def test_gitignore_metadata(path, text_length, num_lines, num_words):
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
def test_save_gitignore_metadata(copy_file, text_length, num_lines, num_words):
    test_gitignore_metadata(copy_file, text_length, num_lines, num_words)

@pytest.mark.parametrize("path", map(lambda x: x[0], values))
def test_gitignore_invalid_save_location(path):
    gitignore_file = File(path)
    invalid_save_path = '/non_existent_folder/' + os.path.basename(path)
    with pytest.raises(FileProcessingFailedError):
        gitignore_file.save(invalid_save_path)