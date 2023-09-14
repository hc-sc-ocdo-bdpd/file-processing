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