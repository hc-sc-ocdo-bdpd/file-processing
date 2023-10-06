from file_processor_strategy import FileProcessorStrategy
import zipfile

class ZipFileProcessor(FileProcessorStrategy):
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.metadata = {}
    
    def process(self) -> None:
        z = zipfile.ZipFile(self.file_path, 'r')
        self.metadata.update({"num_files": len(z.infolist())})
        self.metadata.update({"file_types": self.extract_file_types(z)})

    @staticmethod
    def extract_file_types(z):
        types = set()
        for info in z.infolist():
            fname = info.filename
            types.add(fname[fname.find('.') + 1:])
        return types

    def save(self):
        pass