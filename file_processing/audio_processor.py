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
    def __init__(self, file_path: str, open_file: bool = True) -> None:
        super().__init__(file_path, open_file)
        self.metadata = {'message': 'File was not opened'} if not open_file else {}

    def process(self) -> None:
        if not self.open_file:
            return

        try:
            audio = File(self.file_path)
            if isinstance(audio, MP3):
                audio_tags = EasyID3(self.file_path)
                self.metadata.update({
                    'bitrate': audio.info.bitrate,
                    'length': audio.info.length,
                    'artist': audio_tags.get('artist', [''])[0],
                    'date': audio_tags.get('date', [''])[0],
                    'title': audio_tags.get('title', [''])[0],
                    'organization': audio_tags.get('organization', [''])[0]
                })
            elif isinstance(audio, (WAVE, FLAC, OggVorbis)):
                self.metadata.update({
                    'bitrate': audio.info.bitrate,
                    'length': audio.info.length,
                    'artist': audio.get('ARTIST', [''])[0],
                    'date': audio.get('DATE', [''])[0],
                    'title': audio.get('TITLE', [''])[0],
                    'organization': audio.get('ORGANIZATION', [''])[0]
                })
            elif isinstance(audio, MP4):
                self.metadata.update({
                    'bitrate': audio.info.bitrate if audio.info is not None else 0,
                    'length': audio.info.length,
                    'artist': audio.get('©ART', [''])[0],
                    'date': audio.get('©day', [''])[0],
                    'title': audio.get('©nam', [''])[0],
                    'organization': audio.get('©wrk', [''])[0]
                })
            elif isinstance(audio, AIFF):
                if audio.tags is None:
                    audio.add_tags()
                self.metadata.update({
                    'bitrate': audio.info.bitrate,
                    'length': audio.info.length,
                    'artist': audio.tags.get('artist', [''])[0],
                    'date': audio.tags.get('date', [''])[0],
                    'title': audio.tags.get('title', [''])[0],
                    'organization': audio.tags.get('organization', [''])[0]
                })
        except Exception as e:
            raise FileProcessingFailedError(f"Error encountered while processing: {e}")

    def save(self, output_path: str = None) -> None:
        save_path = output_path or self.file_path
        try:
            # Copy the file first
            main_file = open(self.file_path, "rb").read()
            dest_file = open(save_path, 'wb+')
            dest_file.write(main_file)
            dest_file.close()

            # Update the metadata of the copied file
            audio = File(save_path)

            if isinstance(audio, MP3):
                audio = EasyID3(save_path)
                audio['artist'] = self.metadata.get('artist', audio.get('artist', [''])[0])
                audio['date'] = self.metadata.get('date', audio.get('date', [''])[0])
                audio['title'] = self.metadata.get('title', audio.get('title', [''])[0])
                audio['organization'] = self.metadata.get('organization', audio.get('organization', [''])[0])
            elif isinstance(audio, MP4):
                audio['©ART'] = self.metadata.get('artist', audio.get('©ART', [''])[0])
                audio['©day'] = self.metadata.get('date', audio.get('©day', [''])[0])
                audio['©nam'] = self.metadata.get('title', audio.get('©nam', [''])[0])
                audio['©wrk'] = self.metadata.get('organization', audio.get('©wrk', [''])[0])
            elif isinstance(audio, (FLAC, OggVorbis)):
                audio['ARTIST'] = self.metadata.get('artist', audio.get('ARTIST', [''])[0])
                audio['DATE'] = self.metadata.get('date', audio.get('DATE', [''])[0])
                audio['TITLE'] = self.metadata.get('title', audio.get('TITLE', [''])[0])
                audio['ORGANIZATION'] = self.metadata.get('organization', audio.get('ORGANIZATION', [''])[0])
            elif isinstance(audio, (WAVE, AIFF)):
                print("Metadata can't be saved for WAVE or AIFF files.")
            else:
                raise FileProcessingFailedError(f"Unsupported file type for {save_path}")
            audio.save()
        except Exception as e:
            raise FileProcessingFailedError(f"Error encountered while saving to {save_path}: {e}")