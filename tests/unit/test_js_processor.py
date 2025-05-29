import os
import shutil
from unittest.mock import patch
import pytest
from pathlib import Path
from file_processing.file import File
from file_processing.errors import FileProcessingFailedError
from file_processing_test_data import get_test_files_path

test_files_path = get_test_files_path()

# JavaScript test file metadata expectations:
# (file_name, encoding, num_lines, num_functions, num_classes, num_comments)
values = [
    ('jest-cli.js', 'ascii', 401, 8, 0, 26),
    ('swipe.js', 'ascii', 146, 0, 1, 7),
    ('tab.js', 'ascii', 315, 0, 1, 23),
    ('Fibers.js', 'utf-8', 407, 6, 0, 3),
]

@pytest.mark.parametrize(
    "file_name, encoding, num_lines, num_functions, num_classes, num_comments",
    values
)
def test_js_metadata_extraction(file_name, encoding, num_lines, num_functions, num_classes, num_comments):
    """Tests JavaScript file processing metadata extraction."""
    js_file_path = test_files_path / file_name
    js_file = File(js_file_path)

    metadata = js_file.processor.metadata
    assert metadata['encoding'] == encoding
    assert metadata['num_lines'] == num_lines
    assert metadata['num_functions'] == num_functions
    assert metadata['num_classes'] == num_classes
    assert metadata['num_comments'] == num_comments

@pytest.mark.parametrize("file_name", [entry[0] for entry in values])
def test_js_invalid_save_location(file_name):
    """Tests that saving to an invalid location raises an error."""
    js_file_path = test_files_path / file_name
    js_file = File(js_file_path)
    invalid_save_path = '/non_existent_folder/' + file_name
    with pytest.raises(FileProcessingFailedError):
        js_file.save(invalid_save_path)

@pytest.mark.parametrize("file_name", [entry[0] for entry in values])
def test_js_processor_open_file_false(file_name):
    """Tests that the file is not opened when open_file=False."""
    js_file_path = test_files_path / file_name
    with patch("builtins.open") as mock_open:
        File(js_file_path, open_file=False)
        mock_open.assert_not_called()

@pytest.mark.parametrize("file_name", [entry[0] for entry in values])
@pytest.mark.parametrize("algorithm", ["md5", "sha256"])
def test_js_copy_with_integrity(file_name, algorithm, tmp_path):
    """Tests JavaScript file copy with integrity verification (hash only)."""
    src_path = test_files_path / file_name
    file_obj = File(src_path, open_file=False)
    expected_hash = file_obj.processor.compute_hash(algorithm)

    dest_path = tmp_path / file_name
    file_obj.copy(dest_path, verify_integrity=True)

    copied = File(dest_path)
    assert copied.processor.compute_hash(algorithm) == expected_hash

@pytest.mark.parametrize("file_name", [entry[0] for entry in values])
def test_js_copy_integrity_failure(file_name, tmp_path, monkeypatch):
    """Tests that integrity verification fails if the copy is corrupted."""
    file_obj = File(test_files_path / file_name, open_file=False)

    def corrupt(src, dest, *, follow_symlinks=True):
        with open(dest, 'w') as f:
            f.write("CORRUPTED!")

    monkeypatch.setattr(shutil, "copy2", corrupt)

    with pytest.raises(FileProcessingFailedError) as excinfo:
        file_obj.copy(tmp_path / file_name, verify_integrity=True)
    assert "Integrity check failed" in str(excinfo.value)
