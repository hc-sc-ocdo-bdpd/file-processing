from file_processor_strategy import FileProcessorStrategy
from openpyxl import load_workbook 
from zipfile import ZipFile
from zipfile import BadZipFile

class xlsxFileProcessor(FileProcessorStrategy):
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.metadata = {}
    
    def process(self) -> None:
        try:
            with ZipFile(self.file_path) as zf:
                exceldoc = load_workbook(self.file_path)
                self.metadata.update({"active_sheet": exceldoc.active})
                self.metadata.update({"sheet_names": exceldoc.sheetnames})
                self.metadata.update({"data":self.read_all_data(exceldoc)})
                self.metadata.update({"last_modified_by": exceldoc.properties.lastModifiedBy})
                self.metadata.update({"creator": exceldoc.properties.creator})
        except BadZipFile:
            raise
   
    def save(self, output_path: str = None) -> None:
        exceldoc = load_workbook(self.file_path)
        cp = exceldoc.properties
        # Update the core properties (metadata)
        cp.creator = self.metadata.get('creator', cp.creator)
        cp.last_modified_by = self.metadata.get('last_modified_by', cp.lastModifiedBy)
        
        save_path = output_path or self.file_path
        exceldoc.save(save_path)
 
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
