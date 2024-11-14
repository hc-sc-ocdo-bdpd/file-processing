from PIL import Image
from file_processing.file_processor_strategy import FileProcessorStrategy
from file_processing.errors import FileProcessingFailedError

class GifFileProcessor(FileProcessorStrategy):
    """
    Processor for handling GIF files, extracting metadata and saving the file.

    Attributes:
        metadata (dict): Contains metadata fields such as 'original_format', 'mode', 'width',
                         'height', 'animated', and 'frames' if the file is opened.
    """

    def __init__(self, file_path: str, open_file: bool = True) -> None:
        """
        Initializes the GifFileProcessor with the specified file path.

        Args:
            file_path (str): Path to the GIF file to process.
            open_file (bool): Indicates whether to open and process the file immediately.

        Sets:
            metadata (dict): Populated with a message if `open_file` is False.
        """
        super().__init__(file_path, open_file)
        self.metadata = {'message': 'File was not opened'} if not open_file else {}

    def process(self) -> None:
        """
        Extracts metadata from the GIF file, including format, mode, dimensions, and animation details.

        Raises:
            FileProcessingFailedError: If an error occurs while processing the GIF file.
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
                'animated': image.is_animated,
                'frames': image.n_frames
            })
        except Exception as e:
            raise FileProcessingFailedError(
                f"Error encountered while processing {self.file_path}: {e}"
            )

    def save(self, output_path: str = None) -> None:
        """
        Saves the GIF file to the specified output path, preserving all frames if animated.

        Args:
            output_path (str): Path to save the GIF file. If None, overwrites the original file.

        Raises:
            FileProcessingFailedError: If an error occurs while saving the GIF file.
        """
        try:
            image = Image.open(self.file_path)
            save_path = output_path or self.file_path
            image.save(save_path, save_all=True)
        except Exception as e:
            raise FileProcessingFailedError(
                f"Error encountered while saving to {save_path}: {e}"
            )