import chardet
import re
from file_processing.errors import FileProcessingFailedError
from file_processing.file_processor_strategy import FileProcessorStrategy

class JsFileProcessor(FileProcessorStrategy):
    """
    Processor for handling JavaScript (.js) source files, extracting metadata and content.

    Attributes:
        metadata (dict): Contains metadata such as 'text', 'encoding', 'num_lines',
                         'num_functions', 'num_classes', and 'num_comments'.
    """

    def __init__(self, file_path: str, open_file: bool = True) -> None:
        super().__init__(file_path, open_file)
        self.metadata = {'message': 'File was not opened'} if not open_file else {}

    def process(self) -> None:
        """Extracts JavaScript file metadata if open_file is True."""
        if not self.open_file:
            return
        try:
            raw_data = open(self.file_path, 'rb').read()
            encoding = chardet.detect(raw_data)['encoding'] or 'utf-8'

            # Read using the detected (or fallback) encoding
            with open(self.file_path, 'r', encoding=encoding, errors='replace') as f:
                text = f.read()

            num_lines = len(text.splitlines())

            # Basic regex patterns:
            # Matches 'function foo(...) { ... }' or 'export function foo(...) { ... }'
            function_pattern = re.compile(r'\b(function|export\s+function)\s+[A-Za-z_]\w*\s*\(.*?\)\s*\{')

            # Matches 'class SomeClass { ... }'
            class_pattern = re.compile(r'\bclass\s+[A-Za-z_]\w*\s*\{?')

            # Matches single-line (// ...) and multi-line (/* ... */) comments
            comment_pattern = re.compile(r'(//[^\n]*|/\*.*?\*/)', re.DOTALL)

            num_functions = len(function_pattern.findall(text))
            num_classes = len(class_pattern.findall(text))
            num_comments = len(comment_pattern.findall(text))

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
        """Saves the JavaScript file to the specified path."""
        try:
            save_path = output_path or self.file_path
            with open(save_path, 'w', encoding=self.metadata['encoding']) as f:
                f.write(self.metadata['text'])
        except Exception as e:
            raise FileProcessingFailedError(
                f"Error saving {self.file_path} to {save_path}: {e}"
            )
