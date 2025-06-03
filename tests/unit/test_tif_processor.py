import os
import shutil
from unittest.mock import patch
import pytest
from file_processing import File
from file_processing.errors import FileProcessingFailedError
from file_processing_test_data import get_test_files_path

test_files_path = get_test_files_path()

variable_names = "path, original_format, mode, width, height"
values = [
    (test_files_path / 'CanadaLogo.tif', 'TIFF', 'RGB', 215, 74),
    (test_files_path / 'MSWordIcon.tiff', 'TIFF', 'RGBA', 79, 106)
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


@pytest.mark.parametrize("path", map(lambda x: x[0], values))
@pytest.mark.parametrize("algorithm", ["md5", "sha256"])
def test_tif_copy_with_integrity(path, algorithm, tmp_path):
    file_obj = File(path, open_file=False)
    expected_hash = file_obj.processor.compute_hash(algorithm)

    dest_path = tmp_path / os.path.basename(path)
    file_obj.copy(dest_path, verify_integrity=True)

    copied = File(dest_path)
    assert copied.processor.compute_hash(algorithm) == expected_hash


@pytest.mark.parametrize("path", map(lambda x: x[0], values))
def test_tif_copy_integrity_failure(path, tmp_path, monkeypatch):
    file_obj = File(path, open_file=False)

    def corrupt_copy(src, dst, *, follow_symlinks=True):
        with open(dst, "w") as f:
            f.write("corrupted content")

    monkeypatch.setattr(shutil, "copy2", corrupt_copy)

    with pytest.raises(FileProcessingFailedError) as excinfo:
        file_obj.copy(tmp_path / os.path.basename(path), verify_integrity=True)
    assert "Integrity check failed" in str(excinfo.value)
