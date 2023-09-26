from file_processor_strategy import FileProcessorStrategy
from PIL import Image

class PngFileProcessor(FileProcessorStrategy):
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.metadata = {}

    def process(self) -> None:
        image = Image.open(self.file_path)
        image.load()
        self.metadata.update({
            'original_format': image.format,
            # mode defines type and width of a pixel (https://pillow.readthedocs.io/en/stable/handbook/concepts.html#concept-modes)
            'mode': image.mode,
            'width': image.width,
            'height': image.height,
        })