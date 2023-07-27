import pytest
import PyPDF2

def test_MultiPage():
    #One page pdf file
    doc1 = open('generated_tables\DmZUHweaZfPcMjTCAySRtp.pdf', 'rb')
    #Four page pdf file
    doc2 = open('generated_tables\GBnzszrSV2sAXLEH5k7SFz.pdf', 'rb')
    
    pdfReader1 = PyPDF2.PdfReader(doc1)
    pdfReader2 = PyPDF2.PdfReader(doc2)
  
    # count number of pages
    totalPages1 = len(pdfReader1.pages)
    totalPages2 = len(pdfReader2.pages)
    
    assert totalPages1 == 1
    assert totalPages2 > 1
