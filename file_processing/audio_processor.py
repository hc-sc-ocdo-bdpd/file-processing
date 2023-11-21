from file_processor_strategy import FileProcessorStrategy
from mutagen import File
from errors import FileProcessingFailedError

class AudioFileProcessor(FileProcessorStrategy):
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.metadata = {}

    def process(self) -> None:
        try:
            audio = File(self.file_path)
            self.metadata.update({
                'bitrate': audio.info.bitrate,
                'duration_seconds': audio.info.length,
                'artist': audio.get('artist'),
                'date': audio.get('date'),
                'title': audio.get('title')
            })
        except Exception as e:
            raise FileProcessingFailedError(f"Error encountered while processing: {e}")

    def save(self, output_path: str = None) -> None:
        save_path = output_path or self.file_path
        try:
            audio = File(self.file_path)

            # Update the core properties (metadata)
            audio['artist'] = self.metadata.get('artist', audio.get('artist'))
            audio['date'] = self.metadata.get('date', audio.get('date'))
            audio['title'] = self.metadata.get('title', audio.get('title'))
            audio.save()

            main_file = open(self.file_path, "rb").read()
            dest_file = open(save_path, 'wb+')
            dest_file.write(main_file)
            dest_file.close()
        except Exception as e:
            raise FileProcessingFailedError(f"Error encountered while saving to {save_path}: {e}")