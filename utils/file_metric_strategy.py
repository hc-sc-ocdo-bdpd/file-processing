from abc import ABC, abstractmethod

class FileMetricStrategy(ABC):
    def __init__(self, file1, file2):
        self.file1 = file1
        self.file2 = file2

    @abstractmethod
    def calculate(self):
        pass
