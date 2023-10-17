from file_processor_strategy import FileProcessorStrategy
import zipfile
from pathlib import Path
import shutil

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

    
    def extract(self, output_dir: str = None) -> None:
        if not output_dir:
            output_dir = self.file_path.with_suffix('')

        Path(output_dir).mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(self.file_path, 'r') as zip_ref:
            zip_ref.extractall(output_dir)


    def save(self, output_path: str = None) -> None:
        output_path = output_path or str(self.file_path)
        shutil.copy2(self.file_path, output_path)