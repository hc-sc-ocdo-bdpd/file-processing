import pefile
from pathlib import Path
import shutil
from file_processing.errors import FileProcessingFailedError
from file_processing.file_processor_strategy import FileProcessorStrategy

class ExeFileProcessor(FileProcessorStrategy):
    """
    Processor for handling .exe files, extracting metadata and saving the file.

    Attributes:
        metadata (dict): Contains metadata fields such as 'entry_point', 'machine', 'num_sections',
                         'imports', and 'sections' if the file is opened.
    """

    def __init__(self, file_path: str, open_file: bool = True) -> None:
        """
        Initializes the ExeFileProcessor with the specified file path.

        Args:
            file_path (str): Path to the .exe file to process.
            open_file (bool): Indicates whether to open and process the file immediately.

        Sets:
            metadata (dict): Populated with 'message' if `open_file` is False.
        """
        super().__init__(file_path, open_file)
        self.metadata = {'message': 'File was not opened'} if not open_file else {}

    def process(self) -> None:
        """
        Extracts metadata from the .exe file, including entry point, machine type, number of sections,
        imports, and section details.

        Raises:
            FileProcessingFailedError: If an error occurs during .exe file processing.
        """
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
                f"Error encountered while processing {self.file_path}: {e}"
            )

    @staticmethod
    def extract_imports(pe):
        """
        Extracts imported DLLs and their functions from the .exe file.

        Args:
            pe (PE): A `PE` instance representing the parsed .exe file.

        Returns:
            dict: Dictionary where keys are DLL names and values are lists of imported function names.

        Raises:
            FileProcessingFailedError: If an error occurs while extracting imports.
        """
        imports = {}
        try:
            if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
                for entry in pe.DIRECTORY_ENTRY_IMPORT:
                    dll_name = entry.dll.decode('utf-8')
                    functions = [imp.name.decode('utf-8') for imp in entry.imports if imp.name]
                    imports[dll_name] = functions
        except Exception as e:
            raise FileProcessingFailedError(
                f"Error encountered while extracting imports: {e}"
            )
        return imports

    @staticmethod
    def extract_sections(pe):
        """
        Extracts details of sections in the .exe file, such as name, virtual address, size of raw data, and entropy.

        Args:
            pe (PE): A `PE` instance representing the parsed .exe file.

        Returns:
            list: List of dictionaries, each containing section details.

        Raises:
            FileProcessingFailedError: If an error occurs while extracting sections.
        """
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
                f"Error encountered while extracting sections: {e}"
            )
        return sections

    def save(self, output_path: str = None) -> None:
        """
        Saves a copy of the .exe file to the specified output path.

        Args:
            output_path (str): Path to save the copied .exe file. If None, overwrites the original file.

        Raises:
            FileProcessingFailedError: If an error occurs while saving the .exe file.
        """
        try:
            output_path = output_path or str(self.file_path)
            shutil.copy2(self.file_path, output_path)
        except Exception as e:
            raise FileProcessingFailedError(
                f"Error encountered while saving {self.file_path}: {e}"
            )