from file_processor_strategy import FileProcessorStrategy
import whisper
import wave
from errors import FileProcessingFailedError

class WavFileProcessor(FileProcessorStrategy):
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.metadata = {}

    def process(self) -> None:
        try:
            model = whisper.load_model('base')
            text = model.transcribe(str(self.file_path))
            audiofile = wave.open(self.file_path, 'rb')
            self.metadata.update({
                'text': text['text'],
                'language': text['language'],
                'duration_seconds': audiofile.getnframes() / audiofile.getframerate(),
            })
        except Exception as e:
            raise FileProcessingFailedError(f"Error encountered while processing: {e}")


    def save(self, output_path: str = None) -> None:
        try:
            save_path = output_path or self.file_path
            main_file = open(self.file_path, "rb").read()
            dest_file = open(save_path, 'wb+')
            dest_file.write(main_file)
            dest_file.close()
        except Exception as e:
            raise FileProcessingFailedError(f"Error encountered while saving to {save_path}: {e}")