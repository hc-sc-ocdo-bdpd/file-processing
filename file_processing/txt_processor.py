from file_processor_strategy import FileProcessorStrategy

class TextFileProcessor(FileProcessorStrategy):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.metadata = {}

    def process(self):
        # Reads the file and updates the metadata with information about the file
        with open(self.file_path, 'r') as f:
            text = f.read()
            lines = text.split('\n')
            words = text.split()

        self.metadata.update({
            'text': text,
            'lines': lines,
            'words': words,
            'num_lines': len(lines),
            'num_words': len(words),
        })