import pytest
import os
from pathlib import Path
from file import File
from errors import OCRProcessingError, NotOCRApplciableError

# TO DO:
# Files and ocr results need to be created and filled in.

PDF_SAMPLES = ["sample1.pdf", "sample2.pdf"]
JPEG_SAMPLES = ["sample1.jpeg", "sample2.jpeg"]
PNG_SAMPLES = ["sample1.png", "sample2.png"]
NON_OCR_APPLICABLE_SAMPLES = ["sample1.txt", "sample2.txt"]

EXPECTED_OCR_RESULTS = {
    PDF_SAMPLES[0]: "Expected OCR result for PDF 1",
    PDF_SAMPLES[1]: "Expected OCR result for PDF 2",
    JPEG_SAMPLES[0]: "Expected OCR result for JPEG 1",
    JPEG_SAMPLES[1]: "Expected OCR result for JPEG 2",
    PNG_SAMPLES[0]: "Expected OCR result for PNG 1",
    PNG_SAMPLES[1]: "Expected OCR result for PNG 2",
}

@pytest.fixture(params=PDF_SAMPLES + JPEG_SAMPLES + PNG_SAMPLES)
def ocr_applicable_file(request):
    return request.param, EXPECTED_OCR_RESULTS[request.param]

@pytest.fixture(params=NON_OCR_APPLICABLE_SAMPLES)
def non_ocr_applicable_file(request):
    return request.param

def test_ocr_processing_success(ocr_applicable_file):
    file_path, expected_ocr_result = ocr_applicable_file
    file = File(str(file_path), use_ocr=True)
    assert 'ocr_text' in file.metadata
    assert file.metadata['ocr_text'] == expected_ocr_result

def test_ocr_processing_non_applicable_file(non_ocr_applicable_file):
    with pytest.raises(NotOCRApplciableError):
        File(str(non_ocr_applicable_file), use_ocr=True)

