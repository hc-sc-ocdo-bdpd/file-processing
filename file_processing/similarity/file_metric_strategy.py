from abc import ABC, abstractmethod
from file_processing import File
from file_processing.tools.errors import NotDocumentBasedFile


class FileMetricStrategy(ABC):
    def __init__(self, file1: File, file2: File):

        for file in [file1, file2]:
            if 'text' not in file.metadata:
                raise NotDocumentBasedFile(f'{file.file_name} is not a document-based file (it does not have the "text" metadata field)')

        self.file1 = file1
        self.file2 = file2

    @abstractmethod
    def calculate(self):
        pass
