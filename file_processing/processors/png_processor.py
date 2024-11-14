from PIL import Image
from file_processing.errors import FileProcessingFailedError
from file_processing.file_processor_strategy import FileProcessorStrategy

class PngFileProcessor(FileProcessorStrategy):
    """
    Processor for handling PNG files, extracting metadata such as image format, mode,
    dimensions, and saving the file.

    Attributes:
        metadata (dict): Contains metadata fields such as 'original_format', 'mode', 'width',
                         and 'height' if the file is opened.
    """

    def __init__(self, file_path: str, open_file: bool = True) -> None:
        """
        Initializes the PngFileProcessor with the specified file path.

        Args:
            file_path (str): Path to the PNG file to process.
            open_file (bool): Indicates whether to open and process the file immediately.

        Sets:
            metadata (dict): Populated with a message if `open_file` is False, otherwise initialized as empty.
        """
        super().__init__(file_path, open_file)
        self.metadata = {'message': 'File was not opened'} if not open_file else {}

    def process(self) -> None:
        """
        Extracts metadata from the PNG file, including format, mode, width, and height.

        Raises:
            FileProcessingFailedError: If an error occurs while processing the PNG file.
        """
        if not self.open_file:
            return

        try:
            image = Image.open(self.file_path)
            image.load()
            # Populate metadata with extracted image properties
            self.metadata.update({
                'original_format': image.format,
                'mode': image.mode,  # Mode defines pixel type and width
                'width': image.width,
                'height': image.height,
            })
        except Exception as e:
            raise FileProcessingFailedError(
                f"Error encountered while processing {self.file_path}: {e}"
            )

    def save(self, output_path: str = None) -> None:
        """
        Saves the PNG file to the specified output path.

        Args:
            output_path (str): Path to save the PNG file. If None, overwrites the original file.

        Raises:
            FileProcessingFailedError: If an error occurs while saving the PNG file.
        """
        try:
            image = Image.open(self.file_path)
            save_path = output_path or self.file_path
            image.save(save_path)
        except Exception as e:
            raise FileProcessingFailedError(
                f"Error encountered while saving to {save_path}: {e}"
            )
