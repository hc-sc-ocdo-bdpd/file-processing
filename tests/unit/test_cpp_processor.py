import os
import shutil
import pytest
from pathlib import Path
from unittest.mock import patch
from file_processing.file import File
from file_processing.errors import FileProcessingFailedError
from file_processing_test_data import get_test_files_path

test_files_path = get_test_files_path()

values = [
    ('MemoryOutStream.cpp', 'ascii', 218, 2, 0, 0),
    ('XmlTestReporter.cpp', 'ascii', 130, 3, 0, 1),
    ('arithm.cpp', 'ascii', 2411, 39, 0, 37),
    ('lr.cpp', 'ascii', 604, 6, 11, 44),
    ('scan_9.cc', 'ascii', 544, 3, 1, 51),
    ('bert_defs.cc', 'ascii', 1860, 17, 0, 114),
    ('learner.cc', 'ascii', 1516, 27, 8, 164),
    ('loop.cc', 'ascii', 277, 4, 0, 45),
]

@pytest.mark.parametrize(
    "file_name, encoding, num_lines, num_functions, num_classes, num_comments",
    values
)
def test_cpp_metadata_extraction(file_name, encoding, num_lines, num_functions, num_classes, num_comments):
    cpp_file_path = test_files_path / file_name
    cpp_file = File(str(cpp_file_path))

    assert cpp_file.processor.metadata['encoding'] == encoding
    assert cpp_file.processor.metadata['num_lines'] == num_lines
    assert cpp_file.processor.metadata['num_functions'] == num_functions
    assert cpp_file.processor.metadata['num_classes'] == num_classes
    assert cpp_file.processor.metadata['num_comments'] == num_comments

@pytest.mark.parametrize("file_name", [name for name, *_ in values])
def test_cpp_invalid_save_location(file_name):
    cpp_file = File(str(test_files_path / file_name))
    invalid_save_path = '/non_existent_folder/' + file_name
    with pytest.raises(FileProcessingFailedError):
        cpp_file.save(invalid_save_path)

@pytest.mark.parametrize("file_name", [name for name, *_ in values])
def test_cpp_processor_open_file_false(file_name):
    cpp_file_path = test_files_path / file_name
    with patch("builtins.open") as mock_open:
        File(str(cpp_file_path), open_file=False)
        mock_open.assert_not_called()

@pytest.mark.parametrize("file_name", [v[0] for v in values])
@pytest.mark.parametrize("algorithm", ["md5", "sha256"])
def test_cpp_copy_with_integrity(file_name, algorithm, tmp_path):
    src_path = test_files_path / file_name
    file_obj = File(str(src_path), open_file=False)
    original_hash = file_obj.processor.compute_hash(algorithm)

    dest_path = tmp_path / file_name
    file_obj.copy(str(dest_path), verify_integrity=True)

    copied_file = File(str(dest_path))
    assert copied_file.processor.compute_hash(algorithm) == original_hash

@pytest.mark.parametrize("file_name", [v[0] for v in values])
def test_cpp_copy_integrity_failure(file_name, tmp_path, monkeypatch):
    file_obj = File(str(test_files_path / file_name), open_file=False)

    def corrupt(src, dest, *, follow_symlinks=True):
        with open(dest, 'w') as f:
            f.write("CORRUPTED!")

    monkeypatch.setattr(shutil, "copy2", corrupt)

    with pytest.raises(FileProcessingFailedError) as excinfo:
        file_obj.copy(str(tmp_path / file_name), verify_integrity=True)
    assert "Integrity check failed" in str(excinfo.value)
