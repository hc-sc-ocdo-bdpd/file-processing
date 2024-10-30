import chardet
from file_processing.errors import FileProcessingFailedError
from file_processing.file_processor_strategy import FileProcessorStrategy
import os
from unittest.mock import patch
import pytest
from file_processing_test_data import get_test_files_path

class GitignoreFileProcessor(FileProcessorStrategy):
    def __init__(self, file_path: str, open_file: bool = True) -> None:
        super().__init__(file_path, open_file)
        self.metadata = {'message': 'File was not opened'} if not open_file else {}

    def process(self) -> None:
        if not self.open_file:
            return

        try:
            with open(self.file_path, "rb") as f:
                encoding = chardet.detect(f.read())['encoding']
                
            with open(self.file_path, 'r', encoding=encoding) as f:
                text = f.read()
                lines = text.split('\n')
                words = text.split()

            self.metadata.update({
                'text': text,
                'encoding': encoding,
                'lines': lines,
                'words': words,
                'num_lines': len(lines),
                'num_words': len(words),
            })
        except UnicodeDecodeError as ude:
            raise FileProcessingFailedError(
                f"Unicode decoding error encountered while processing {self.file_path}: {ude}")
        except Exception as e:
            raise FileProcessingFailedError(
                f"Error encountered while processing {self.file_path}: {e}")

    def save(self, output_path: str = None) -> None:
        try:
            encoding = self.metadata.get('encoding', 'utf-8')  # Default to 'utf-8'
            save_path = output_path or self.file_path
            with open(save_path, 'w', encoding=encoding) as f:
                f.write(self.metadata['text'])
        except Exception as e:
            raise FileProcessingFailedError(
                f"Error encountered while saving {self.file_path}: {e}")

# Test variables
test_files_path = get_test_files_path()
variable_names = "path, text_length, num_lines, num_words"
values = [
    (test_files_path / 'Python.gitignore', 3132, 162, 403),
    (test_files_path / 'tensorflow.gitignore', 938, 52, 52)
]

@pytest.mark.parametrize(variable_names, values)
def test_gitignore_metadata(path, text_length, num_lines, num_words):
    file_obj = GitignoreFileProcessor(path)
    file_obj.process()
    assert len(file_obj.metadata['text']) == text_length
    assert file_obj.metadata['num_lines'] == num_lines
    assert file_obj.metadata['num_words'] == num_words