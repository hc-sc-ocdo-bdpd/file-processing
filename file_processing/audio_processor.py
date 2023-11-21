from file_processor_strategy import FileProcessorStrategy
from mutagen import File
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.oggvorbis import OggVorbis
from mutagen.aiff import AIFF
from mutagen.wave import WAVE
from mutagen.mp4 import MP4
from errors import FileProcessingFailedError

class AudioFileProcessor(FileProcessorStrategy):
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.metadata = {}

    def process(self) -> None:
        try:
            audio = File(self.file_path)
            if isinstance(audio, MP3):
                audio_tags = EasyID3(self.file_path)
                self.metadata.update({
                    'length': audio.info.length,
                    'artist': audio_tags.get('artist', [''])[0],
                    'date': audio_tags.get('date', [''])[0],
                    'title': audio_tags.get('title', [''])[0]
                })
            elif isinstance(audio, (FLAC, OggVorbis, AIFF, WAVE, MP4)):
                self.metadata.update({
                    'length': audio.info.length,
                    'artist': audio.get('ARTIST', [''])[0],
                    'date': audio.get('DATE', [''])[0],
                    'title': audio.get('TITLE', [''])[0]
                })
        except Exception as e:
            raise FileProcessingFailedError(f"Error encountered while processing: {e}")

    def save(self, output_path: str = None) -> None:
        save_path = output_path or self.file_path
        try:
            audio = File(self.file_path)
            if isinstance(audio, MP3):
                audio = EasyID3(self.file_path)
                audio['artist'] = self.metadata.get('artist', audio.get('artist', [''])[0])
                audio['date'] = self.metadata.get('date', audio.get('date', [''])[0])
                audio['title'] = self.metadata.get('title', audio.get('title', [''])[0])
            elif isinstance(audio, (FLAC, OggVorbis, AIFF, WAVE, MP4)):
                audio['ARTIST'] = self.metadata.get('artist', audio.get('ARTIST', [''])[0])
                audio['DATE'] = self.metadata.get('date', audio.get('DATE', [''])[0])
                audio['TITLE'] = self.metadata.get('title', audio.get('TITLE', [''])[0])
            audio.save()
            main_file = open(self.file_path, "rb").read()
            dest_file = open(save_path, 'wb+')
            dest_file.write(main_file)
            dest_file.close()
        except Exception as e:
            raise FileProcessingFailedError(f"Error encountered while saving to {save_path}: {e}")