from file_processor_strategy import FileProcessorStrategy
from PyPDF2 import PdfReader

class PdfFileProcessor(FileProcessorStrategy):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.metadata = {}

    def process(self, startPage=None, endPage=None):
        self.startPage=startPage
        self.endPage=endPage
        text = self.extract_text_from_pdf(self)
        if text is not None:
            self.metadata.update({'text': text})
    
    @staticmethod
    def extract_text_from_pdf(self):
        try:
            pdfFileObj = open(self.file_path, 'rb')
            reader = PdfReader(pdfFileObj)
            numPages=len(reader.pages)
            
            #Check if start and end page are specified. If not read the whole document
            if (self.startPage == None) or (type(self.startPage) != type(0)):
                self.startPage = 0
            else:
                self.startPage = self.startPage
            
            if (self.endPage == None) or (self.endPage > numPages) or (type(self.endPage) != type(0)):
                self.endPage = numPages
            else:
                self.endPage = self.endPage
            
            if self.startPage<0 or self.endPage>numPages or self.startPage>numPages or self.startPage>self.endPage:
                raise Exception("Invalid page specification.")
            
            text = ""
            for i in range(self.startPage, self.endPage):
                pageObj = reader.pages[i]
                
                text += pageObj.extract_text() #extract the text of the page
            
            pdfFileObj.close()
            return text
        except Exception as e:
            print(f"Error encountered while opening or processing {self.file_path}: {e}")
            return None


# OCR functionality: to implement