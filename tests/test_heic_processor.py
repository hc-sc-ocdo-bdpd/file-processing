import os
from unittest.mock import patch
import pytest
from file_processing import File
from file_processing.errors import FileProcessingFailedError

variable_names = "path, original_format, mode, width, height"
values = [
    ('tests/resources/test_files/MapleLeaf.heic', 'HEIF', 'RGB', 1600, 1200),
    ('tests/resources/test_files/MapleLeaf.heif', 'HEIF', 'RGB', 1600, 1200)
]


@pytest.mark.parametrize(variable_names, values)
def test_heic_metadata(path, original_format, mode, width, height):
    file_obj = File(path)
    assert file_obj.metadata['original_format'] == original_format
    assert file_obj.metadata['mode'] == mode
    assert file_obj.metadata['width'] == width
    assert file_obj.metadata['height'] == height


@pytest.mark.parametrize(variable_names, values)
def test_save_heic_metadata(copy_file, original_format, mode, width, height):
    test_heic_metadata(copy_file, original_format, mode, width, height)


@pytest.mark.parametrize("path", map(lambda x: x[0], values))
def test_heic_invalid_save_location(path):
    heic_file = File(path)
    invalid_save_path = '/non_existent_folder/' + os.path.basename(path)
    with pytest.raises(FileProcessingFailedError):
        heic_file.processor.save(invalid_save_path)


@pytest.mark.parametrize("path", map(lambda x: x[0], values))
def test_not_opening_file(path):
    with patch('builtins.open', autospec=True) as mock_open:
        File(path, open_file=False)
        mock_open.assert_not_called()
