import os
import pytest
from unittest.mock import patch
from file_processing.file import File
from file_processing.errors import FileProcessingFailedError
from file_processing_test_data import get_test_files_path

test_files_path = get_test_files_path()

values = [
    ('active_record.rb', 'utf-8', 328, 17, 0, 3),
    ('tensorflow.rb', 'ascii', 99, 3, 1, 1),
    ('utils.rb', 'ascii', 186, 5, 0, 2),
    ('yandex.rb', 'utf-8', 292, 24, 1, 1),
]

@pytest.mark.parametrize(
    "file_name, encoding, num_lines, num_methods, num_classes, num_modules",
    values
)
def test_rb_metadata_extraction(file_name, encoding, num_lines, num_methods, num_classes, num_modules):
    rb_file_path = test_files_path / file_name
    rb_file = File(str(rb_file_path))

    assert rb_file.processor.metadata['encoding'] == encoding
    assert rb_file.processor.metadata['num_lines'] == num_lines
    assert rb_file.processor.metadata['num_methods'] == num_methods
    assert rb_file.processor.metadata['num_classes'] == num_classes
    assert rb_file.processor.metadata['num_modules'] == num_modules

@pytest.mark.parametrize("file_name", [name for name, *_ in values])
def test_rb_invalid_save_location(file_name):
    rb_file = File(str(test_files_path / file_name))
    invalid_save_path = '/non_existent_folder/' + file_name
    with pytest.raises(FileProcessingFailedError):
        rb_file.save(invalid_save_path)

@pytest.mark.parametrize("file_name", [name for name, *_ in values])
def test_rb_processor_open_file_false(file_name):
    rb_file_path = test_files_path / file_name
    with patch("builtins.open") as mock_open:
        File(str(rb_file_path), open_file=False)
        mock_open.assert_not_called()