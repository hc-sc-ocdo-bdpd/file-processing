import pefile
from pathlib import Path
import shutil
from file_processing.errors import FileProcessingFailedError
from file_processing.file_processor_strategy import FileProcessorStrategy

class ExeFileProcessor(FileProcessorStrategy):
    def __init__(self, file_path: str, open_file: bool = True) -> None:
        super().__init__(file_path, open_file)
        self.metadata = {'message': 'File was not opened'} if not open_file else {}

    def process(self) -> None:
        if not self.open_file:
            return

        try:
            pe = pefile.PE(self.file_path)
            self.metadata.update({
                "entry_point": hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint),
                "machine": hex(pe.FILE_HEADER.Machine),
                "num_sections": len(pe.sections),
                "imports": self.extract_imports(pe),
                "sections": self.extract_sections(pe),
            })
        except Exception as e:
            raise FileProcessingFailedError(
                f"Error encountered while processing {self.file_path}: {e}")

    @staticmethod
    def extract_imports(pe):
        imports = {}
        try:
            if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
                for entry in pe.DIRECTORY_ENTRY_IMPORT:
                    dll_name = entry.dll.decode('utf-8')
                    functions = [imp.name.decode('utf-8') for imp in entry.imports if imp.name]
                    imports[dll_name] = functions
        except Exception as e:
            raise FileProcessingFailedError(
                f"Error encountered while extracting imports: {e}")
        return imports

    @staticmethod
    def extract_sections(pe):
        sections = []
        try:
            for section in pe.sections:
                sections.append({
                    'name': section.Name.decode('utf-8').strip(),
                    'virtual_address': hex(section.VirtualAddress),
                    'size_of_raw_data': section.SizeOfRawData,
                    'entropy': section.get_entropy(),
                })
        except Exception as e:
            raise FileProcessingFailedError(
                f"Error encountered while extracting sections: {e}")
        return sections

    def save(self, output_path: str = None) -> None:
        try:
            output_path = output_path or str(self.file_path)
            shutil.copy2(self.file_path, output_path)
        except Exception as e:
            raise FileProcessingFailedError(
                f"Error encountered while saving {self.file_path}: {e}")