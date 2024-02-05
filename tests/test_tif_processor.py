import pytest
import sys, os
sys.path.append(os.path.join(sys.path[0],'file_processing'))
from file_processing.file import File
from unittest.mock import patch
from file_processing.errors import FileProcessingFailedError

variable_names = "path, original_format, mode, width, height"
values = [
   ('tests/resources/test_files/CanadaLogo.tif', 'TIFF', 'RGB', 215, 74),
   ('tests/resources/test_files/MSWordIcon.tiff', 'TIFF', 'RGBA', 79, 106)
]


@pytest.mark.parametrize(variable_names, values)
def test_tif_metadata(path, original_format, mode, width, height):
    file_obj = File(path)
    assert file_obj.metadata['original_format'] == original_format
    assert file_obj.metadata['mode'] == mode
    assert file_obj.metadata['width'] == width
    assert file_obj.metadata['height'] == height


@pytest.mark.parametrize(variable_names, values)
def test_save_tif_metadata(copy_file, original_format, mode, width, height):
    test_tif_metadata(copy_file, original_format, mode, width, height)


@pytest.mark.parametrize("path", map(lambda x: x[0], values))
def test_tif_invalid_save_location(path):
    tif_file = File(path)
    invalid_save_path = '/non_existent_folder/' + os.path.basename(path)
    with pytest.raises(FileProcessingFailedError):
        tif_file.processor.save(invalid_save_path)


@pytest.mark.parametrize("path", map(lambda x: x[0], values))
def test_not_opening_file(path):
    with patch('builtins.open', autospec=True) as mock_open:
        File(path, open_file=False)
        mock_open.assert_not_called()