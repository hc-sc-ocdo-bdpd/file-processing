from abc import ABC, abstractmethod
import os

class FileProcessorStrategy(ABC):
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_name = os.path.basename(file_path)
        self.extension = os.path.splitext(self.file_name)[1]
        self.size = os.path.getsize(file_path)
        self.modification_time = os.path.getmtime(file_path)
        self.access_time = os.path.getatime(file_path)

    @abstractmethod
    def process(self):
        # Abstract method to be implemented by subclasses for file processing
        pass