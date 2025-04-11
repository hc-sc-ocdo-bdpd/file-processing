import chardet
import re
from file_processing.errors import FileProcessingFailedError
from file_processing.file_processor_strategy import FileProcessorStrategy

class CppFileProcessor(FileProcessorStrategy):
    """
    Processor for handling C++ source files (.cpp, .cc), extracting metadata and content.

    Attributes:
        metadata (dict): Contains metadata such as 'text', 'encoding', 'num_lines',
                         'num_functions', 'num_classes', and 'num_comments'.
    """

    def __init__(self, file_path: str, open_file: bool = True) -> None:
        super().__init__(file_path, open_file)
        self.metadata = {'message': 'File was not opened'} if not open_file else {}

    def process(self) -> None:
        if not self.open_file:
            return
        try:
            raw_data = open(self.file_path, 'rb').read()
            encoding = chardet.detect(raw_data)['encoding'] or 'utf-8'

            with open(self.file_path, 'r', encoding=encoding, errors='replace') as f:
                text = f.read()

                num_lines = len(text.splitlines())

                num_functions = len(re.findall(r'\b[a-zA-Z_]\w*\s+[a-zA-Z_]\w*\s*\(.*?\)\s*\{', text))
                num_classes = len(re.findall(r'\bclass\s+\w+', text))
                num_comments = len(re.findall(r'(//[^\n]*|/\*.*?\*/)', text, re.DOTALL))

                self.metadata.update({
                    'text': text,
                    'encoding': encoding,
                    'num_lines': num_lines,
                    'num_functions': num_functions,
                    'num_classes': num_classes,
                    'num_comments': num_comments
                })

        except Exception as e:
            raise FileProcessingFailedError(
                f"Error processing {self.file_path}: {e}"
            )

    def save(self, output_path: str = None) -> None:
        try:
            save_path = output_path or self.file_path
            with open(save_path, 'w', encoding=self.metadata['encoding']) as f:
                f.write(self.metadata['text'])
        except Exception as e:
            raise FileProcessingFailedError(
                f"Error saving {self.file_path} to {save_path}: {e}"
            )