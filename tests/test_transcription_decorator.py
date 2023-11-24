import pytest
import sys, os
sys.path.append(os.path.join(sys.path[0], 'file_processing'))
from file import File
from errors import TranscriptionProcessingError, NotTranscriptionApplicableError

MP3_SAMPLES = ['tests/resources/test_files/How Canadas Universal HealthCare System Works.mp3', 'tests/resources/test_files/Super Easy French.mp3']
WAV_SAMPLES = ['tests/resources/test_files/How Canadas Universal HealthCare System Works.wav', 'tests/resources/test_files/Super Easy French.wav']
MP4_SAMPLES = ['tests/resources/test_files/Taylor Swift.mp4']
FLAC_SAMPLES = ['tests/resources/test_files/Jingle Bell Rock.flac']
AIFF_SAMPLES = ['tests/resources/test_files/Katy Perry.aiff']
OGG_SAMPLES = ['tests/resources/test_files/Frosty the Snowman.ogg']
NON_TRANSCRIPTION_APPLICABLE_SAMPLES = ["tests/resources/test_files/Empty.zip", "tests/resources/test_files/Sample.xml"]

EXPECTED_TRANSCRIPTION_RESULTS = {
    MP3_SAMPLES[0]: [[9570, 9570], 'en'],
    MP3_SAMPLES[1]: [[2704, 2704], 'fr'],
    WAV_SAMPLES[0]: [[9572, 9572], 'en'],
    WAV_SAMPLES[1]: [[2704, 2704], 'fr'],
    MP4_SAMPLES[0]: [[1826, 2200], 'en'],
    FLAC_SAMPLES[0]: [[954, 1100], 'en'],
    AIFF_SAMPLES[0]: [[1630, 1901], 'en'],
    OGG_SAMPLES[0]: [[1182, 1182], 'en'],
}

@pytest.fixture(params=MP3_SAMPLES + WAV_SAMPLES + MP4_SAMPLES + FLAC_SAMPLES + AIFF_SAMPLES + OGG_SAMPLES)
def transcription_applicable_file(request):
    return request.param, EXPECTED_TRANSCRIPTION_RESULTS[request.param]

@pytest.fixture(params=NON_TRANSCRIPTION_APPLICABLE_SAMPLES)
def non_transcription_applicable_file(request):
    return request.param

def test_transcription_processing_success(transcription_applicable_file):
    file_path, expected_transcription_result = transcription_applicable_file
    file = File(file_path, use_transcriber=True)
    assert 'transcribed_text' in file.metadata
    assert (expected_transcription_result[0][0] <= len(file.metadata['transcribed_text']) <= expected_transcription_result[0][1])
    assert file.metadata['language'] == expected_transcription_result[1]

def test_transcription_processing_non_applicable_file(non_transcription_applicable_file):
    with pytest.raises(NotTranscriptionApplicableError):
        File(non_transcription_applicable_file, use_transcriber=True)
