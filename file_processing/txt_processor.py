from file_processor_strategy import FileProcessorStrategy
import chardet

class TextFileProcessor(FileProcessorStrategy):
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.metadata = {}

    def process(self) -> None:
        # Reads the file and updates the metadata with information about the file
        encoding = chardet.detect(open(self.file_path, "rb").read())['encoding']
        with open(self.file_path, 'r', encoding=encoding) as f:
            text = f.read()

        self.metadata.update({
            'text': text,
            'encoding': encoding,
            'num_lines': len(text.split('\n')),
            'num_words': len(text.split()),
        })