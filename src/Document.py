import PyPDF2
import pytesseract
from PIL import Image
import os
import io
import getpass
import logging
from pdfminer.high_level import extract_text

# Init for tesseract
pytesseract.pytesseract.tesseract_cmd = os.path.join('C:/Users',getpass.getuser(),'AppData/Local/Programs/Tesseract-OCR/tesseract.exe')

class Document:

    def __init__(self, path = './', startPage=None, endPage=None):
        self.startPage=startPage
        self.endPage=endPage
        self.loadDocument(path)

    def loadDocument(self, path):
        text = ''
        ocrText = ''

        if str(path).endswith('pdf'):
            pdfFileObj = open(path, 'rb')
            reader = PyPDF2.PdfReader(pdfFileObj)
            numPages=len(reader.pages)

            #Check if start and end page are specified. If not read the whole document
            if (self.startPage == None) or (type(self.startPage) != type(0)):
                startPage = 0
            else:
                startPage = self.startPage
            
            if (self.endPage == None) or (self.endPage > numPages) or (type(self.endPage) != type(0)):
                endPage = numPages
            else:
                endPage = self.endPage
          
            if startPage<0 or endPage>numPages or startPage>numPages or startPage>endPage:
                raise ValueError("Invalid page specification.")

            for i in range(startPage, endPage):
                pageObj = reader.pages[i]
                
                text += pageObj.extract_text() #extract the text of the page
                
                for image in pageObj.images: #extract the images of the page
                    ocrText += pytesseract.image_to_string(Image.open(io.BytesIO(image.data)))
            pdfFileObj.close()

        else:   # Try loading it as an image
            image = Image.open(path)
            ocrText = pytesseract.image_to_string(image)


        self.text = text
        self.ocrText = ocrText

def processSampleDocument(self):
    path = 'resources/SampleReport.pdf'
    #path = 'resources/SampleReportScreenShot.pdf'
    (text, ocrText) = self.loadDocument(path)
    logging.info('Text')
    logging.info(text)
    logging.info('-------------')
    logging.info('OCR Text')
    logging.info(ocrText)