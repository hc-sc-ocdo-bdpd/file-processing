from file_processor_strategy import FileProcessorStrategy
from PyPDF2 import PdfReader, PdfWriter

class PdfFileProcessor(FileProcessorStrategy):
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.metadata = self._default_metadata()
        self.reader = None


    def _default_metadata(self) -> dict:
        return {
            'text': None,
            'has_password': False
        }


    def process(self) -> None:
        reader = PdfReader(self.file_path)

        if not reader.is_encrypted:
            self.metadata.update({'text': self.extract_text_from_pdf(self.file_path, reader)})
        else:
            self.metadata['has_password'] = True
    
    def save(self, output_path: str = None) -> None:
        output_path = output_path or self.file_path

        pdf_read = PdfReader(self.file_path)
        pdf = PdfWriter(self.file_path)

        for page in range(len(pdf_read.pages)):
            # Add each page to the writer object
            pdf.add_page(pdf_read.pages[page])

        with open(output_path, 'wb') as output_pdf:
            pdf.write(output_pdf)

    @staticmethod
    def extract_text_from_pdf(file_path: str, reader: PdfReader) -> str:
        try:
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            print(f"Error encountered while extracting text {file_path}: {e}")
            return None
        