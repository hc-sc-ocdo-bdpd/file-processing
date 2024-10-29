import pytest
from file_processing import File
from file_processing.errors import NotOCRApplicableError, TesseractNotFound
from file_processing_ocr.errors import OCRProcessingError
from file_processing_test_data import get_test_files_path

OCR_APPLICABLE_SAMPLES = [
    "test_ocr_text.pdf", "test_ocr_text_2.pdf",
    "test_ocr_text.jpg", "test_ocr_text_2.jpg",
    "test_ocr_text.png", "test_ocr_text_2.png",
    "test_ocr_text.tif", "test_ocr_text_2.tif",
    "test_ocr_text.tiff", "test_ocr_text_2.tiff",
    "test_ocr_text.gif", "test_ocr_text_2.gif"
]
EXPECTED_OCR_TEXT = "Test OCR text successful!"

@pytest.mark.parametrize("file_name", OCR_APPLICABLE_SAMPLES)
def test_ocr_integration(file_name):
    """
    Test integration of file-processing and file-processing-ocr on real OCR-compatible files.
    """
    test_files_path = get_test_files_path()
    file_path = test_files_path / file_name

    try:
        # Initialize the File object with OCR enabled
        file_obj = File(str(file_path), use_ocr=True)

        # Check that OCR text is extracted and matches expected output
        assert 'ocr_text' in file_obj.metadata, "OCR text not found in metadata"
        assert file_obj.metadata['ocr_text'].strip() == EXPECTED_OCR_TEXT, "OCR text does not match expected output"

    except TesseractNotFound:
        pytest.fail("Tesseract is not installed or not accessible in the path.")
    except OCRProcessingError as e:
        pytest.fail(f"OCR processing failed: {e}")

@pytest.mark.parametrize("file_name", OCR_APPLICABLE_SAMPLES)
def test_ocr_with_invalid_tesseract_path(file_name):
    """
    Test OCR processing failure when an invalid Tesseract path is provided.
    """
    test_files_path = get_test_files_path()
    file_path = test_files_path / file_name
    invalid_ocr_path = "/invalid/path/to/tesseract"

    with pytest.raises(TesseractNotFound):
        # Attempt to process the file with OCR using an invalid Tesseract path
        File(str(file_path), use_ocr=True, ocr_path=invalid_ocr_path)

@pytest.mark.parametrize("file_name", ["Empty.zip", "Sample.xml"])
def test_ocr_not_applicable_error(file_name):
    """
    Test that OCR processing raises NotOCRApplicableError for unsupported file types.
    """
    test_files_path = get_test_files_path()
    file_path = test_files_path / file_name

    with pytest.raises(NotOCRApplicableError):
        # Attempt to process a file not compatible with OCR
        File(str(file_path), use_ocr=True)
