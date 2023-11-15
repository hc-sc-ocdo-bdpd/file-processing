import pytest
import sys, os
sys.path.append(os.path.join(sys.path[0],'file_processing'))
from file_processing.file import File
from unittest.mock import patch

variable_names = "path, text_length"
values = [
   ('tests/resources/test_files/Test_for_RTF.rtf', 5306)
]

@pytest.mark.parametrize(variable_names, values)
def test_rtf_metadata(path, text_length):
    file_obj = File(path)
    assert len(file_obj.metadata['text']) == text_length


@pytest.mark.parametrize(variable_names, values)
def test_save_rtf_metadata(copy_file, text_length):
    test_rtf_metadata(copy_file, text_length)

@pytest.mark.parametrize("path", map(lambda x: x[0], values))
def test_rtf_invalid_save_location(invalid_save_location):
    invalid_save_location
    pytest.fail("Test not yet implemented")


@pytest.mark.parametrize("path", map(lambda x: x[0], values))
def test_not_opening_file(path):
    with patch('builtins.open', autospec=True) as mock_open:
        File(path, open_file=False)
        mock_open.assert_not_called()


corrupted_files = [
    'tests/resources/test_files/Test_for_RTF_corrupted.rtf'
]

@pytest.mark.parametrize("path", corrupted_files)
def test_rtf_corrupted_file_processing(corrupted_file_processing):
    corrupted_file_processing
    pytest.fail("Test not yet implemented")
