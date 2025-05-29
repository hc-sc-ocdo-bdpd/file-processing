import os
import shutil
from unittest.mock import patch
import pytest
from file_processing import File
from file_processing.errors import FileProcessingFailedError
from file_processing_test_data import get_test_files_path

test_files_path = get_test_files_path()

variable_names = "path, sheet_names, active_sheet, data, last_modified_by, creator"
values = [
    (test_files_path / 'Test_excel_file.xlsx', ['Sheet1', 'Sheet2', 'Sheet3'], "Sheet3", 42,
     'Burnett, Taylen (HC/SC)', 'Burnett, Taylen (HC/SC)'),
    (test_files_path / 'Government.xlsx', ['Health Canada', 'Government of Canada'],
     "Government of Canada", 49, 'Prazuch, Karolina (HC/SC)', 'Prazuch, Karolina (HC/SC)')
]


@pytest.mark.parametrize(variable_names, values)
def test_xlsx_metadata(path, sheet_names, active_sheet, data, last_modified_by, creator):
    file_obj = File(path)
    assert file_obj.metadata['sheet_names'] == sheet_names
    assert file_obj.metadata['active_sheet'] == active_sheet
    assert sum(len(file_obj.metadata["data"][x]) for x in file_obj.metadata["data"].keys()) == data
    assert file_obj.metadata['last_modified_by'] == last_modified_by
    assert file_obj.metadata['creator'] == creator


@pytest.mark.parametrize("path", map(lambda x: x[0], values))
def test_not_opening_file(path):
    with patch('builtins.open', autospec=True) as mock_open:
        File(path, open_file=False)
        mock_open.assert_not_called()


locked_files = [
    test_files_path / 'Test_excel_file_Locked.xlsx',
    test_files_path / 'StructureofCanadianFederalGovFromWikipedia_Locked.xlsx'
]


@pytest.mark.parametrize("path", locked_files)
def test_xlsx_locked(path):
    assert File(path).metadata["has_password"] is True


@pytest.mark.parametrize("path, sheet_names, active_sheet, data", map(lambda x: x[:4], values))
def test_save_xlsx_metadata(copy_file, sheet_names, active_sheet, data):
    xlsx_file = File(copy_file)
    xlsx_file.metadata['last_modified_by'] = 'Modified Creator'
    xlsx_file.metadata['creator'] = 'New Creator'
    xlsx_file.save()
    test_xlsx_metadata(copy_file, sheet_names, active_sheet, data, 'Modified Creator', 'New Creator')


@pytest.mark.parametrize("path", map(lambda x: x[0], values))
def test_xlsx_invalid_save_location(path):
    xlsx_file = File(path)
    invalid_save_path = '/non_existent_folder/' + os.path.basename(path)
    with pytest.raises(FileProcessingFailedError):
        xlsx_file.save(invalid_save_path)


@pytest.mark.parametrize("path", map(lambda x: x[0], values))
@pytest.mark.parametrize("algorithm", ["md5", "sha256"])
def test_xlsx_copy_with_integrity(path, algorithm, tmp_path):
    file_obj = File(path, open_file=False)
    expected_hash = file_obj.processor.compute_hash(algorithm)

    dest_path = tmp_path / os.path.basename(path)
    file_obj.copy(dest_path, verify_integrity=True)

    copied = File(dest_path)
    assert copied.processor.compute_hash(algorithm) == expected_hash


@pytest.mark.parametrize("path", map(lambda x: x[0], values))
def test_xlsx_copy_integrity_failure(path, tmp_path, monkeypatch):
    file_obj = File(path, open_file=False)

    def corrupt_copy(src, dst, *, follow_symlinks=True):
        with open(dst, "w") as f:
            f.write("corrupted content")

    # Patch the actual function used by File.copy (shutil.copy2)
    monkeypatch.setattr(shutil, "copy2", corrupt_copy)

    with pytest.raises(FileProcessingFailedError) as excinfo:
        file_obj.copy(tmp_path / os.path.basename(path), verify_integrity=True)
    assert "Integrity check failed" in str(excinfo.value)
