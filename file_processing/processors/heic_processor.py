from PIL import Image
from pillow_heif import register_heif_opener
from file_processing.file_processor_strategy import FileProcessorStrategy
from file_processing.errors import FileProcessingFailedError

register_heif_opener()  # Supports .heic, .heics, .heif, .heifs, .hif

class HeicFileProcessor(FileProcessorStrategy):
    """
    Processor for handling HEIC files, extracting metadata and saving the file.

    Attributes:
        metadata (dict): Contains metadata fields such as 'original_format', 'mode', 'width',
                         and 'height' if the file is opened.
    """

    def __init__(self, file_path: str, open_file: bool = True) -> None:
        """
        Initializes the HeicFileProcessor with the specified file path.

        Args:
            file_path (str): Path to the HEIC file to process.
            open_file (bool): Indicates whether to open and process the file immediately.

        Sets:
            metadata (dict): Populated with a message if `open_file` is False.
        """
        super().__init__(file_path, open_file)
        self.metadata = {'message': 'File was not opened'} if not open_file else {}

    def process(self) -> None:
        """
        Extracts metadata from the HEIC file, including format, mode, and dimensions.

        Raises:
            FileProcessingFailedError: If an error occurs while processing the HEIC file.
        """
        if not self.open_file:
            return

        try:
            image = Image.open(self.file_path)
            image.load()
            self.metadata.update({
                'original_format': image.format,
                'mode': image.mode,  # Mode defines type and width of a pixel
                'width': image.width,
                'height': image.height,
            })
        except Exception as e:
            raise FileProcessingFailedError(
                f"Error encountered while processing {self.file_path}: {e}"
            )

    def save(self, output_path: str = None) -> None:
        """
        Saves the HEIC file to the specified output path.

        Args:
            output_path (str): Path to save the HEIC file. If None, overwrites the original file.

        Raises:
            FileProcessingFailedError: If an error occurs while saving the HEIC file.
        """
        try:
            image = Image.open(self.file_path)

            save_path = output_path or self.file_path
            image.save(save_path)
        except Exception as e:
            raise FileProcessingFailedError(
                f"Error encountered while saving to {save_path}: {e}"
            )
