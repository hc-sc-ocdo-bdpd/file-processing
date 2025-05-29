import os
import shutil
import pytest
from unittest.mock import patch
from datetime import datetime
from pathlib import Path
from file_processing import File
from file_processing.errors import FileProcessingFailedError
from file_processing_test_data import get_test_files_path

test_files_path = get_test_files_path()

variable_names = "path, text_length, subject, date, sender"
values = [
    (test_files_path / 'Test Email.msg', 19, 'Test Email', 'Mon, 18 Sep 2023 13:57:16 -0400', '"Burnett, Taylen (HC/SC)" <Taylen.Burnett@hc-sc.gc.ca>'),
    (test_files_path / 'Health Canada Overview from Wikipedia.msg', 13876, 'Health Canada Overview from Wikipedia', 'Tue, 31 Oct 2023 14:54:03 -0400', '"Prazuch, Karolina (HC/SC)" <karolina.prazuch@hc-sc.gc.ca>')
]

@pytest.mark.parametrize(variable_names, values)
def test_msg_metadata(path, text_length, subject, date, sender):
    file_obj = File(path)

    if isinstance(file_obj.metadata['date'], str):
        processed_date = datetime.strptime(file_obj.metadata['date'], "%a, %d %b %Y %H:%M:%S %z")
    else:
        processed_date = file_obj.metadata['date']
    
    true_date = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %z")

    assert len(file_obj.metadata['text']) == text_length
    assert file_obj.metadata['subject'] == subject
    assert processed_date == true_date
    assert file_obj.metadata['sender'] == sender
    assert 'thread' in file_obj.metadata
    assert isinstance(file_obj.metadata['thread'], dict)

@pytest.mark.parametrize(variable_names, values)
def test_save_msg_metadata(copy_file, text_length, subject, date, sender):
    test_msg_metadata(copy_file, text_length, subject, date, sender)

@pytest.mark.parametrize("path", map(lambda x: x[0], values))
def test_msg_invalid_save_location(path):
    msg_file = File(path)
    invalid_save_path = '/non_existent_folder/' + os.path.basename(path)
    with pytest.raises(FileProcessingFailedError):
        msg_file.processor.save(invalid_save_path)

@pytest.mark.parametrize("path", map(lambda x: x[0], values))
def test_msg_open_file_false(path):
    with patch('builtins.open', autospec=True) as mock_open:
        File(path, open_file=False)
        mock_open.assert_not_called()

@pytest.mark.parametrize("path", map(lambda x: x[0], values))
@pytest.mark.parametrize("algorithm", ["md5", "sha256"])
def test_msg_copy_with_integrity(path, algorithm, tmp_path):
    file_obj = File(path, open_file=False)
    expected_hash = file_obj.processor.compute_hash(algorithm)

    dest_path = tmp_path / Path(path).name
    file_obj.copy(dest_path, verify_integrity=True)

    copied = File(dest_path)
    assert copied.processor.compute_hash(algorithm) == expected_hash

@pytest.mark.parametrize("path", map(lambda x: x[0], values))
def test_msg_copy_integrity_failure(path, tmp_path, monkeypatch):
    file_obj = File(path, open_file=False)

    def corrupt(src, dst, *, follow_symlinks=True):
        with open(dst, 'w') as f:
            f.write("INVALID MSG FILE")

    monkeypatch.setattr(shutil, "copy2", corrupt)

    with pytest.raises(FileProcessingFailedError) as excinfo:
        file_obj.copy(tmp_path / Path(path).name, verify_integrity=True)
    assert "Integrity check failed" in str(excinfo.value)
