from pathlib import Path
import shutil
from file_processing.errors import FileProcessingFailedError
from file_processing.file_processor_strategy import FileProcessorStrategy
import re

class MarkdownFileProcessor(FileProcessorStrategy):
    def __init__(self, file_path: str, open_file: bool = True) -> None:
        super().__init__(file_path, open_file)
        self.metadata = {'message': 'File was not opened'} if not open_file else {}

    def process(self) -> None:
        if not self.open_file:
            return

        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            self.metadata.update({
                "num_headings": self.count_headings(content),
                "num_links": self.count_links(content),
                "num_code_blocks": self.count_code_blocks(content),
                "text_length": len(content),
                "num_lines": content.count('\n') + 1,
                "num_words": len(content.split())
            })
        except Exception as e:
            raise FileProcessingFailedError(
                f"Error encountered while processing {self.file_path}: {e}")

    @staticmethod
    def count_headings(content):
        return len(re.findall(r'^(#{1,6})\s', content, re.MULTILINE))

    @staticmethod
    def count_links(content):
        return len(re.findall(r'\[.*?\]\(.*?\)', content))

    @staticmethod
    def count_code_blocks(content):
        return len(re.findall(r'```.*?```', content, re.DOTALL))

    def save(self, output_path: str = None) -> None:
        try:
            output_path = output_path or str(self.file_path)
            shutil.copy2(self.file_path, output_path)
        except Exception as e:
            raise FileProcessingFailedError(
                f"Error encountered while saving {self.file_path}: {e}")
