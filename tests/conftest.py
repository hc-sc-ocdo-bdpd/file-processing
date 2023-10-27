import sys, os
sys.path.append(os.path.join(sys.path[0],'file_processing'))
import pytest
from file_processing.file import File
from errors import FileProcessingFailedError, FileCorruptionError

# copy_file fixture to be used in test_..._processor.py files
@pytest.fixture()
def copy_file(path, tmp_path_factory):
    from pathlib import Path
    copy_path = str(tmp_path_factory.mktemp("copy") / Path(path).name)
    file_obj = File(path)
    file_obj.save(copy_path)
    yield copy_path

# invalid_save_location fixture to be used in test_..._processor.py files
@pytest.fixture()
def invalid_save_location(path):
    save_path = '/non_existent_folder/' + path
    file_obj = File(path)
    with pytest.raises(FileProcessingFailedError):
        file_obj.processor.save(save_path)

# corrupted_file_processing fixture to be used in test_..._processor.py file
@pytest.fixture()
def corrupted_file_processing(path):
    with pytest.raises(FileProcessingFailedError):
        File(path)

# corrupted_file_processing_lock fixture to be used in test_..._processor.py file (for files that could be potentially locked)
@pytest.fixture()
def corrupted_file_processing_lock(path):
    with pytest.raises(FileCorruptionError):
        File(path)