from pathlib import Path
from file_processing.file_processor_strategy import FileProcessorStrategy
from file_processing.errors import FileProcessingFailedError

class DirectoryProcessor(FileProcessorStrategy):
    """
    Processor for handling directories, gathering metadata and saving information about
    the top-level contents of the directory.

    Attributes:
        metadata (dict): Contains metadata such as the number of items, total size, and permissions.
    """

    def __init__(self, dir_path: str, open_file: bool = True) -> None:
        """
        Initializes the DirectoryProcessor with the specified directory path.

        Args:
            dir_path (str): Path to the directory to process.
            open_file (bool): Indicates whether to process the directory immediately.

        Raises:
            FileProcessingFailedError: If the provided path is not a directory.
        """
        super().__init__(dir_path, open_file)

        # Ensure that this path is a directory
        if not self.file_path.is_dir():
            raise FileProcessingFailedError(f"Path is not a directory: {dir_path}")

        self.metadata = self._gather_basic_metadata()

    def _gather_basic_metadata(self) -> dict:
        """
        Gathers and returns basic metadata about the directory, excluding subdirectories.

        Returns:
            dict: Metadata with the number of items, total size of files, and directory permissions.
        """
        metadata = {
            'num_items_in_top_level': len(list(self.file_path.iterdir())),
            'total_size_of_files_in_top_level': self._get_top_level_size(),
            'permissions': self._get_permissions(),  # Gather directory permissions
        }
        return metadata

    def _get_permissions(self) -> str:
        """
        Fetches and returns the permissions of the directory in octal format.

        Returns:
            str: Permissions of the directory.
        """
        return oct(self.file_path.stat().st_mode)[-3:]

    def _get_top_level_size(self) -> int:
        """
        Calculates the total size of files in the top-level directory (excluding subdirectories).

        Returns:
            int: Total size of files in bytes.
        """
        return sum(f.stat().st_size for f in self.file_path.iterdir() if f.is_file())

    def list_files_in_top_level(self) -> list:
        """
        Lists files in the top-level directory, excluding subdirectories.

        Returns:
            list: List of Path objects for each file in the top-level directory.
        """
        return [f for f in self.file_path.iterdir() if f.is_file()]

    def list_top_level_subdirectories(self) -> list:
        """
        Lists subdirectories in the top-level directory.

        Returns:
            list: List of Path objects for each subdirectory in the top-level directory.
        """
        return [d for d in self.file_path.iterdir() if d.is_dir()]

    def process(self) -> None:
        """Processes the directory; intended as a placeholder for interface compatibility."""
        pass

    def save(self, output_path: str = None) -> None:
        """
        Saves the gathered directory metadata to the specified output path.

        Args:
            output_path (str): The file path where metadata should be saved.

        Raises:
            FileProcessingFailedError: If the output path is not provided, does not exist,
                                       or if an error occurs during saving.
        """
        if output_path is None:
            raise FileProcessingFailedError("Output path not provided.")
        
        output_path = Path(output_path)
        if not output_path.parent.exists():
            raise FileProcessingFailedError(f"Save location does not exist: {output_path}")
        
        # Logic for saving the directory metadata
        try:
            with open(output_path, 'w') as f:
                f.write(str(self.metadata))  # Serialize metadata as needed
        except Exception as e:
            raise FileProcessingFailedError(f"Failed to save directory metadata: {e}")
