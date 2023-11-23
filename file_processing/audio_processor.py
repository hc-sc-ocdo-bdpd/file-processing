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
                    'bitrate': audio.info.bitrate,
                    'length': audio.info.length,
                    'author': audio_tags.get('author', [''])[0],
                    'date': audio_tags.get('date', [''])[0],
                    'title': audio_tags.get('title', [''])[0],
                    'organization': audio_tags.get('organization', [''])[0]
                })
            elif isinstance(audio, (WAVE, MP4, FLAC, AIFF, OggVorbis)):
                self.metadata.update({
                    'bitrate': audio.info.bitrate,
                    'length': audio.info.length,
                    'author': audio.get('ARTIST', [''])[0],
                    'date': audio.get('DATE', [''])[0],
                    'title': audio.get('TITLE', [''])[0],
                    'organization': audio.get('ORGANIZATION', [''])[0]
                })
        except Exception as e:
            raise FileProcessingFailedError(f"Error encountered while processing: {e}")

    def save(self, output_path: str = None) -> None:
        save_path = output_path or self.file_path
        try:
            audio = File(self.file_path)
            if isinstance(audio, MP3):
                audio = EasyID3(self.file_path)
                audio['author'] = self.metadata.get('author', audio.get('author', [''])[0])
                audio['date'] = self.metadata.get('date', audio.get('date', [''])[0])
                audio['title'] = self.metadata.get('title', audio.get('title', [''])[0])
                audio['organization'] = self.metadata.get('organization', audio.get('organization', [''])[0])
            elif isinstance(audio, (WAVE, MP4, FLAC, AIFF, OggVorbis)):
                audio['AUTHOR'] = self.metadata.get('author', audio.get('AUTHOR', [''])[0])
                audio['DATE'] = self.metadata.get('date', audio.get('DATE', [''])[0])
                audio['TITLE'] = self.metadata.get('title', audio.get('TITLE', [''])[0])
                audio['ORGANIZATION'] = self.metadata.get('organization', audio.get('ORGANIZATION', [''])[0])
            audio.save()
            with open(self.file_path, "rb") as main_file, open(save_path, 'wb+') as dest_file:
                dest_file.write(main_file.read())
                dest_file.close()
        except Exception as e:
            raise FileProcessingFailedError(f"Error encountered while saving to {save_path}: {e}")