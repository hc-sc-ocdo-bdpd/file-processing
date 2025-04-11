import os
import pytest
from unittest.mock import patch
from file_processing.file import File
from file_processing.errors import FileProcessingFailedError
from file_processing_test_data import get_test_files_path

test_files_path = get_test_files_path()

# (file_name, encoding, num_lines, num_includes, num_macros, num_structs, num_classes, num_comments)
values = [
    ('internal.h', 'ascii', 202, 5, 6, 4, 0, 23),
    ('rtp_av1.h', 'ascii', 132, 2, 19, 0, 0, 13),
    ('wglew.h', 'ascii', 958, 1, 356, 2, 0, 77),
    ('wglext.h', 'ascii', 696, 1, 235, 1, 0, 27),
]

@pytest.mark.parametrize(
    "file_name, encoding, num_lines, num_includes, num_macros, num_structs, num_classes, num_comments",
    values
)
def test_h_metadata_extraction(file_name, encoding, num_lines, num_includes,
                               num_macros, num_structs, num_classes, num_comments):
    """Tests .h file processing metadata extraction."""
    h_file_path = test_files_path / file_name
    h_file = File(str(h_file_path))

    metadata = h_file.processor.metadata
    assert metadata['encoding'] == encoding
    assert metadata['num_lines'] == num_lines
    assert metadata['num_includes'] == num_includes
    assert metadata['num_macros'] == num_macros
    assert metadata['num_structs'] == num_structs
    assert metadata['num_classes'] == num_classes
    assert metadata['num_comments'] == num_comments

@pytest.mark.parametrize("file_name", [entry[0] for entry in values])
def test_h_invalid_save_location(file_name):
    """Tests that saving to an invalid location raises an error."""
    h_file_path = test_files_path / file_name
    h_file = File(str(h_file_path))
    invalid_save_path = '/non_existent_folder/' + file_name
    with pytest.raises(FileProcessingFailedError):
        h_file.save(invalid_save_path)

@pytest.mark.parametrize("file_name", [entry[0] for entry in values])
def test_h_processor_open_file_false(file_name):
    """Tests that the file is not opened when open_file=False."""
    h_file_path = test_files_path / file_name
    with patch("builtins.open") as mock_open:
        File(str(h_file_path), open_file=False)
        mock_open.assert_not_called()