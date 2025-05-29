import os
from pathlib import Path
from unittest.mock import patch
import pytest
from file_processing import File
from file_processing.errors import FileProcessingFailedError
from file_processing_test_data import get_test_files_path

# Data fixture
test_files_path = get_test_files_path()
variable_names = (
    "path, text_length, encoding, num_rows, num_cols, num_cells, empty_cells"
)
values = [
    (test_files_path / '2021_Census_English.csv', 6084302, 'ISO-8859-1', 36835, 23, 847205, 253932),
    (test_files_path / 'Approved_Schools_2023_10_01.csv', 1403268, 'UTF-8-SIG', 5385, 13, 70005, 73)
]

@pytest.mark.parametrize(variable_names, values)
def test_csv_metadata(path, text_length, encoding, num_rows, num_cols, num_cells, empty_cells):
    file_obj = File(path)
    assert len(file_obj.metadata['text']) == text_length
    assert file_obj.metadata['encoding'] == encoding
    assert file_obj.metadata['num_rows'] == num_rows
    assert file_obj.metadata['num_cols'] == num_cols
    assert file_obj.metadata['num_cells'] == num_cells
    assert file_obj.metadata['empty_cells'] == empty_cells

@pytest.mark.parametrize(variable_names, values)
def test_save_csv_metadata(copy_file, text_length, encoding, num_rows, num_cols, num_cells, empty_cells):
    # Reuse metadata assertions on the saved file
    test_csv_metadata(copy_file, text_length, encoding, num_rows, num_cols, num_cells, empty_cells)

@pytest.mark.parametrize("valid_path", [p for p, *_ in values])
def test_csv_invalid_save_location(valid_path):
    csv_file = File(valid_path)
    invalid_path = '/non_existent_folder/' + os.path.basename(str(valid_path))
    with pytest.raises(FileProcessingFailedError):
        csv_file.processor.save(invalid_path)

@pytest.mark.parametrize(variable_names, values)
def test_not_opening_file(path, text_length, encoding, num_rows, num_cols, num_cells, empty_cells):
    with patch('builtins.open', autospec=True) as mock_open:
        File(path, open_file=False)
        mock_open.assert_not_called()

@pytest.mark.parametrize(variable_names, values)
@pytest.mark.parametrize("algorithm", ["md5", "sha256"])
def test_csv_copy_with_integrity(path, tmp_path, algorithm,
                                 text_length, encoding, num_rows, num_cols, num_cells, empty_cells):
    # 1. Compute original hash (raw file)
    file_obj = File(path, open_file=False)
    original_hash = file_obj.processor.compute_hash(algorithm)

    # 2. Copy with integrity verification
    dest = tmp_path / Path(path).name
    file_obj.copy(str(dest), verify_integrity=True)

    # 3. Re-open and verify metadata unchanged
    saved = File(str(dest))
    assert len(saved.metadata['text']) == text_length
    assert saved.metadata['encoding'] == encoding
    assert saved.metadata['num_rows'] == num_rows
    assert saved.metadata['num_cols'] == num_cols
    assert saved.metadata['num_cells'] == num_cells
    assert saved.metadata['empty_cells'] == empty_cells

    # 4. Verify hash matches for chosen algorithm
    assert saved.processor.compute_hash(algorithm) == original_hash

@pytest.mark.parametrize("path", [p for p, *_ in values])
def test_csv_copy_integrity_failure(path, tmp_path, monkeypatch):
    file_obj = File(path, open_file=False)
    # Simulate corruption in raw copy
    import shutil
    def corrupt(src, dest, *, follow_symlinks=True):
        with open(dest, 'w') as f:
            f.write('CORRUPTED!')
    monkeypatch.setattr(shutil, 'copy2', corrupt)

    with pytest.raises(FileProcessingFailedError) as excinfo:
        file_obj.copy(str(tmp_path / Path(path).name), verify_integrity=True)
    assert 'Integrity check failed' in str(excinfo.value)
