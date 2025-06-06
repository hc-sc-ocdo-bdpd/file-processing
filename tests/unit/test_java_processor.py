import os
import shutil
from pathlib import Path
import pytest
from unittest.mock import patch
from file_processing.file import File
from file_processing.errors import FileProcessingFailedError
from file_processing_test_data import get_test_files_path

# Get the directory where test files are stored
test_files_path = get_test_files_path()

# Java test file metadata expectations (filename, text length, encoding, num_lines, num_methods, num_classes)
values = [
    ('DataTypes.java', 59831, 'ascii', 1409, 70, 17),
    ('ExecutionJobVertex.java', 27219, 'ascii', 695, 24, 2),
    ('TopicAdmin.java', 39062, 'ascii', 770, 25, 3),
    ('Utils.java', 4721, 'ascii', 106, 7, 1),
]

@pytest.mark.parametrize(
    "file_name, text_length, encoding, num_lines, num_methods, num_classes",
    values
)
def test_java_metadata_extraction(file_name, text_length, encoding, num_lines, num_methods, num_classes):
    """Tests Java file processing metadata extraction."""
    java_file_path = test_files_path / file_name
    java_file = File(java_file_path)

    assert len(java_file.processor.metadata['text']) == text_length
    assert java_file.processor.metadata['encoding'] == encoding
    assert java_file.processor.metadata['num_lines'] == num_lines
    assert java_file.processor.metadata['num_methods'] == num_methods
    assert java_file.processor.metadata['num_classes'] == num_classes

@pytest.mark.parametrize("file_name", [v[0] for v in values])
def test_java_invalid_save_location(file_name):
    """Tests that saving to an invalid location raises an error."""
    java_file = File(test_files_path / file_name)
    invalid_save_path = '/non_existent_folder/' + file_name
    with pytest.raises(FileProcessingFailedError):
        java_file.save(invalid_save_path)

@pytest.mark.parametrize("file_name", [v[0] for v in values])
def test_java_processor_open_file_false(file_name):
    """Tests that the file is not opened when open_file=False."""
    java_file_path = test_files_path / file_name
    with patch("builtins.open") as mock_open:
        File(java_file_path, open_file=False)
        mock_open.assert_not_called()

@pytest.mark.parametrize("file_name", [v[0] for v in values])
@pytest.mark.parametrize("algorithm", ["md5", "sha256"])
def test_java_copy_with_integrity(file_name, algorithm, tmp_path):
    """Tests that copied Java file maintains integrity (hash match)."""
    path = test_files_path / file_name
    file_obj = File(str(path), open_file=False)
    original_hash = file_obj.processor.compute_hash(algorithm)

    dest_path = tmp_path / file_name
    file_obj.copy(str(dest_path), verify_integrity=True)

    copied = File(str(dest_path))
    assert copied.processor.compute_hash(algorithm) == original_hash

@pytest.mark.parametrize("file_name", [v[0] for v in values])
def test_java_copy_integrity_failure(file_name, tmp_path, monkeypatch):
    """Tests that a corrupted Java copy raises integrity failure."""
    path = test_files_path / file_name
    file_obj = File(str(path), open_file=False)

    def corrupt(src, dest, *, follow_symlinks=True):
        with open(dest, 'w') as f:
            f.write("CORRUPTED!")

    monkeypatch.setattr(shutil, "copy2", corrupt)

    with pytest.raises(FileProcessingFailedError) as excinfo:
        file_obj.copy(str(tmp_path / file_name), verify_integrity=True)
    assert "Integrity check failed" in str(excinfo.value)
