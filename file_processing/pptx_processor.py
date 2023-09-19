from file_processor_strategy import FileProcessorStrategy
from pptx import Presentation

class PptxFileProcessor(FileProcessorStrategy):
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.metadata = {}

    def process(self) -> None:
        ppt = Presentation(self.file_path)
        self.metadata.update({'text': self.extract_text_from_pptx(ppt)})
        self.metadata.update({'author': ppt.core_properties.author})
        self.metadata.update({'last_modified_by': ppt.core_properties.last_modified_by})

        # Other core properties to include: https://python-docx.readthedocs.io/en/latest/api/document.html#coreproperties-objects
        # keywords, language, subject, version

    @staticmethod
    def extract_text_from_pptx(ppt: Presentation) -> str:
        try:
            full_text = []
            for slide in ppt.slides:
                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        full_text.append(shape.text)
            return '\n'.join(full_text)
        except Exception as e:
            print(f"Error encountered while opening or processing {file_path}: {e}")
            return None