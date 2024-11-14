import chardet
from file_processing.file_processor_strategy import FileProcessorStrategy
from file_processing.errors import FileProcessingFailedError

# Beautiful Soup is commonly used for parsing HTML/XML data:
# https://beautiful-soup-4.readthedocs.io/en/latest/

class HtmlFileProcessor(FileProcessorStrategy):
    """
    Processor for handling HTML files, extracting text content and metadata such as encoding,
    line count, and word count.

    Attributes:
        metadata (dict): Contains metadata fields including 'text', 'encoding', 'lines', 'words',
                         'num_lines', and 'num_words' if the file is opened.
    """

    def __init__(self, file_path: str, open_file: bool = True) -> None:
        """
        Initializes the HtmlFileProcessor with the specified file path.

        Args:
            file_path (str): Path to the HTML file to process.
            open_file (bool): Indicates whether to open and process the file immediately.

        Sets:
            metadata (dict): Populated with a message if `open_file` is False, otherwise initialized as empty.
        """
        super().__init__(file_path, open_file)
        self.metadata = {'message': 'File was not opened'} if not open_file else {}

    def process(self) -> None:
        """
        Extracts metadata from the HTML file, including text content, encoding, line count, 
        and word count.

        Raises:
            FileProcessingFailedError: If an error occurs during HTML file processing.
        """
        if not self.open_file:
            return

        try:
            # Detect file encoding for accurate text processing
            encoding = chardet.detect(open(self.file_path, "rb").read())['encoding']
            with open(self.file_path, 'r', encoding=encoding) as f:
                text = f.read()
                lines = text.split('\n')
                words = text.split()

            # Populate metadata with extracted content and counts
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
                f"Error encountered while processing: {e}"
            )

    def save(self, output_path: str = None) -> None:
        """
        Saves the HTML file with updated metadata to the specified output path.

        Args:
            output_path (str): Path to save the processed HTML file. If None, overwrites the original file.

        Raises:
            FileProcessingFailedError: If an error occurs while saving the HTML file.
        """
        try:
            # Retrieve encoding from metadata, default to 'utf-8' if unspecified
            save_path = output_path or self.file_path
            with open(save_path, 'w', encoding=self.metadata.get('encoding', 'utf-8')) as f:
                f.write(self.metadata['text'])
        except Exception as e:
            raise FileProcessingFailedError(
                f"Error encountered while saving: {e}"
            )
