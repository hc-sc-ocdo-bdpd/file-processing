from file_processor_strategy import FileProcessorStrategy
from docx import Document
from zipfile import BadZipFile
from docx.oxml import OxmlElement
from errors import FileProcessingFailedError

class DocxFileProcessor(FileProcessorStrategy):
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.metadata = self._default_metadata()


    def _default_metadata(self) -> dict:
        return {
            'text': None,
            'author': None,
            'last_modified_by': None,
            'has_password': False
        }


    def process(self) -> None:
        try:
            doc = Document(self.file_path)
            self.metadata.update({'text': self.extract_text_from_docx(doc)})
            self.metadata.update({'author': doc.core_properties.author})
            self.metadata.update({'last_modified_by': doc.core_properties.last_modified_by})
        except BadZipFile:
            self.metadata["has_password"] = True
        except Exception as e:
            raise FileProcessingFailedError(f"Error encountered while processing {self.file_path}: {e}")

        # Other core properties to include: https://python-docx.readthedocs.io/en/latest/api/document.html#coreproperties-objects
        # keywords, language, subject, version


    def save(self, output_path: str = None) -> None:
        try:
            doc = Document(self.file_path)

            # Update the core properties (metadata)
            cp = doc.core_properties
            cp.author = self.metadata.get('author', cp.author)
            cp.last_modified_by = self.metadata.get('last_modified_by', cp.last_modified_by)
            
            save_path = output_path or self.file_path
            doc.save(save_path)
        except Exception as e:
            raise FileProcessingFailedError(f"Error encountered while saving {self.file_path}: {e}")


    @staticmethod
    def extract_text_from_docx(doc: Document) -> str:
        try:
            full_text = []
            for para in doc.paragraphs:
                full_text.append(para.text)
            return '\n'.join(full_text)
        except Exception as e:
            raise FileProcessingFailedError(f"Error encountered while opening or processing {doc}: {e}")
            return None