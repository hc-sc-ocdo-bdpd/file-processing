from unittest.mock import patch
import pytest
from file_processing import File
from file_processing.errors import FileProcessingFailedError
from file_processing_test_data import get_test_files_path

test_files_path = get_test_files_path()

# Define test parameters including path and expected metadata values
variable_names = "path, num_lines, num_functions, num_classes, num_imports, num_docstrings, text_length"
values = [
    (test_files_path / 'backend.py', 6503, 224, 5, 69, 194, 205761),  # Example length for 'backend.py' text content
    (test_files_path / 'align.py', 213, 8, 0, 16, 3, 6173)            # Example length for 'align.py' text content
]

@pytest.mark.parametrize(variable_names, values)
def test_python_metadata(path, num_lines, num_functions, num_classes, num_imports, num_docstrings, text_length):
    """
    Test that Python file metadata is accurately extracted, including line count, function count,
    class count, import count, docstring count, and total text length.
    """
    file_obj = File(path)
    assert file_obj.metadata['num_lines'] == num_lines
    assert file_obj.metadata['num_functions'] == num_functions
    assert file_obj.metadata['num_classes'] == num_classes
    assert len(file_obj.metadata['imports']) == num_imports
    assert len(file_obj.metadata['docstrings']) == num_docstrings
    assert len(file_obj.metadata['text']) == text_length  # Validate text content length

@pytest.mark.parametrize(variable_names, values)
def test_not_opening_file(path, num_lines, num_functions, num_classes, num_imports, num_docstrings, text_length):
    """
    Test that when open_file is set to False, the file is not opened and no metadata is extracted.
    """
    with patch('builtins.open', autospec=True) as mock_open:
        File(path, open_file=False)
        mock_open.assert_not_called()

@pytest.mark.parametrize(variable_names, values)
def test_save_python_metadata(copy_file, num_lines, num_functions, num_classes, num_imports, num_docstrings, text_length):
    """
    Test that Python metadata is saved correctly, preserving line count, function count,
    class count, import count, docstring count, and text content length.
    """
    test_python_metadata(copy_file, num_lines, num_functions, num_classes, num_imports, num_docstrings, text_length)

# Define test parameters for invalid save locations
invalid_save_locations_python = [
    (test_files_path / 'backend.py', '/non_existent_folder/backend.py')
]

@pytest.mark.parametrize("path, save_path", invalid_save_locations_python)
def test_py_invalid_save_location(path, save_path):
    """
    Test that attempting to save to an invalid location raises a FileProcessingFailedError.
    """
    file_obj = File(path)
    with pytest.raises(FileProcessingFailedError):
        file_obj.save(save_path)