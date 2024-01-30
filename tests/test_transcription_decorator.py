import pytest
from utils.cosine_similarity import CosineSimilarity
from file_processing import File
from file_processing.tools.errors import NotTranscriptionApplicableError

variable_names = "path, actual_transcription_path, language"
values = [
    ('tests/resources/test_files/How Canadas Universal HealthCare System Works.mp3', 'tests/resources/true_transcriptions/How Canadas Universal HealthCare System Works.txt', 'en'),
    ('tests/resources/test_files/Super Easy French.wav', 'tests/resources/true_transcriptions/Super Easy French.txt', 'fr'),
    ('tests/resources/test_files/Taylor Swift.mp4', 'tests/resources/true_transcriptions/Taylor Swift.txt', 'en'),
    ('tests/resources/test_files/Jingle Bell Rock.flac', 'tests/resources/true_transcriptions/Jingle Bell Rock.txt', 'en'),
    ('tests/resources/test_files/Katy Perry.aiff', 'tests/resources/true_transcriptions/Katy Perry.txt', 'en'),
    ('tests/resources/test_files/Frosty the Snowman.ogg', 'tests/resources/true_transcriptions/Frosty the Snowman.txt', 'en')
]
NON_TRANSCRIPTION_APPLICABLE_SAMPLES = ["tests/resources/test_files/Empty.zip", "tests/resources/test_files/Sample.xml"]

@pytest.fixture(params=NON_TRANSCRIPTION_APPLICABLE_SAMPLES)
def non_transcription_applicable_file(request):
    return request.param

@pytest.mark.parametrize(variable_names, values)
def test_transcription_processing_success(path, actual_transcription_path, language):
    audio_file = File(path, use_transcriber=True)
    transcription_file = File(actual_transcription_path)
    assert 'text' in audio_file.metadata
    assert CosineSimilarity(audio_file, transcription_file).calculate().round(3) >= 0.8
    assert audio_file.metadata['language'] == language

def test_transcription_processing_non_applicable_file(non_transcription_applicable_file):
    with pytest.raises(NotTranscriptionApplicableError):
        File(non_transcription_applicable_file, use_transcriber=True)
