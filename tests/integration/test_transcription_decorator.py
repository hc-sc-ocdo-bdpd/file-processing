# file-processing/tests/test_transcription_decorator.py
import pytest
from file_processing import File
from file_processing.errors import NotTranscriptionApplicableError
from file_processing_transcription.errors import TranscriptionProcessingError
from file_processing_test_data import get_test_files_path

# Full set of transcription-applicable sample files
TRANSCRIPTION_APPLICABLE_SAMPLES = [
    'sample_speech.aiff',
    'sample_speech.flac',
    'sample_speech.mp3',
    'sample_speech.mp4',
    'sample_speech.ogg',
    'sample_speech.wav',
]

@pytest.mark.parametrize("file_name", TRANSCRIPTION_APPLICABLE_SAMPLES)
def test_transcription_integration(file_name):
    """
    Test integration of file-processing and file-processing-transcription on real audio files.
    """
    test_files_path = get_test_files_path()
    audio_file_path = test_files_path / file_name

    try:
        # Initialize the File object with transcription enabled
        file_obj = File(str(audio_file_path), use_transcriber=True)

        # Check that transcription text was generated and language identified
        assert 'transcribed_text' in file_obj.metadata, "Transcribed text not found in metadata"
        assert 'transcribed_language' in file_obj.metadata, "Transcribed language not found in metadata"
        assert len(file_obj.metadata['transcribed_text']) > 0, "Transcription text is empty"

    except TranscriptionProcessingError as e:
        pytest.fail(f"Transcription processing failed: {e}")

@pytest.mark.parametrize("file_name", ["Empty.zip", "Sample.xml"])
def test_transcription_not_applicable_error(file_name):
    """
    Test that transcription processing raises NotTranscriptionApplicableError for unsupported file types.
    """
    test_files_path = get_test_files_path()
    file_path = test_files_path / file_name

    with pytest.raises(NotTranscriptionApplicableError):
        # Attempt to process a file not compatible with transcription
        File(str(file_path), use_transcriber=True)

@pytest.mark.parametrize("file_name", TRANSCRIPTION_APPLICABLE_SAMPLES)
def test_transcription_ffmpeg_not_found_error(file_name, monkeypatch):
    """
    Test transcription processing failure when 'ffmpeg' is not found in system PATH.
    """
    test_files_path = get_test_files_path()
    audio_file_path = test_files_path / file_name

    # Temporarily remove 'ffmpeg' from PATH
    monkeypatch.setenv("PATH", "")

    with pytest.raises(TranscriptionProcessingError):
        # Attempt to process the file, expecting ffmpeg error
        File(str(audio_file_path), use_transcriber=True)
