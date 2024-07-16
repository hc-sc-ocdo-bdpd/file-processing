from file_processing import Directory, File
import pytest

@pytest.fixture
def directory_instance(use_ocr=True, use_transcribers=True):
    return Directory("tests/resources/directory_test_files", use_ocr=use_ocr, use_transcribers=use_transcribers)

def test_file_metadata_in_processor_dict(directory_instance):
    for file_instance in directory_instance._file_generator():
        assert isinstance(file_instance, File), "Every file should be an instance of the File class"
        file_metadata = file_instance.metadata
        file_processor_dict = file_instance.processor.__dict__
        assert file_metadata in file_processor_dict.values(), "file.metadata should be in file.processor.__dict__"







