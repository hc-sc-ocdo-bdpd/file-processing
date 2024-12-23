from mutagen import File
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.oggvorbis import OggVorbis
from mutagen.aiff import AIFF
from mutagen.wave import WAVE
from mutagen.mp4 import MP4
from file_processing.errors import FileProcessingFailedError
from file_processing.file_processor_strategy import FileProcessorStrategy

class AudioFileProcessor(FileProcessorStrategy):
    """
    Processor for handling audio files, extracting and saving metadata for supported file types.

    Attributes:
        metadata (dict): Contains metadata fields such as 'bitrate', 'length', 'artist', 'date', 'title',
                         and 'organization' if the file is opened and supported.
    """

    def __init__(self, file_path: str, open_file: bool = True) -> None:
        """
        Initializes the AudioFileProcessor with the specified file path.

        Args:
            file_path (str): Path to the audio file to process.
            open_file (bool): Indicates whether to open and process the file immediately.

        Sets:
            metadata (dict): Populated with 'message' if `open_file` is False.
        """
        super().__init__(file_path, open_file)
        self.metadata = {'message': 'File was not opened'} if not open_file else {}

    def process(self) -> None:
        """
        Extracts metadata from the audio file if it is open and supported.

        For MP3 files, uses ID3 tags for metadata extraction. Other audio types like WAVE, FLAC, OggVorbis, and MP4
        are handled with appropriate tag formats. Metadata extracted includes bitrate, length, artist, date, title,
        and organization.

        Raises:
            FileProcessingFailedError: If an error occurs during metadata extraction.
        """
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
        """
        Saves updated metadata to the audio file if the file format supports metadata updates.

        Supported formats for metadata saving include MP3, MP4, FLAC, and OggVorbis. WAVE and AIFF formats
        do not support saving metadata and will raise an error. For MP3 files, ID3 tags are used.

        Args:
            output_path (str): Path to save the file with updated metadata. If None, overwrites the original file.

        Raises:
            FileProcessingFailedError: If an error occurs while saving metadata or if the file type does not
                                       support metadata updates.
        """
        save_path = output_path or self.file_path
        if self.extension in [".mp3", ".mp4", ".flac", ".ogg"]:
            try:
                # Copy the file first
                main_file = open(self.file_path, "rb").read()
                with open(save_path, 'wb+') as dest_file:
                    dest_file.write(main_file)

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
                audio.save()
            except Exception as e:
                raise FileProcessingFailedError(f"Error encountered while saving to {save_path}: {e}")
        elif self.extension in [".wav", ".aiff"]:
            raise FileProcessingFailedError(f"Metadata can't be saved for {self.extension} files.")
        else:
            raise FileProcessingFailedError(f"Unsupported file type for {save_path}")