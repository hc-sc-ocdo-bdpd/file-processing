import os
import shutil
from pathlib import Path
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

@pytest.mark.parametrize("file_name", [v[0] for v in values])
@pytest.mark.parametrize("algorithm", ["md5", "sha256"])
def test_h_copy_with_integrity(file_name, algorithm, tmp_path):
    """Tests that copied .h file maintains integrity (hash match)."""
    path = test_files_path / file_name
    file_obj = File(str(path), open_file=False)
    original_hash = file_obj.processor.compute_hash(algorithm)

    dest_path = tmp_path / file_name
    file_obj.copy(str(dest_path), verify_integrity=True)

    copied = File(str(dest_path))
    assert copied.processor.compute_hash(algorithm) == original_hash


@pytest.mark.parametrize("file_name", [v[0] for v in values])
def test_h_copy_integrity_failure(file_name, tmp_path, monkeypatch):
    """Tests that a corrupted .h copy raises integrity failure."""
    path = test_files_path / file_name
    file_obj = File(str(path), open_file=False)

    def corrupt(src, dest, *, follow_symlinks=True):
        with open(dest, 'w') as f:
            f.write("CORRUPTED!")

    monkeypatch.setattr(shutil, "copy2", corrupt)

    with pytest.raises(FileProcessingFailedError) as excinfo:
        file_obj.copy(str(tmp_path / file_name), verify_integrity=True)
    assert "Integrity check failed" in str(excinfo.value)
