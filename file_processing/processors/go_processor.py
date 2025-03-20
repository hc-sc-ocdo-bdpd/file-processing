import chardet
import re
from file_processing.errors import FileProcessingFailedError
from file_processing.file_processor_strategy import FileProcessorStrategy

class GoFileProcessor(FileProcessorStrategy):
    """
    Processor for handling Go source files (.go), extracting metadata and content.

    Attributes:
        metadata (dict): Contains metadata such as 'text', 'encoding', 'num_lines',
                         'num_functions', 'num_structs', and 'num_interfaces'.
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

            with open(self.file_path, 'r', encoding=encoding) as f:
                text = f.read()

                num_lines = len(text.splitlines())

                num_functions = len(re.findall(r'\bfunc\s+\w+\s*\(', text))
                num_structs = len(re.findall(r'\btype\s+\w+\s+struct\s*\{', text))
                num_interfaces = len(re.findall(r'\btype\s+\w+\s+interface\s*\{', text))

                self.metadata.update({
                    'text': text,
                    'encoding': encoding,
                    'num_lines': num_lines,
                    'num_functions': num_functions,
                    'num_structs': num_structs,
                    'num_interfaces': num_interfaces
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