import os
import shutil
import pytest
from unittest.mock import patch
from pathlib import Path
from file_processing import File
from file_processing.errors import FileProcessingFailedError
from file_processing_test_data import get_test_files_path

test_files_path = get_test_files_path()

variable_names = "path, num_keys, key_names, empty_values"
values = [
    (test_files_path / 'coffee.json', 15, ['quiz', 'sport', 'q1', 'question', 'options', 'answer', 'maths', 'q1', 'question', 'options', 'answer', 'q2', 'question', 'options', 'answer'], 0),
    (test_files_path / 'sample.json', 9, ['array', 'boolean', 'color', 'null', 'number', 'object', 'a', 'c', 'string'], 1)
]

@pytest.mark.parametrize(variable_names, values)
def test_json_metadata(path, num_keys, key_names, empty_values):
    file_obj = File(path)
    assert file_obj.metadata['num_keys'] == num_keys
    assert file_obj.metadata['key_names'] == key_names
    assert file_obj.metadata['empty_values'] == empty_values

@pytest.mark.parametrize(variable_names, values)
def test_save_json_metadata(copy_file, num_keys, key_names, empty_values):
    test_json_metadata(copy_file, num_keys, key_names, empty_values)

@pytest.mark.parametrize("path", map(lambda x: x[0], values))
def test_json_invalid_save_location(path):
    json_file = File(path)
    invalid_save_path = '/non_existent_folder/' + os.path.basename(path)
    with pytest.raises(FileProcessingFailedError):
        json_file.processor.save(invalid_save_path)

@pytest.mark.parametrize("path", map(lambda x: x[0], values))
def test_json_open_file_false(path):
    with patch('builtins.open', autospec=True) as mock_open:
        File(path, open_file=False)
        mock_open.assert_not_called()

@pytest.mark.parametrize("path", map(lambda x: x[0], values))
@pytest.mark.parametrize("algorithm", ["md5", "sha256"])
def test_json_copy_with_integrity(path, algorithm, tmp_path):
    """Tests JSON file copy with integrity verification using hash only."""
    file_obj = File(path, open_file=False)
    expected_hash = file_obj.processor.compute_hash(algorithm)

    dest_path = tmp_path / path.name
    file_obj.copy(dest_path, verify_integrity=True)

    copied = File(dest_path)
    assert copied.processor.compute_hash(algorithm) == expected_hash

@pytest.mark.parametrize("path", map(lambda x: x[0], values))
def test_json_copy_integrity_failure(path, tmp_path, monkeypatch):
    file_obj = File(path, open_file=False)

    def corrupt(src, dst, *, follow_symlinks=True):
        with open(dst, 'w') as f:
            f.write("INVALID JSON")

    monkeypatch.setattr(shutil, "copy2", corrupt)

    with pytest.raises(FileProcessingFailedError) as excinfo:
        file_obj.copy(tmp_path / path.name, verify_integrity=True)
    assert "Integrity check failed" in str(excinfo.value)
