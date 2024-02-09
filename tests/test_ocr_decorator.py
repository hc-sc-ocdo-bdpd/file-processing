import re
import os
from unittest.mock import patch
import pytest
from file_processing import File
from file_processing.tools.errors import NotOCRApplicableError

PDF_SAMPLES = ["tests/resources/test_files/test_ocr_text.pdf", "tests/resources/test_files/test_ocr_text_2.pdf"]
JPEG_SAMPLES = ["tests/resources/test_files/test_ocr_text.jpg", "tests/resources/test_files/test_ocr_text_2.jpg"]
PNG_SAMPLES = ["tests/resources/test_files/test_ocr_text.png", "tests/resources/test_files/test_ocr_text_2.png"]
TIF_SAMPLES = ["tests/resources/test_files/test_ocr_text.tif", "tests/resources/test_files/test_ocr_text_2.tif"]
TIFF_SAMPLES = ["tests/resources/test_files/test_ocr_text.tiff", "tests/resources/test_files/test_ocr_text_2.tiff"]
GIF_SAMPLES = ["tests/resources/test_files/test_ocr_text.gif", "tests/resources/test_files/test_ocr_text_2.gif"]
NON_OCR_APPLICABLE_SAMPLES = ["tests/resources/test_files/Empty.zip", "tests/resources/test_files/Sample.xml"]


@pytest.fixture(params=PDF_SAMPLES + JPEG_SAMPLES + PNG_SAMPLES + TIF_SAMPLES + TIFF_SAMPLES + GIF_SAMPLES)
def ocr_applicable_file(request):
    return request.param


@pytest.fixture(params=NON_OCR_APPLICABLE_SAMPLES)
def non_ocr_applicable_file(request):
    return request.param


## Non-mocked test for reference
# def test_ocr_processing_success(ocr_applicable_file):
#     file_path = ocr_applicable_file
#     file = File(str(file_path), use_ocr=True)
#     assert 'ocr_text' in file.metadata

#     result = re.sub('[^A-Za-z0-9!? ]+', '', file.metadata['ocr_text'])
#     assert result == 'Test OCR text successful!'


@patch('pytesseract.image_to_string')
def test_ocr_processing_success(mock_tesseract, ocr_applicable_file):
    image_path = os.path.normpath(ocr_applicable_file)
    mock_tesseract.return_value = 'Test OCR text successful!'
    file = File(image_path, use_ocr=True)
    result = re.sub('[^A-Za-z0-9!? ]+', '', file.metadata['ocr_text'])

    assert result == 'Test OCR text successful!'
    mock_tesseract.assert_called()


def test_ocr_processing_non_applicable_file(non_ocr_applicable_file):
    with pytest.raises(NotOCRApplicableError):
        File(str(non_ocr_applicable_file), use_ocr=True)
