import pytest
from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cdist
from file_processing import File
from file_processing.tools.errors import NotTranscriptionApplicableError

variable_names = "path, transcription, language"
values = [
    ("tests/resources/test_files/sample_speech.aiff",
     "and thank you for your continued support thank you", "en"),
    ("tests/resources/test_files/sample_speech.flac",
     "into a lease with us they go through an extensive counseling process and legal review with summaries of it with signed statements that they understand what they're getting themselves into and what they have to do and what they own and what they don't own and they own the", "en"),
    ("tests/resources/test_files/sample_speech.mp3",
     "from our volunteers in maui county when the storms on top of us or a disaster is headed our way or a disaster has just happened because they truly love the work that they're doing and there's something that draws them to red cross something from the heart where", "en"),
    ("tests/resources/test_files/sample_speech.mp4",
     "we're definitely in support of this concept and we'll figure a way to make it work very good and then i know it's a work in progress but in relation to enforcement any type", "en"),
    ("tests/resources/test_files/sample_speech.ogg",
     "mr clarke mr chair proceeding with committee reports you have before you from your policy an intergovernmental affairs committee committee report fifteen dash fifteen recommending the adoption of the resolution", "en"),
    ("tests/resources/test_files/sample_speech.wav",
     "into a lease with us they go through an extensive counseling process and legal review with summaries of it with signed statements that they understand what they're getting themselves into and what they have to do and what they own and what they don't own and they own the", "en")
]

@pytest.mark.parametrize(variable_names, values)
def test_transcription_processing_success(path, transcription, language):
    audio_file = File(path, use_transcriber=True)
    
    assert 'text' in audio_file.metadata
    assert CosineSimilarity(audio_file, transcription).calculate().round(3) >= 0.8
    assert audio_file.metadata['language'] == language


def test_transcription_processing_non_applicable_file(non_transcription_applicable_file):
    with pytest.raises(NotTranscriptionApplicableError):
        File(non_transcription_applicable_file, use_transcriber=True)
