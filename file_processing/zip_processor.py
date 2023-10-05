from file_processor_strategy import FileProcessorStrategy
import zipfile

class ZipFileProcessor(FileProcessorStrategy):
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.metadata = {}
    
    def process(self) -> None:
        pass
        # print("hi")
        # z = zipfile.ZipFile(self.file_path, 'r')
        # for info in z.infolist():
        #     fname = info.filename
        #     data = z.read(fname)
        #     print(fname)
        #     print(data)

    def save(self):
        pass