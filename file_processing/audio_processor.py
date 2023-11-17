from file_processor_strategy import FileProcessorStrategy
import audio_metadata
from errors import FileProcessingFailedError

class AudioFileProcessor(FileProcessorStrategy):
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.metadata = {}

    def process(self) -> None:
        try:
            metadata = audio_metadata.load(self.file_path)
            self.metadata.update({
                'bitrate': metadata.streaminfo.bitrate,
                'duration': metadata.streaminfo.duration,
                'artist': getattr(metadata.tags, 'artist', None),
                'date': getattr(metadata.tags, 'date', None),
                'title': getattr(metadata.tags, 'title', None),
            })
        except Exception as e:
            raise FileProcessingFailedError(f"Error encountered while processing: {e}")


    def save(self, output_path: str = None) -> None:
        try:
            metadata = audio_metadata.load(self.file_path)

            #Update the core metadata
            metadata.tags.artist = self.metadata.get('artist', metadata.tags.artist)
            metadata.tags.date = self.metadata.get('date', metadata.tags.date)    
            metadata.tags.title = self.metadata.get('title', metadata.tags.title)
            metadata.tags.save()

            save_path = output_path or self.file_path

            main_file = open(self.file_path, "rb").read()
            dest_file = open(save_path, 'wb+')
            dest_file.write(main_file)
            dest_file.close()
        except Exception as e:
            raise FileProcessingFailedError(f"Error encountered while saving to {save_path}: {e}")