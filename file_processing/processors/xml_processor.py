import chardet
from file_processing.errors import FileProcessingFailedError
from file_processing.file_processor_strategy import FileProcessorStrategy

class XmlFileProcessor(FileProcessorStrategy):
    """
    Processor for handling XML files, extracting metadata such as encoding, text content,
    line count, word count, and individual lines and words.

    Attributes:
        metadata (dict): Contains metadata fields such as 'text', 'encoding', 'lines', 'words',
                         'num_lines', and 'num_words' if the file is opened.
    """

    def __init__(self, file_path: str, open_file: bool = True) -> None:
        """
        Initializes the XmlFileProcessor with the specified file path.

        Args:
            file_path (str): Path to the XML file to process.
            open_file (bool): Indicates whether to open and process the file immediately.

        Sets:
            metadata (dict): Populated with a message if `open_file` is False, otherwise initialized as empty.
        """
        super().__init__(file_path, open_file)
        self.metadata = {'message': 'File was not opened'} if not open_file else {}

    def process(self) -> None:
        """
        Extracts metadata from the XML file, including encoding, text content, line count,
        word count, individual lines, and words.

        Raises:
            FileProcessingFailedError: If an error occurs while processing the XML file.
        """
        if not self.open_file:
            return

        try:
            # Detect encoding and read content
            encoding = chardet.detect(
                open(self.file_path, "rb").read())['encoding']
            with open(self.file_path, 'r', encoding=encoding) as f:
                text = f.read()
                lines = text.split('\n')
                words = text.split()

            # Update metadata with extracted values
            self.metadata.update({
                'text': text,
                'encoding': encoding,
                'lines': lines,
                'words': words,
                'num_lines': len(lines),
                'num_words': len(words),
            })
        except Exception as e:
            raise FileProcessingFailedError(
                f"Error encountered while processing {self.file_path}: {e}"
            )

    def save(self, output_path: str = None) -> None:
        """
        Saves the XML file with the extracted metadata to the specified output path.

        Args:
            output_path (str): Path to save the XML file. If None, overwrites the original file.

        Raises:
            FileProcessingFailedError: If an error occurs while saving the XML file.
        """
        try:
            save_path = output_path or self.file_path
            with open(save_path, 'w', encoding=self.metadata['encoding']) as f:
                f.write(self.metadata['text'])
        except Exception as e:
            raise FileProcessingFailedError(
                f"Error encountered while saving {self.file_path}: {e}"
            )
