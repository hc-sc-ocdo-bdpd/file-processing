import os
import shutil
from pathlib import Path
from unittest.mock import patch
import pytest
from file_processing import File
from file_processing.errors import FileProcessingFailedError
from file_processing_test_data import get_test_files_path

test_files_path = get_test_files_path()

variable_names = "path, original_format, mode, width, height, animated, frames"
values = [
   (test_files_path / 'MapleLeaf.gif', 'GIF', 'P', 480, 480, True, 27),
   (test_files_path / 'MSEdgeIcon.gif', 'GIF', 'P', 79, 100, False, 1)
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


@pytest.mark.parametrize("path", [v[0] for v in values])
@pytest.mark.parametrize("algorithm", ["md5", "sha256"])
def test_gif_copy_with_integrity(path, algorithm, tmp_path):
    file_obj = File(path, open_file=False)
    original_hash = file_obj.processor.compute_hash(algorithm)

    dest_path = tmp_path / Path(path).name
    file_obj.copy(str(dest_path), verify_integrity=True)

    copied = File(str(dest_path))
    assert copied.processor.compute_hash(algorithm) == original_hash


@pytest.mark.parametrize("path", [v[0] for v in values])
def test_gif_copy_integrity_failure(path, tmp_path, monkeypatch):
    file_obj = File(path, open_file=False)

    def corrupt(src, dest, *, follow_symlinks=True):
        with open(dest, 'w') as f:
            f.write("CORRUPTED!")

    monkeypatch.setattr(shutil, "copy2", corrupt)

    with pytest.raises(FileProcessingFailedError) as excinfo:
        file_obj.copy(str(tmp_path / Path(path).name), verify_integrity=True)
    assert "Integrity check failed" in str(excinfo.value)
