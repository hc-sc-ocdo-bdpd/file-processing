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
        self.metadata.update({"file_names": z.namelist()})

    @staticmethod
    def extract_file_types(z):
        types = dict()
        for info in z.infolist():
            fname = info.filename
            ext = fname[fname.find('.') + 1:]
            if ext in types.keys():
                types[ext] = types[ext] + 1
            else:
                types[ext] = 1
        return types

    def save(self):
        pass