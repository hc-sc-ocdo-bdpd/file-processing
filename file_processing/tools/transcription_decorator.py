import whisper
import torch
from file_processing.tools import FileProcessorStrategy
from file_processing.tools.errors import TranscriptionProcessingError

class TranscriptionDecorator:
    def __init__(self, processor: FileProcessorStrategy) -> None:
        """Initializes the TranscriptionDecorator with a given file processor."""
        self._processor = processor

    def process(self) -> None:
        """Processes the file using the wrapped processor and then applies transcription."""
        self._processor.process()
        transcribed_text, language = self.extract_text_with_whisper()
        self._processor.metadata['text'] = transcribed_text
        self._processor.metadata['language'] = language

    def extract_text_with_whisper(self) -> str:
        """Extracts text from the file using Whisper by OpenAI.

        Returns:
            list: The extracted text, language
        """
        try:
            has_gpu = torch.cuda.is_available()
            device = 'cuda' if has_gpu else None

            text = whisper.transcribe(
                model=whisper.load_model('base', device=device),
                audio=str(self._processor.file_path),
                fp16=has_gpu
            )
            return text['text'], text['language']
        except Exception as e:
            raise TranscriptionProcessingError(
                f"Error during transcription processing: {e}")

    @property
    def file_name(self) -> str:
        """Returns the file name of the processed file."""
        return self._processor.file_name

    @property
    def extension(self) -> str:
        """Returns the file extension of the processed file."""
        return self._processor.extension

    @property
    def owner(self) -> str:
        """Returns the owner of the processed file."""
        return self._processor.owner

    @property
    def size(self) -> str:
        """Returns the size of the processed file."""
        return self._processor.size

    @property
    def modification_time(self) -> str:
        """Returns the modification time of the processed file."""
        return self._processor.modification_time

    @property
    def access_time(self) -> str:
        """Returns the access time of the processed file."""
        return self._processor.access_time

    @property
    def creation_time(self) -> str:
        """Returns the creation time of the processed file."""
        return self._processor.creation_time

    @property
    def parent_directory(self) -> str:
        """Returns the parent directory of the processed file."""
        return self._processor.parent_directory

    @property
    def permissions(self) -> str:
        """Returns the permissions of the processed file."""
        return self._processor.permissions

    @property
    def is_file(self) -> bool:
        """Returns True if the processed file is a regular file."""
        return self._processor.is_file

    @property
    def is_symlink(self) -> bool:
        """Returns True if the processed file is a symbolic link."""
        return self._processor.is_symlink

    @property
    def absolute_path(self) -> str:
        """Returns the absolute path of the processed file."""
        return self._processor.absolute_path

    @property
    def metadata(self) -> dict:
        """Returns the metadata of the processed file."""
        return self._processor.metadata
