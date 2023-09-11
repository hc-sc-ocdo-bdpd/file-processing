from file_processor_strategy import FileProcessorStrategy
from docx import Document

class DocxFileProcessor(FileProcessorStrategy):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.metadata = {}

    def process(self):
        text = self.extract_text_from_docx(self.file_path)
        self.metadata.update({'text': text})

    @staticmethod
    def extract_text_from_docx(file_path):
        try:
            doc = Document(file_path)
            full_text = []
            for para in doc.paragraphs:
                full_text.append(para.text)
            return '\n'.join(full_text)
        except Exception as e:
            print(f"Error encountered while opening or processing {file_path}: {e}")
            return None