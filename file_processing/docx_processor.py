from file_processor_strategy import FileProcessorStrategy
from docx import Document
from zipfile import ZipFile
from zipfile import BadZipFile

class DocxFileProcessor(FileProcessorStrategy):
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.metadata = {}

    def process(self) -> None:
        try:
            with ZipFile(self.file_path) as zf:
                doc = Document(self.file_path)
                self.metadata.update({'text': self.extract_text_from_docx(doc)})
                self.metadata.update({'author': doc.core_properties.author})
                self.metadata.update({'last_modified_by': doc.core_properties.last_modified_by})
        except BadZipFile:
            raise

        # Other core properties to include: https://python-docx.readthedocs.io/en/latest/api/document.html#coreproperties-objects
        # keywords, language, subject, version

    @staticmethod
    def extract_text_from_docx(doc: Document) -> str:
        try:
            full_text = []
            for para in doc.paragraphs:
                full_text.append(para.text)
            return '\n'.join(full_text)
        except Exception as e:
            print(f"Error encountered while opening or processing {file_path}: {e}")
            return None