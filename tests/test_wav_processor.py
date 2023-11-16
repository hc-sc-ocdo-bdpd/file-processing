import pytest
import sys, os
sys.path.append(os.path.join(sys.path[0], 'file_processing'))
from file_processing.file import File
from errors import FileProcessingFailedError

variable_names = "path, text_length, language, duration_seconds"
values = [
   ('tests/resources/test_files/How Canadas Universal HealthCare System Works.wav', 9572, 'en', 576.0123263888889),
   ('tests/resources/test_files/Super Easy French.wav', 2704, 'fr', 218.9706875)
]

@pytest.mark.parametrize(variable_names, values)
def test_wav_metadata(path, text_length, language, duration_seconds):
    file_obj = File(path)
    assert len(file_obj.metadata['text']) == text_length
    assert file_obj.metadata['language'] == language
    assert file_obj.metadata['duration_seconds'] == duration_seconds

@pytest.fixture()
def copy_file(path, tmp_path_factory):
   from pathlib import Path
   copy_path = str(tmp_path_factory.mktemp("copy") / Path(path).name)
   file_obj = File(path)
   file_obj.save(copy_path)
   yield copy_path

@pytest.mark.parametrize("path, text_length, language, duration_seconds", map(lambda x: x[:4], values))
def test_save_wav_metadata(copy_file, text_length, language, duration_seconds):

   # Load via File object
   wav_file = File(copy_file)

   # Save the updated file
   wav_file.save()
   test_wav_metadata(copy_file, text_length, language, duration_seconds)

invalid_save_locations = [
   ('tests/resources/test_files/How Canadas Universal HealthCare System Works.wav', '/non_existent_folder/How Canadas Universal HealthCare System Works.wav')
]

@pytest.mark.parametrize("path, save_path", invalid_save_locations)
def test_wav_invalid_save_location(path, save_path):
   file_obj = File(path)
   with pytest.raises(FileProcessingFailedError):
      file_obj.save(save_path)

corrupted_files = [
   'tests/resources/test_files/Super Easy French Corrupted.wav'
]

@pytest.mark.parametrize("path", corrupted_files)
def test_wav_corrupted_file_processing(path):
   with pytest.raises(FileProcessingFailedError):
      File(path)