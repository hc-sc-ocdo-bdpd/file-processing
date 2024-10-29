import pytest
from file_processing import File
from file_processing.errors import OptionalDependencyNotInstalledError
from file_processing_test_data import get_test_files_path
import builtins

@pytest.mark.parametrize("file_name", ["test_ocr_text.pdf"])
def test_ocr_missing_dependency_error(file_name, monkeypatch):
    """
    Test that OCR processing raises OptionalDependencyNotInstalledError when 'file-processing-ocr' is missing.
    """
    # Store the original __import__ function
    original_import = builtins.__import__

    # Define a custom import function that raises ImportError for 'file_processing_ocr' and 'pytesseract'
    def mocked_import(name, globals, locals, fromlist, level):
        if name.startswith('file_processing_ocr') or name == 'pytesseract':
            raise ImportError(f"No module named '{name}'")
        return original_import(name, globals, locals, fromlist, level)

    # Replace the built-in __import__ with our custom function
    monkeypatch.setattr(builtins, '__import__', mocked_import)

    test_files_path = get_test_files_path()
    file_path = test_files_path / file_name

    with pytest.raises(OptionalDependencyNotInstalledError) as exc_info:
        # Attempt to process an OCR-compatible file without 'file-processing-ocr' installed
        File(str(file_path), use_ocr=True)

    # Check that the error message is as expected
    assert "Please install it using 'pip install file-processing-ocr'" in str(exc_info.value)

@pytest.mark.parametrize("file_name", ["sample_speech.mp3"])
def test_transcription_missing_dependency_error(file_name, monkeypatch):
    """
    Test that transcription processing raises OptionalDependencyNotInstalledError when 'file-processing-transcription' is missing.
    """
    original_import = builtins.__import__

    def mocked_import(name, globals, locals, fromlist, level):
        if name.startswith('file_processing_transcription') or name == 'whisper':
            raise ImportError(f"No module named '{name}'")
        return original_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, '__import__', mocked_import)

    test_files_path = get_test_files_path()
    file_path = test_files_path / file_name

    with pytest.raises(OptionalDependencyNotInstalledError) as exc_info:
        # Attempt to process a transcription-compatible file without 'file-processing-transcription' installed
        File(str(file_path), use_transcriber=True)

    # Check that the error message is as expected
    assert "Please install it using 'pip install file-processing-transcription'" in str(exc_info.value)
