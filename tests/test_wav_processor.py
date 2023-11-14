import pytest
import sys, os
sys.path.append(os.path.join(sys.path[0], 'file_processing'))
from file_processing.file import File
from errors import FileProcessingFailedError


variable_names = "path, text_length, language"
values = [
   ('tests/resources/test_files/How Canadas Universal HealthCare System Works.wav', 9572, 'en'),
   ('tests/resources/test_files/Super Easy French.wav', 2704, 'fr')
]


@pytest.mark.parametrize(variable_names, values)
def test_wav_metadata(path, text_length, language):
    file_obj = File(path)
    assert len(file_obj.metadata['text']) == text_length
    assert file_obj.metadata['language'] == language