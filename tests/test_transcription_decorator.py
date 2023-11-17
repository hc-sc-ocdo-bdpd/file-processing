import pytest
import sys, os
sys.path.append(os.path.join(sys.path[0], 'file_processing'))
from file import File
from errors import TranscriptionProcessingError, NotTranscriptionApplicableError

MP3_SAMPLES = ['tests/resources/test_files/How Canadas Universal HealthCare System Works.mp3', 'tests/resources/test_files/Super Easy French.mp3']
WAV_SAMPLES = ['tests/resources/test_files/How Canadas Universal HealthCare System Works.wav', 'tests/resources/test_files/Super Easy French.wav']
# MP4_SAMPLES = []
# FLAC_SAMPLES = []
NON_TRANSCRIPTION_APPLICABLE_SAMPLES = ["tests/resources/test_files/Empty.zip", "tests/resources/test_files/Sample.xml"]

EXPECTED_TRANSCRIPTION_RESULTS = {
    MP3_SAMPLES[0]: [9570, 'en'],
    MP3_SAMPLES[1]: [2704, 'fr'],
    WAV_SAMPLES[0]: [9572, 'en'],
    WAV_SAMPLES[1]: [2704, 'fr']
}

@pytest.fixture(params=MP3_SAMPLES + WAV_SAMPLES)
def transcription_applicable_file(request):
    return request.param, EXPECTED_TRANSCRIPTION_RESULTS[request.param]

@pytest.fixture(params=NON_TRANSCRIPTION_APPLICABLE_SAMPLES)
def non_transcription_applicable_file(request):
    return request.param

def test_transcription_processing_success(transcription_applicable_file):
    file_path, expected_transcription_result = transcription_applicable_file
    file = File(str(file_path), use_transcriber=True)
    assert 'transcribed_text' in file.metadata
    assert len(file.metadata['transcribed_text']) == expected_transcription_result[0]
    assert file.metadata['language'] == expected_transcription_result[1]

def test_transcription_processing_non_applicable_file(non_transcription_applicable_file):
    with pytest.raises(NotTranscriptionApplicableError):
        File(str(non_transcription_applicable_file), use_transcriber=True)
