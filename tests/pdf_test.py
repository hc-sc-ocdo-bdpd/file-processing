import pytest
import sys
sys.path.append('file_processing')
from file_processing.file import File

def test_pdfTextFound():
    doc = File('resources/SampleReport.pdf')
    assert len(doc.metadata['text']) > 0

def test_pdfTextFound_pagespec():
    doc = File(path='resources/ArtificialNeuralNetworksForBeginners.pdf').processor
    doc.process(startPage=0,endPage=1)
    assert len(doc.metadata['text']) > 0


'''
def test_pdfOcrTextFound():
    doc = Document('resources/SampleReportScreenShot.pdf')
    text = doc.text.strip()
    assert len(text) == 0
    assert len(doc.ocrText) > 0

def test_pdfOcrTextFound_pagespec():
    doc = Document(startPage=4,endPage=5,path='resources/ArtificialNeuralNetworksForBeginners.pdf')
    text = doc.text.strip()
    assert len(text) == 0
    assert len(doc.ocrText) > 0
'''

def test_invalid_page(capsys):
    File(path='resources/ArtificialNeuralNetworksForBeginners.pdf').processor.process(startPage=3,endPage=2)
    captured=capsys.readouterr()
    assert "Error encountered while opening or processing resources/ArtificialNeuralNetworksForBeginners.pdf: Invalid page specification." in captured.out