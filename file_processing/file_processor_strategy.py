from abc import ABC, abstractmethod
from pathlib import Path

class FileProcessorStrategy(ABC):
    def __init__(self, file_path: str) -> None:
        self.file_path = Path(file_path)
        self.file_name = self.file_path.name
        self.extension = self.file_path.suffix
        self.size = self.file_path.stat().st_size
        self.modification_time = self.file_path.stat().st_mtime
        self.access_time = self.file_path.stat().st_atime
        self.creation_time = self.file_path.stat().st_ctime
        self.parent_directory = self.file_path.parent
        self.is_file = self.file_path.is_file()
        self.is_symlink = self.file_path.is_symlink()
        self.absolute_path = self.file_path.resolve()

    @abstractmethod
    def process(self) -> None:
        # Abstract method to be implemented by subclasses for file processing
        pass

    @abstractmethod
    def save(self) -> None:
        """Saves the processed file after metadata changes"""
        pass
