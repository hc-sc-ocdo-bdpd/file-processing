import re
import pytest
from file_processing.file import File
from file_processing.errors import NotOCRApplciableError

PDF_SAMPLES = ["tests/resources/test_files/test_ocr_text.pdf", "tests/resources/test_files/test_ocr_text_2.pdf"]
JPEG_SAMPLES = ["tests/resources/test_files/test_ocr_text.jpg", "tests/resources/test_files/test_ocr_text_2.jpg"]
PNG_SAMPLES = ["tests/resources/test_files/test_ocr_text.png", "tests/resources/test_files/test_ocr_text_2.png"]
TIF_SAMPLES = ["tests/resources/test_files/test_ocr_text.tif", "tests/resources/test_files/test_ocr_text_2.tif"]
TIFF_SAMPLES = ["tests/resources/test_files/test_ocr_text.tiff", "tests/resources/test_files/test_ocr_text_2.tiff"]
GIF_SAMPLES = ["tests/resources/test_files/test_ocr_text.gif", "tests/resources/test_files/test_ocr_text_2.gif"]
NON_OCR_APPLICABLE_SAMPLES = ["tests/resources/test_files/Empty.zip", "tests/resources/test_files/Sample.xml"]

EXPECTED_OCR_RESULTS = {
    PDF_SAMPLES[0]: 'Test OCR text successful!',
    PDF_SAMPLES[1]: 'Test OCR text successful!',
    JPEG_SAMPLES[0]: 'Test OCR text successful!',
    JPEG_SAMPLES[1]: 'Test OCR text successful!',
    PNG_SAMPLES[0]: 'Test OCR text successful!',
    PNG_SAMPLES[1]: 'Test OCR text successful!',
    TIF_SAMPLES[0]: 'Test OCR text successful!',
    TIF_SAMPLES[1]: 'Test OCR text successful!',
    TIFF_SAMPLES[0]: 'Test OCR text successful!',
    TIFF_SAMPLES[1]: 'Test OCR text successful!',
    GIF_SAMPLES[0]: 'Test OCR text successful!',
    GIF_SAMPLES[1]: 'Test OCR text successful!',
}

@pytest.fixture(params=PDF_SAMPLES + JPEG_SAMPLES + PNG_SAMPLES + TIF_SAMPLES + TIFF_SAMPLES + GIF_SAMPLES)
def ocr_applicable_file(request):
    return request.param, EXPECTED_OCR_RESULTS[request.param]

@pytest.fixture(params=NON_OCR_APPLICABLE_SAMPLES)
def non_ocr_applicable_file(request):
    return request.param

def test_ocr_processing_success(ocr_applicable_file):
    file_path, expected_ocr_result = ocr_applicable_file
    file = File(str(file_path), use_ocr=True)
    assert 'ocr_text' in file.metadata

    predicted_text = re.sub('[^A-Za-z0-9!? ]+', '', file.metadata['ocr_text'])
    assert predicted_text == expected_ocr_result

def test_ocr_processing_non_applicable_file(non_ocr_applicable_file):
    with pytest.raises(NotOCRApplciableError):
        File(str(non_ocr_applicable_file), use_ocr=True)

