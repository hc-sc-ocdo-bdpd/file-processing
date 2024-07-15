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

def test_ocr_text_key_in_metadata_when_use_ocr_true(directory_instance):
    ocr_extensions = [".pdf", ".jpeg", ".jpg", ".png", ".gif", ".tiff", ".tif"]
    for file_instance in directory_instance._file_generator():
        if file_instance.path.suffix in ocr_extensions: 
            if "error" not in file_instance.metadata:
                assert "ocr_text" in file_instance.metadata, "Expected 'ocr_text' key in file.metadata when use_ocr is True"

def test_transcription_text_key_in_metadata_when_use_transcribers_true(directory_instance):
    transcription_extensions = [".mp3", ".wav", ".mp4", ".flac", ".aiff", ".ogg"]   
    for file_instance in directory_instance._file_generator():
        if file_instance.path.suffix in transcription_extensions:
            if "error" not in file_instance.metadata:
                assert "text" in file_instance.metadata and "language" in file_instance.metadata, "Expected 'text' and 'language' keys in file.metadata when use_transcribers is True"










