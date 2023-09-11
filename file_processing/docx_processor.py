from file_processor_strategy import FileProcessorStrategy
from docx import Document

class DocxFileProcessor(FileProcessorStrategy):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.metadata = {}

    def process(self):
        doc = Document(self.file_path)
        self.metadata.update({'text': self.extract_text_from_docx(doc)})
        self.metadata.update({'author': doc.core_properties.author})
        self.metadata.update({'last_modified_by': doc.core_properties.last_modified_by})

    @staticmethod
    def extract_text_from_docx(doc: Document):
        try:
            full_text = []
            for para in doc.paragraphs:
                full_text.append(para.text)
            return '\n'.join(full_text)
        except Exception as e:
            print(f"Error encountered while opening or processing {file_path}: {e}")
            return None