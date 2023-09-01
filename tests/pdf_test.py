import pytest
from src.Document import Document


def test_pdfTextFound():
    doc = Document('tests/resources/test_files/SampleReport.pdf')
    assert len(doc.text) > 0
    assert len(doc.ocrText) == 0

def test_pdfOcrTextFound():
    doc = Document('tests/resources/test_files/SampleReportScreenShot.pdf')
    text = doc.text.strip()
    assert len(text) == 0
    assert len(doc.ocrText) > 0

def test_pdfTextFound_pagespec():
    doc = Document(startPage=0,endPage=1,path='tests/resources/test_files/ArtificialNeuralNetworksForBeginners.pdf')
    assert len(doc.text) > 0
    assert len(doc.ocrText) == 0

def test_pdfOcrTextFound_pagespec():
    doc = Document(startPage=4,endPage=5,path='tests/resources/test_files/ArtificialNeuralNetworksForBeginners.pdf')
    text = doc.text.strip()
    assert len(text) == 0
    assert len(doc.ocrText) > 0

def test_invalid_page():
    with pytest.raises(ValueError) as exc_info:
        Document(startPage=3,endPage=2,path='tests/resources/test_files/ArtificialNeuralNetworksForBeginners.pdf')
    assert str(exc_info.value)=="Invalid page specification."