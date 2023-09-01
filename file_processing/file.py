import os
from txt_processor import TextFileProcessor
from pdf_processor import PdfFileProcessor
from docx_processor import DocxFileProcessor

class File:
    def __init__(self, path):
        self.path = path
        self.processor = self._get_processor()  # Decides which processor to use
        self.process()

    def _get_processor(self):
        _, extension = os.path.splitext(self.path)
        # Choose the appropriate processor based on file extension
        if extension == ".txt":
            return TextFileProcessor(self.path)
        elif extension == ".pdf":
            return PdfFileProcessor(self.path)
        elif extension == ".docx":
            return DocxFileProcessor(self.path)
        else:
            # If no processor is available for the file type, raise an exception
            raise ValueError(f"No processor for file type {extension}")

    def process(self):
        # Processes the file using the chosen processor
        return self.processor.process()

    @property
    def file_name(self):
        return self.processor.file_name

    @property
    def metadata(self):
        return self.processor.metadata