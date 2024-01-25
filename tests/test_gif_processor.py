import pytest
import os
from file_processing.file import File
from unittest.mock import patch
from file_processing.errors import FileProcessingFailedError

variable_names = "path, original_format, mode, width, height, animated, frames"
values = [
   ('tests/resources/test_files/MapleLeaf.gif', 'GIF', 'P', 480, 480, True, 27),
   ('tests/resources/test_files/MSEdgeIcon.gif', 'GIF', 'P', 79, 100, False, 1)
]


@pytest.mark.parametrize(variable_names, values)
def test_gif_metadata(path, original_format, mode, width, height, animated, frames):
    file_obj = File(path)
    assert file_obj.metadata['original_format'] == original_format
    assert file_obj.metadata['mode'] == mode
    assert file_obj.metadata['width'] == width
    assert file_obj.metadata['height'] == height
    assert bool(file_obj.metadata['animated']) == animated
    assert file_obj.metadata['frames'] == frames


@pytest.mark.parametrize(variable_names, values)
def test_save_gif_metadata(copy_file, original_format, mode, width, height, animated, frames):
    test_gif_metadata(copy_file, original_format, mode, width, height, animated, frames)


@pytest.mark.parametrize("path", map(lambda x: x[0], values))
def test_gif_invalid_save_location(path):
    gif_file = File(path)
    invalid_save_path = '/non_existent_folder/' + os.path.basename(path)
    with pytest.raises(FileProcessingFailedError):
        gif_file.processor.save(invalid_save_path)


@pytest.mark.parametrize("path", map(lambda x: x[0], values))
def test_not_opening_file(path):
    with patch('builtins.open', autospec=True) as mock_open:
        File(path, open_file=False)
        mock_open.assert_not_called()