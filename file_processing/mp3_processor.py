from file_processor_strategy import FileProcessorStrategy
import whisper
from errors import FileProcessingFailedError

class Mp3FileProcessor(FileProcessorStrategy):
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.metadata = {}

    def process(self) -> None:
        try:
            model = whisper.load_model('base')
            text = model.transcribe(str(self.file_path))
            self.metadata.update({
                'text': text['text'],
                'language': text['language']
            })
        except Exception as e:
            raise FileProcessingFailedError(f"Error encountered while processing: {e}")


    def save(self, output_path: str = None) -> None:
        pass