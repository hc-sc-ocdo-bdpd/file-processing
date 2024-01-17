from pathlib import Path
from generic_processor import GenericFileProcessor


class CorruptedFile:

    def __init__(self, path: str) -> None:
        self.path = Path(path)
        self.processor = GenericFileProcessor(str(self.path), False)
        self.process()

    def save(self, output_path: str = None) -> None:
        self.processor.save(output_path)

    def process(self) -> None:
        return self.processor.process()

    @property
    def file_path(self) -> str:
        return self.processor.file_path

    @property
    def file_name(self) -> str:
        return self.processor.file_name

    @property
    def extension(self) -> str:
        return self.processor.extension

    @property
    def size(self) -> str:
        return self.processor.size

    @property
    def modification_time(self) -> str:
        return self.processor.modification_time

    @property
    def access_time(self) -> str:
        return self.processor.access_time

    @property
    def creation_time(self) -> str:
        return self.processor.creation_time

    @property
    def parent_directory(self) -> str:
        return self.processor.parent_directory

    @property
    def is_file(self) -> bool:
        return self.processor.is_file

    @property
    def is_symlink(self) -> bool:
        return self.processor.is_symlink

    @property
    def absolute_path(self) -> str:
        return self.processor.absolute_path

    @property
    def metadata(self) -> dict:
        return self.processor.metadata
