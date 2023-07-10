from file_processor_strategy import FileProcessorStrategy
from PyPDF2 import PdfReader

class PdfFileProcessor(FileProcessorStrategy):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.metadata = {}

    def process(self):
        text = self.extract_text_from_pdf(self.file_path)
        if text is not None:
            self.metadata.update({'text': text})

    @staticmethod
    def extract_text_from_pdf(file_path):
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            print(f"Error encountered while opening or processing {file_path}: {e}")
            return None


# OCR functionality: to implement