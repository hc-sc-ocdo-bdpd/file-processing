import os
import shutil
from unittest.mock import patch
from docx import Document
import pytest
from pathlib import Path
from file_processing import File
from file_processing.errors import FileProcessingFailedError
from file_processing_test_data import get_test_files_path

test_files_path = get_test_files_path()

variable_names = "path, text_length, last_modified_by, author"
values = [
    (test_files_path / 'HealthCanadaOverviewFromWikipedia.docx', 1631, 'Test last_modified_by One', 'Test Author One'),
    (test_files_path / 'SampleReport.docx', 3220, 'last_modified_by Test Author', 'Second Test Author')
]


@pytest.mark.parametrize(variable_names, values)
def test_docx_metadata(path, text_length, last_modified_by, author):
    file_obj = File(path)
    assert len(file_obj.metadata['text']) == text_length
    assert file_obj.metadata['last_modified_by'] == last_modified_by
    assert file_obj.metadata['author'] == author


@pytest.mark.parametrize("path, text_length", map(lambda x: x[:2], values))
def test_save_docx_metadata(copy_file, text_length):
    docx_file = File(copy_file)
    docx_file.metadata['last_modified_by'] = 'Modified New'
    docx_file.metadata['author'] = 'New Author'
    docx_file.save()
    test_docx_metadata(copy_file, text_length, 'Modified New', 'New Author')


@pytest.mark.parametrize("path, text_length", map(lambda x: x[:2], values))
def test_change_docx_author_last_modified_by(copy_file, text_length):
    docx_file = Document(copy_file)
    docx_file.core_properties.last_modified_by = "Modified New"
    docx_file.core_properties.author = "New Author"
    docx_file.save(copy_file)
    test_docx_metadata(copy_file, text_length, 'Modified New', 'New Author')


@pytest.mark.parametrize("path", map(lambda x: x[0], values))
def test_docx_invalid_save_location(path):
    docx_file = File(path)
    invalid_save_path = '/non_existent_folder/' + os.path.basename(path)
    with pytest.raises(FileProcessingFailedError):
        docx_file.processor.save(invalid_save_path)


@pytest.mark.parametrize("path", map(lambda x: x[0], values))
def test_not_opening_file(path):
    with patch('builtins.open', autospec=True) as mock_open:
        File(path, open_file=False)
        mock_open.assert_not_called()


locked_files = [
    (test_files_path / 'SampleReport_Locked.docx'),
    (test_files_path / 'HealthCanadaOverviewFromWikipedia_Locked.docx')
]


@pytest.mark.parametrize("path", locked_files)
def test_docx_locked(path):
    assert File(path).metadata["has_password"] is True


@pytest.mark.parametrize("path", [v[0] for v in values])
@pytest.mark.parametrize("algorithm", ["md5", "sha256"])
def test_docx_copy_with_integrity(path, algorithm, tmp_path):
    file_obj = File(path, open_file=False)
    file_obj.process()
    original_hash = file_obj.processor.compute_hash(algorithm)

    dest_path = tmp_path / Path(path).name
    file_obj.copy(str(dest_path), verify_integrity=True)

    copied = File(str(dest_path))
    copied.process()

    assert copied.processor.compute_hash(algorithm) == original_hash


@pytest.mark.parametrize("path", [v[0] for v in values])
def test_docx_copy_integrity_failure(path, tmp_path, monkeypatch):
    file_obj = File(path, open_file=False)

    def corrupt(src, dest, *, follow_symlinks=True):
        with open(dest, 'w') as f:
            f.write("CORRUPTED!")

    monkeypatch.setattr(shutil, "copy2", corrupt)

    with pytest.raises(FileProcessingFailedError) as excinfo:
        file_obj.copy(str(tmp_path / Path(path).name), verify_integrity=True)
    assert "Integrity check failed" in str(excinfo.value)
