import os
import shutil
from unittest.mock import patch
from pathlib import Path
import pytest
from file_processing import File
from file_processing.errors import FileProcessingFailedError
from file_processing_test_data import get_test_files_path

test_files_path = get_test_files_path()

# Note: test_save_png_metadata tests both files for "original_format == 'PNG'
# when creating a copy, the original_format metadata for Health_Canada_logo.png
# becomes 'GIF' --> 'PNG'

variable_names = "path, original_format, mode, width, height"
values = [
    (test_files_path / 'Health_Canada_logo.png', 'GIF', 'P', 303, 40),
    (test_files_path / 'MapCanada.png', 'PNG', 'RGBA', 3000, 2408)
]


@pytest.mark.parametrize(variable_names, values)
def test_png_metadata(path, original_format, mode, width, height):
    file_obj = File(path)
    assert file_obj.metadata['original_format'] == original_format
    assert file_obj.metadata['mode'] == mode
    assert file_obj.metadata['width'] == width
    assert file_obj.metadata['height'] == height


@pytest.mark.parametrize(variable_names, values)
def test_save_png_metadata(copy_file, original_format, mode, width, height):
    test_png_metadata(copy_file, 'PNG', mode, width, height)


@pytest.mark.parametrize("path", map(lambda x: x[0], values))
def test_png_invalid_save_location(path):
    png_file = File(path)
    invalid_save_path = '/non_existent_folder/' + os.path.basename(path)
    with pytest.raises(FileProcessingFailedError):
        png_file.processor.save(invalid_save_path)


@pytest.mark.parametrize("path", map(lambda x: x[0], values))
def test_not_opening_file(path):
    with patch('builtins.open', autospec=True) as mock_open:
        File(path, open_file=False)
        mock_open.assert_not_called()


@pytest.mark.parametrize("path", map(lambda x: x[0], values))
@pytest.mark.parametrize("algorithm", ["md5", "sha256"])
def test_png_copy_with_integrity(path, algorithm, tmp_path):
    file_obj = File(path, open_file=False)
    expected_hash = file_obj.processor.compute_hash(algorithm)

    dest_path = tmp_path / Path(path).name
    file_obj.copy(dest_path, verify_integrity=True)

    copied = File(dest_path)
    assert copied.processor.compute_hash(algorithm) == expected_hash


@pytest.mark.parametrize("path", map(lambda x: x[0], values))
def test_png_copy_integrity_failure(path, tmp_path, monkeypatch):
    file_obj = File(path, open_file=False)

    def corrupt_copy(src, dst, *, follow_symlinks=True):
        with open(dst, 'w') as f:
            f.write("corrupted png data")

    monkeypatch.setattr(shutil, "copy2", corrupt_copy)

    with pytest.raises(FileProcessingFailedError) as excinfo:
        file_obj.copy(tmp_path / Path(path).name, verify_integrity=True)
    assert "Integrity check failed" in str(excinfo.value)
