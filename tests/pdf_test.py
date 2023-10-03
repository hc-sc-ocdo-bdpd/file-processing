import pytest
from src.Document import Document
import sys, os
sys.path.append(os.path.join(sys.path[0],'file_processing'))

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

def test_save_pdf_metadata():
    from file_processing.file import File
    
    test_pdf_path = 'tests/resources/test_files/ArtificialNeuralNetworksForBeginners.pdf'
    copy_test_pdf_path = 'tests/resources/test_files/ArtificialNeuralNetworksForBeginners_copy.pdf'
    
    # Copying file
    with open(test_pdf_path, 'rb') as src_file:
        with open(copy_test_pdf_path, 'wb') as dest_file:
            dest_file.write(src_file.read())

    try:
        
        # Load via File object
        pdf_file = File(copy_test_pdf_path)

        # Save changes
        pdf_file.save()
        
        # Load document again to check if saved correctly
        pdf = Document(copy_test_pdf_path)
        
        # Assert if correct
        
        assert len(pdf.text) > 0

    finally:
        
        # Clean up by removing the copied file after the test is done
        os.remove(copy_test_pdf_path)