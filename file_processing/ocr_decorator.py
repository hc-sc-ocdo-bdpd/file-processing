import PyPDF2
import pytesseract
from PIL import Image
import os
import io
import getpass

# Init for tesseract
pytesseract.pytesseract.tesseract_cmd = os.path.join('C:/Users', getpass.getuser(), 'AppData/Local/Programs/Tesseract-OCR/tesseract.exe')

class OCRDecorator:
    def __init__(self, processor):
        """Initializes the OCRDecorator with a given file processor."""
        self._processor = processor

    def process(self):
        """Processes the file using the wrapped processor and then applies OCR."""
        self._processor.process()
        ocr_text = self.extract_text_with_ocr()
        self._processor.metadata['ocr_text'] = ocr_text


    def extract_text_with_ocr(self):
        """Extracts text from the file using OCR.

        Returns:
            str: The extracted text.
        """
        extension = self._processor.extension
            
        if extension == ".pdf":
            return self._ocr_pdf()
        else:
            return self._ocr_image()

    def _ocr_image(self):
        try:
            image = Image.open(self._processor.file_path)
            ocr_result = pytesseract.image_to_string(image)
            return ocr_result
        except Exception as e:
            print(f"Error during OCR processing for image: {e}")
            return ""

    def _ocr_pdf(self):
        text = ''
        ocrText = ''

        try:
            pdfFileObj = open(self._processor.file_path, 'rb')
            reader = PyPDF2.PdfReader(pdfFileObj)
            numPages = len(reader.pages)

            # Assuming you want to read the whole document for the OCRDecorator
            startPage = 0
            endPage = numPages

            for i in range(startPage, endPage):
                pageObj = reader.pages[i]
                
                text += pageObj.extract_text()  # extract the text of the page
                
                for image in pageObj.images:  # extract the images of the page
                    ocrText += pytesseract.image_to_string(Image.open(io.BytesIO(image.data)))
            pdfFileObj.close()

            # Combine the extracted text and OCR text
            combined_text = text + "\n" + ocrText
            return combined_text

        except Exception as e:
            print(f"Error during OCR processing for PDF: {e}")
            return ""

    @property
    def file_name(self):
        """Returns the file name of the processed file."""
        return self._processor.file_name

    @property
    def metadata(self):
        """Returns the metadata of the processed file."""
        return self._processor.metadata
