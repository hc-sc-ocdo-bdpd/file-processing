import chardet
from file_processing.errors import FileProcessingFailedError
from file_processing.file_processor_strategy import FileProcessorStrategy

class JavaFileProcessor(FileProcessorStrategy):
    """
    Processor for handling Java files (.java), extracting source code metadata and content.

    Attributes:
        metadata (dict): Contains extracted metadata such as 'text', 'encoding',
                         'num_lines', 'num_characters', 'num_methods', and 'num_classes'.
    """

    def __init__(self, file_path: str, open_file: bool = True) -> None:
        """
        Initializes the JavaFileProcessor with the specified file path.

        Args:
            file_path (str): Path to the Java file to process.
            open_file (bool): Indicates whether to open and process the file immediately.

        Sets:
            metadata (dict): Populated with 'message' if `open_file` is False.
        """
        super().__init__(file_path, open_file)
        self.metadata = {'message': 'File was not opened'} if not open_file else {}

    def process(self) -> None:
        """
        Extracts metadata from the Java source file if it is open and accessible.

        Metadata extracted includes the source text, file encoding, number of lines,
        number of characters, number of methods, and number of classes.

        Raises:
            FileProcessingFailedError: If an error occurs during Java file processing.
        """
        if not self.open_file:
            return
        try:
            raw_data = open(self.file_path, 'rb').read()
            encoding = chardet.detect(raw_data)['encoding']

            with open(self.file_path, 'r', encoding=encoding) as f:
                text = f.read()

                num_lines = len(text.splitlines())
                num_characters = len(text)

                # Simple method/class counting using regex patterns
                import re
                method_pattern = re.compile(r'\b(public|private|protected|static|\s)+\s+\w+\s+\w+\s*\([^\)]*\)\s*\{', re.MULTILINE)
                class_pattern = re.compile(r'\b(class|interface|enum)\s+\w+', re.MULTILINE)

                num_methods = len(method_pattern.findall(text))
                num_classes = len(class_pattern.findall(text))

                self.metadata.update({
                    'text': text,
                    'encoding': encoding,
                    'num_lines': num_lines,
                    'num_characters': num_characters,
                    'num_methods': num_methods,
                    'num_classes': num_classes,
                })
        except Exception as e:
            raise FileProcessingFailedError(
                f"Error encountered while processing {self.file_path}: {e}"
            )

    def save(self, output_path: str = None) -> None:
        """
        Saves the processed Java file to the specified output path with current metadata.

        Args:
            output_path (str): Path to save the processed Java file. If None, overwrites the original file.

        Raises:
            FileProcessingFailedError: If an error occurs while saving the Java file.
        """
        try:
            save_path = output_path or self.file_path
            with open(save_path, 'w', encoding=self.metadata['encoding']) as f:
                f.write(self.metadata['text'])
        except Exception as e:
            raise FileProcessingFailedError(
                f"Error encountered while saving file {self.file_path} to {save_path}: {e}"
            )
