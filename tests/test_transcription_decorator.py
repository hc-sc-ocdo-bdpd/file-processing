from unittest.mock import patch
import pytest
from Levenshtein import ratio
from file_processing import File
from file_processing.tools.errors import NotTranscriptionApplicableError

variable_names = "path, transcription"
values = [
    ("tests/resources/test_files/sample_speech.aiff",
     "and thank you for your continued support thank you"),
    ("tests/resources/test_files/sample_speech.flac",
     "into a lease with us they go through an extensive counseling process and legal review with summaries of it with signed statements that they understand what they're getting themselves into and what they have to do and what they own and what they don't own and they own the"),
    ("tests/resources/test_files/sample_speech.mp3",
     "into a lease with us they go through an extensive counseling process and legal review with summaries of it with signed statements that they understand what they're getting themselves into and what they have to do and what they own and what they don't own and they own the"),
    ("tests/resources/test_files/sample_speech.mp4",
     "we're definitely in support of this concept and we'll figure a way to make it work very good and then i know it's a work in progress but in relation to enforcement any type"),
    ("tests/resources/test_files/sample_speech.ogg",
     "mr clarke mr chair proceeding with committee reports you have before you from your policy an intergovernmental affairs committee committee report fifteen dash fifteen recommending the adoption of the resolution"),
    ("tests/resources/test_files/sample_speech.wav",
     "into a lease with us they go through an extensive counseling process and legal review with summaries of it with signed statements that they understand what they're getting themselves into and what they have to do and what they own and what they don't own and they own the")
]

NON_TRANSCRIPTION_APPLICABLE_SAMPLES = [
    "tests/resources/test_files/Empty.zip",
    "tests/resources/test_files/Sample.xml"
]


@pytest.fixture(params=NON_TRANSCRIPTION_APPLICABLE_SAMPLES)
def non_transcription_applicable_file(request):
    return request.param


## Non-mocked test for reference
# @pytest.mark.parametrize(variable_names, values)
# def test_transcription_processing_success(path, transcription):
#     audio_file = File(path, use_transcriber=True)

#     assert 'text' in audio_file.metadata

#     similarity = ratio(audio_file.metadata['text'], transcription)
#     assert similarity >= 0.8


@pytest.mark.parametrize(variable_names, values)
def test_mock_transcription(path, transcription):
    mocked_value = {
        'text': transcription,
        'language': 'en'
    }
    with patch('whisper.transcribe', return_value=mocked_value) as mock_transcribe:
        audio_file = File(path, use_transcriber=True)
        mock_transcribe.assert_called()
        assert audio_file.metadata['text'] == transcription


def test_transcription_processing_non_applicable_file(non_transcription_applicable_file):
    with pytest.raises(NotTranscriptionApplicableError):
        File(non_transcription_applicable_file, use_transcriber=True)
