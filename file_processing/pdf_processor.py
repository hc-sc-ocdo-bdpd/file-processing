from file_processor_strategy import FileProcessorStrategy
from PyPDF2 import PdfReader
from zipfile import ZipFile
from zipfile import BadZipFile

class PdfFileProcessor(FileProcessorStrategy):
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.metadata = {}

    def process(self) -> None:
        try:
            with ZipFile(self.file_path) as zf:
                text = self.extract_text_from_pdf(self.file_path)
                self.metadata.update({'text': text})
        except BadZipFile:
            raise

    @staticmethod
    def extract_text_from_pdf(file_path: str) -> str:
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            print(f"Error encountered while opening or processing {file_path}: {e}")
            return None