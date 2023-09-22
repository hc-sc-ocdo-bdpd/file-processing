import os
from file import File

class Directory:
    def __init__(self, path: str, use_ocr: bool = False) -> None:
        self.path = path
        self.use_ocr = use_ocr

    def _file_generator(self, filters: dict = None):
        filters = filters or {}
        for root, _, filenames in os.walk(self.path):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                file = File(file_path, use_ocr=self.use_ocr)
                if not self._apply_filters(file, filters):
                    continue
                yield file

    def _apply_filters(self, file: File, filters: dict) -> bool:
        if filters.get('extensions') and file.extension not in filters['extensions']:
            return False
        
        # Example: Filter by size
        if filters.get('min_size') and file.size < filters['min_size']:
            return False
        if filters.get('max_size') and file.size > filters['max_size']:
            return False
        
        # Additional filter conditions can be added here as needed
        
        return True  # Passes all filter conditions

    def get_files(self, filters: dict = None):
        return self._file_generator(filters)