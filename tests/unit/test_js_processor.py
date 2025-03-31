import os
import pytest
from unittest.mock import patch
from file_processing.file import File
from file_processing.errors import FileProcessingFailedError
from file_processing_test_data import get_test_files_path

test_files_path = get_test_files_path()

# JavaScript test file metadata expectations:
# (file_name, encoding, num_lines, num_functions, num_classes, num_comments)
values = [
    ('jest-cli.js', 'ascii', 401, 8, 0, 26),
    ('swipe.js', 'ascii', 146, 0, 1, 7),
    ('tab.js', 'ascii', 315, 0, 1, 23),
    ('Fibers.js', 'utf-8', 407, 6, 0, 3),
]

@pytest.mark.parametrize(
    "file_name, encoding, num_lines, num_functions, num_classes, num_comments",
    values
)
def test_js_metadata_extraction(file_name, encoding, num_lines, num_functions, num_classes, num_comments):
    """Tests JavaScript file processing metadata extraction."""
    js_file_path = test_files_path / file_name
    js_file = File(str(js_file_path))

    assert js_file.processor.metadata['encoding'] == encoding
    assert js_file.processor.metadata['num_lines'] == num_lines
    assert js_file.processor.metadata['num_functions'] == num_functions
    assert js_file.processor.metadata['num_classes'] == num_classes
    assert js_file.processor.metadata['num_comments'] == num_comments

@pytest.mark.parametrize("file_name", [entry[0] for entry in values])
def test_js_invalid_save_location(file_name):
    """Tests that saving to an invalid location raises an error."""
    js_file_path = test_files_path / file_name
    js_file = File(str(js_file_path))
    invalid_save_path = '/non_existent_folder/' + file_name
    with pytest.raises(FileProcessingFailedError):
        js_file.save(invalid_save_path)

@pytest.mark.parametrize("file_name", [entry[0] for entry in values])
def test_js_processor_open_file_false(file_name):
    """Tests that the file is not opened when open_file=False."""
    js_file_path = test_files_path / file_name
    with patch("builtins.open") as mock_open:
        File(str(js_file_path), open_file=False)
        mock_open.assert_not_called()