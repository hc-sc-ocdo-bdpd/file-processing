from file_processor_strategy import FileProcessorStrategy
from openpyxl import load_workbook 

class xlsxFileProcessor(FileProcessorStrategy):
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.metadata = {}
    
    def process(self) -> None:
        exceldoc = load_workbook(self.file_path)
        self.metadata.update({"active sheet": exceldoc.active})
        self.metadata.update({"sheet names": exceldoc.sheetnames})
        self.metadata.update({"data":self.read_all_data(exceldoc)})
        self.metadata.update({"last_modified_by": exceldoc.properties.lastModifiedBy})
        self.metadata.update({"creator": exceldoc.properties.creator})
    
    @staticmethod
    def read_all_data(exceldoc):
        data = {}
        for sheet_name in exceldoc.sheetnames:
            sheet = exceldoc[sheet_name]
            sheet_data = []
            for row in sheet.iter_rows(values_only=True):
                sheet_data.append(row)
            data[sheet_name] = sheet_data
        return data
    