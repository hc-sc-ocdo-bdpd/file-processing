import os
import shutil
from pathlib import Path
from unittest.mock import patch
import pytest
from file_processing import File
from file_processing.errors import FileProcessingFailedError
from file_processing_test_data import get_test_files_path

test_files_path = get_test_files_path()

# Define the variable names and values specific to .gitignore files
variable_names = "path, text_length, num_lines, num_words"
values = [
    (test_files_path / 'Python.gitignore', 3139, 163, 403),
    (test_files_path / 'tensorflow.gitignore', 939, 53, 52)
]

@pytest.mark.parametrize(variable_names, values)
def test_gitignore_metadata(path, text_length, num_lines, num_words):
    file_obj = File(path)
    assert len(file_obj.metadata['text']) == text_length
    assert file_obj.metadata['num_lines'] == num_lines
    assert file_obj.metadata['num_words'] == num_words

@pytest.mark.parametrize(variable_names, values)
def test_not_opening_file(path, text_length, num_lines, num_words):
    with patch('builtins.open', autospec=True) as mock_open:
        File(path, open_file=False)
        mock_open.assert_not_called()

@pytest.mark.parametrize(variable_names, values)
def test_save_gitignore_metadata(copy_file, text_length, num_lines, num_words):
    test_gitignore_metadata(copy_file, text_length, num_lines, num_words)

@pytest.mark.parametrize("path", map(lambda x: x[0], values))
def test_gitignore_invalid_save_location(path):
    gitignore_file = File(path)
    invalid_save_path = '/non_existent_folder/' + os.path.basename(path)
    with pytest.raises(FileProcessingFailedError):
        gitignore_file.save(invalid_save_path)

@pytest.mark.parametrize("path", [v[0] for v in values])
@pytest.mark.parametrize("algorithm", ["md5", "sha256"])
def test_gitignore_copy_with_integrity(path, algorithm, tmp_path):
    file_obj = File(path, open_file=False)
    original_hash = file_obj.processor.compute_hash(algorithm)

    dest_path = tmp_path / Path(path).name
    file_obj.copy(str(dest_path), verify_integrity=True)

    copied = File(str(dest_path))
    assert copied.processor.compute_hash(algorithm) == original_hash

@pytest.mark.parametrize("path", [v[0] for v in values])
def test_gitignore_copy_integrity_failure(path, tmp_path, monkeypatch):
    file_obj = File(path, open_file=False)

    def corrupt(src, dest, *, follow_symlinks=True):
        with open(dest, 'w') as f:
            f.write("CORRUPTED!")

    monkeypatch.setattr(shutil, "copy2", corrupt)

    with pytest.raises(FileProcessingFailedError) as excinfo:
        file_obj.copy(str(tmp_path / Path(path).name), verify_integrity=True)
    assert "Integrity check failed" in str(excinfo.value)
