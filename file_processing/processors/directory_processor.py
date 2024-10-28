from pathlib import Path
from file_processing.file_processor_strategy import FileProcessorStrategy
from file_processing.errors import FileProcessingFailedError

class DirectoryProcessor(FileProcessorStrategy):
    def __init__(self, dir_path: str, open_file: bool = True) -> None:
        super().__init__(dir_path, open_file)

        # Ensure that this path is a directory
        if not self.file_path.is_dir():
            raise FileProcessingFailedError(f"Path is not a directory: {dir_path}")

        self.metadata = self._gather_basic_metadata()

    def _gather_basic_metadata(self) -> dict:
        # Gather and return basic metadata about the directory, excluding subdirectories
        metadata = {
            'num_items_in_top_level': len(list(self.file_path.iterdir())),
            'total_size_of_files_in_top_level': self._get_top_level_size(),
            'permissions': self._get_permissions(),  # Gather directory permissions
        }
        return metadata

    def _get_permissions(self) -> str:
        # Fetch and return the permissions of the directory
        return oct(self.file_path.stat().st_mode)[-3:]  # Directory permissions

    def _get_top_level_size(self) -> int:
        # Calculate the total size of files in the top-level directory (excluding subdirectories)
        return sum(f.stat().st_size for f in self.file_path.iterdir() if f.is_file())

    def list_files_in_top_level(self) -> list:
        # Returns a list of files in the top-level directory (Path objects), excluding subdirectories
        return [f for f in self.file_path.iterdir() if f.is_file()]

    def list_top_level_subdirectories(self) -> list:
        # Returns a list of subdirectories in the top-level directory (Path objects)
        return [d for d in self.file_path.iterdir() if d.is_dir()]

    def process(self) -> None:
        pass

    def save(self, output_path: str = None) -> None:
        if output_path is None:
            raise FileProcessingFailedError("Output path not provided.")
        
        output_path = Path(output_path)
        if not output_path.parent.exists():
            raise FileProcessingFailedError(f"Save location does not exist: {output_path}")
        
        # Logic for saving the directory metadata
        try:
            with open(output_path, 'w') as f:
                f.write(str(self.metadata))  # Just an example, you could serialize metadata differently
        except Exception as e:
            raise FileProcessingFailedError(f"Failed to save directory metadata: {e}")
