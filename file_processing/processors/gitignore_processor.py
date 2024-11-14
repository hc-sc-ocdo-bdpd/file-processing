import chardet
from file_processing.errors import FileProcessingFailedError
from file_processing.file_processor_strategy import FileProcessorStrategy

class GitignoreFileProcessor(FileProcessorStrategy):
    """
    Processor for handling .gitignore files, extracting metadata such as text content, encoding,
    line count, and word count.

    Attributes:
        metadata (dict): Contains metadata fields such as 'text', 'encoding', 'lines', 'words',
                         'num_lines', and 'num_words' if the file is opened.
    """

    def __init__(self, file_path: str, open_file: bool = True) -> None:
        """
        Initializes the GitignoreFileProcessor with the specified file path.

        Args:
            file_path (str): Path to the .gitignore file to process.
            open_file (bool): Indicates whether to open and process the file immediately.

        Sets:
            metadata (dict): Populated with a message if `open_file` is False.
        """
        super().__init__(file_path, open_file)
        self.metadata = {'message': 'File was not opened'} if not open_file else {}

    def process(self) -> None:
        """
        Extracts metadata from the .gitignore file, including text content, encoding, lines, words,
        line count, and word count.

        Raises:
            FileProcessingFailedError: If an error occurs during .gitignore file processing.
            UnicodeDecodeError: If there is a decoding error when reading the file.
        """
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
                f"Unicode decoding error encountered while processing {self.file_path}: {ude}"
            )
        except Exception as e:
            raise FileProcessingFailedError(
                f"Error encountered while processing {self.file_path}: {e}"
            )

    def save(self, output_path: str = None) -> None:
        """
        Saves the .gitignore file to the specified output path with updated metadata.

        Args:
            output_path (str): Path to save the file. If None, overwrites the original file.

        Raises:
            FileProcessingFailedError: If an error occurs while saving the .gitignore file.
        """
        try:
            encoding = self.metadata.get('encoding', 'utf-8')  # Default to 'utf-8'
            save_path = output_path or self.file_path
            with open(save_path, 'w', encoding=encoding) as f:
                f.write(self.metadata['text'])
        except Exception as e:
            raise FileProcessingFailedError(
                f"Error encountered while saving {self.file_path}: {e}"
            )
