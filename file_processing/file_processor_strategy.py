from abc import ABC, abstractmethod
from pathlib import Path
import sys
import importlib.util
from file_processing.errors import FileProcessingFailedError

class FileProcessorStrategy(ABC):
    """
    Abstract base class defining the strategy interface for file processing.
    Concrete implementations should define file-specific processing and saving
    behavior. This class provides basic file metadata extraction and validation.

    Attributes:
        file_path (Path): The path of the file to be processed.
        open_file (bool): Flag indicating if the file should be opened immediately.
        file_name (str): The name of the file.
        owner (str): The owner of the file.
        extension (str): The file extension.
        size (int): The size of the file in bytes.
        modification_time (float): Last modification timestamp of the file.
        access_time (float): Last access timestamp of the file.
        creation_time (float): Creation timestamp of the file.
        parent_directory (Path): The parent directory of the file.
        permissions (str): File permissions in octal representation.
        is_file (bool): Indicates if the path is a regular file.
        is_symlink (bool): Indicates if the file is a symbolic link.
        absolute_path (Path): The absolute path of the file.
    """

    def __init__(self, file_path: str, open_file: bool = True) -> None:
        """
        Initializes the file processor with metadata extraction for the given file.

        Args:
            file_path (str): The path of the file to process.
            open_file (bool): Flag to open the file immediately if set to True.

        Raises:
            FileProcessingFailedError: If the specified file or directory does not exist.
        """
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
        """
        Determines the owner of the file. For Windows, retrieves the owner information
        if the `win32security` library is available.

        Args:
            file_path (str): Path to the file for which to find the owner.

        Returns:
            str: The owner of the file in 'domain/name' format, or an empty string if unavailable.
        """
        if sys.platform == 'win32' and importlib.util.find_spec('win32security'):
            import win32security
            sd = win32security.GetFileSecurity(file_path, win32security.OWNER_SECURITY_INFORMATION)
            owner_sid = sd.GetSecurityDescriptorOwner()
            name, domain, _ = win32security.LookupAccountSid(None, owner_sid)
            return f'{domain}/{name}'
        return ''

    @abstractmethod
    def process(self) -> None:
        """
        Processes the file according to its type. This method should be overridden
        by subclasses to implement specific file processing logic.

        Note:
            If `open_file` is False, this method may simply return without performing
            any processing.
        """
        if not self.open_file:
            return

    @abstractmethod
    def save(self) -> None:
        """
        Saves the processed file after any metadata or content modifications.
        This method must be implemented by subclasses to define save behavior.
        """