from abc import ABC, abstractmethod
from pathlib import Path
import sys
import importlib.util
from file_processing.errors import FileProcessingFailedError

class FileProcessorStrategy(ABC):
    def __init__(self, file_path: str, open_file: bool = True) -> None:
        self.file_path = Path(file_path)

        # Check if the file or directory exists
        if not self.file_path.exists():
            raise FileProcessingFailedError(f"File or directory does not exist: {file_path}")

        self.open_file = open_file
        self.file_name = self.file_path.name
        self.owner = self._find_owner(file_path)
        self.extension = self.file_path.suffix
        self.size = self.file_path.stat().st_size
        self.modification_time = self.file_path.stat().st_mtime
        self.access_time = self.file_path.stat().st_atime
        self.creation_time = self.file_path.stat().st_ctime
        self.parent_directory = self.file_path.parent
        self.permissions = oct(self.file_path.stat().st_mode)[-3:]
        self.is_file = self.file_path.is_file()
        self.is_symlink = self.file_path.is_symlink()
        self.absolute_path = self.file_path.resolve()

    def _find_owner(self, file_path: str) -> str:
        if sys.platform == 'win32' and importlib.util.find_spec('win32security'):
            import win32security
            sd = win32security.GetFileSecurity(file_path, win32security.OWNER_SECURITY_INFORMATION)
            owner_sid = sd.GetSecurityDescriptorOwner()
            name, domain, _ = win32security.LookupAccountSid(None, owner_sid)
            return f'{domain}/{name}'
        return ''

    @abstractmethod
    def process(self) -> None:
        if not self.open_file:
            return

    @abstractmethod
    def save(self) -> None:
        """Saves the processed file after metadata changes"""
