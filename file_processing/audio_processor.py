from file_processor_strategy import FileProcessorStrategy
from mutagen import File
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.oggvorbis import OggVorbis
from mutagen.aiff import AIFF
from mutagen.wavpack import WavPack
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
                audio = EasyID3(self.file_path)
                self.metadata.update({
                    'bitrate': audio.info.bitrate,
                    'length': audio.info.length,
                    'artist': audio.get('artist', ''),
                    'date': audio.get('date', ''),
                    'title': audio.get('title', '')
                })
            elif isinstance(audio, (FLAC, OggVorbis, AIFF, WavPack, MP4)):
                self.metadata.update({
                    'length': audio.info.length,
                    'artist': audio.get('ARTIST', ''),
                    'date': audio.get('DATE', ''),
                    'title': audio.get('TITLE', '')
                })
        except Exception as e:
            raise FileProcessingFailedError(f"Error encountered while processing: {e}")

    def save(self, output_path: str = None) -> None:
        save_path = output_path or self.file_path
        try:
            audio = File(self.file_path)
            if isinstance(audio, MP3):
                audio = EasyID3(self.file_path)
                audio['artist'] = self.metadata.get('artist', audio.get('artist', ''))
                audio['date'] = self.metadata.get('date', audio.get('date', ''))
                audio['title'] = self.metadata.get('title', audio.get('title', ''))
            elif isinstance(audio, (FLAC, OggVorbis, AIFF, WavPack, MP4)):
                audio['ARTIST'] = self.metadata.get('artist', audio.get('ARTIST', ''))
                audio['DATE'] = self.metadata.get('date', audio.get('DATE', ''))
                audio['TITLE'] = self.metadata.get('title', audio.get('TITLE', ''))
            audio.save()
            main_file = open(self.file_path, "rb").read()
            dest_file = open(save_path, 'wb+')
            dest_file.write(main_file)
            dest_file.close()
        except Exception as e:
            raise FileProcessingFailedError(f"Error encountered while saving to {save_path}: {e}")