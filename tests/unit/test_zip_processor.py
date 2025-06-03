import os
import shutil
from unittest.mock import patch
import tempfile
import zipfile
import pytest
from file_processing import File
from file_processing.errors import FileProcessingFailedError
from file_processing_test_data import get_test_files_path

test_files_path = get_test_files_path()

variable_names = "path, num_files, file_types, file_names"
values = [
    (test_files_path / 'SampleReport.zip', 3, {'docx': 2, 'pptx': 1}, ['SampleReport.docx', 'SampleReport.pptx', 'HealthCanadaOverviewFromWikipedia.docx']),
    (test_files_path / 'Empty.zip', 0, {}, [])
]

@pytest.fixture(params=values, ids=[str(x[0]) for x in values])
def file_obj(request):
    return File(request.param[0])

def test_zip_extraction(file_obj):
    file_obj.processor.extract()

    extraction_dir = os.path.splitext(file_obj.path)[0]
    assert os.path.isdir(extraction_dir)

    extracted_files = os.listdir(extraction_dir)
    expected_files = file_obj.metadata['file_names']
    assert set(extracted_files) == set(expected_files)

    shutil.rmtree(extraction_dir)

def test_zip_save(file_obj):
    with tempfile.TemporaryDirectory() as temp_dir:
        original_zip_path = file_obj.path
        saved_zip_path = os.path.join(temp_dir, 'SavedSampleReport.zip')

        file_obj.processor.save(saved_zip_path)

        assert os.path.exists(saved_zip_path)

        with zipfile.ZipFile(original_zip_path, 'r') as original_zip, zipfile.ZipFile(saved_zip_path, 'r') as saved_zip:
            assert set(original_zip.namelist()) == set(
                saved_zip.namelist())  # Check contents are still the same

@pytest.mark.parametrize(variable_names, values)
def test_zip_metadata(path, num_files, file_types, file_names):
    file_obj = File(path)
    assert file_obj.metadata['num_files'] == num_files
    assert file_obj.metadata['file_types'] == file_types
    assert file_obj.metadata['file_names'] == file_names

@pytest.mark.parametrize(variable_names, values)
def test_save_zip_metadata(copy_file, num_files, file_types, file_names):
    test_zip_metadata(copy_file, num_files, file_types, file_names)

@pytest.mark.parametrize("path", map(lambda x: x[0], values))
def test_zip_invalid_save_location(path):
    zip_file = File(path)
    invalid_save_path = '/non_existent_folder/' + os.path.basename(path)
    with pytest.raises(FileProcessingFailedError):
        zip_file.save(invalid_save_path)

@pytest.mark.parametrize("path", map(lambda x: x[0], values))
def test_not_opening_file(path):
    with patch('builtins.open', autospec=True) as mock_open:
        File(path, open_file=False)
        mock_open.assert_not_called()

@pytest.mark.parametrize("path", map(lambda x: x[0], values))
@pytest.mark.parametrize("algorithm", ["md5", "sha256"])
def test_zip_copy_with_integrity(path, algorithm, tmp_path):
    file_obj = File(path, open_file=False)
    expected_hash = file_obj.processor.compute_hash(algorithm)

    dest_path = tmp_path / os.path.basename(path)
    file_obj.copy(dest_path, verify_integrity=True)

    copied = File(dest_path)
    assert copied.processor.compute_hash(algorithm) == expected_hash

@pytest.mark.parametrize("path", map(lambda x: x[0], values))
def test_zip_copy_integrity_failure(path, tmp_path, monkeypatch):
    file_obj = File(path, open_file=False)

    def corrupt_copy(src, dst, *, follow_symlinks=True):
        with open(dst, "w") as f:
            f.write("corrupted content")

    monkeypatch.setattr(shutil, "copy2", corrupt_copy)

    with pytest.raises(FileProcessingFailedError) as excinfo:
        file_obj.copy(tmp_path / os.path.basename(path), verify_integrity=True)
    assert "Integrity check failed" in str(excinfo.value)
