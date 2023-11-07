from file_processor_strategy import FileProcessorStrategy
import whisper
import eyed3
from errors import FileProcessingFailedError

class Mp3FileProcessor(FileProcessorStrategy):
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.metadata = {}

    def process(self) -> None:
        try:
            model = whisper.load_model('base')
            text = model.transcribe(str(self.file_path))
            audiofile = eyed3.load(self.file_path)
            self.metadata.update({
                'text': text['text'],
                'language': text['language'],
                'duration_seconds': audiofile.info.time_secs,
                'title': audiofile.tag.title,
                'artist': audiofile.tag.artist                
            })
        except Exception as e:
            raise FileProcessingFailedError(f"Error encountered while processing: {e}")


    def save(self, output_path: str = None) -> None:
        try:
            audiofile = eyed3.load(self.file_path)

            # Update the core properties (metadata)
            audiofile.tag.title = self.metadata.get('title', audiofile.tag.title)
            audiofile.tag.artist = self.metadata.get('artist', audiofile.tag.artist)
            audiofile.tag.save()
            
            save_path = output_path or self.file_path

            main_file = open(self.file_path, "rb").read()
            dest_file = open(save_path, 'wb+')
            dest_file.write(main_file)
            dest_file.close()
        except Exception as e:
            raise FileProcessingFailedError(f"Error encountered while saving to {save_path}: {e}")