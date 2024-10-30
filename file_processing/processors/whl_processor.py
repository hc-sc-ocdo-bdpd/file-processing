import re
import zipfile
import shutil
from pathlib import Path
from importlib.metadata import PathDistribution
from file_processing.errors import FileProcessingFailedError
from file_processing.file_processor_strategy import FileProcessorStrategy

class WhlFileProcessor(FileProcessorStrategy):
    def __init__(self, file_path: str, open_file: bool = True) -> None:
        super().__init__(file_path, open_file)
        self.metadata = {'message': 'File was not opened'} if not open_file else self._default_metadata()

    def _default_metadata(self) -> dict:
        return {
            "package_name": None,
            "version": None,
            "python_compatibility": None,
            "platform_compatibility": None,
            "optional_dependencies": [],
            "non_optional_dependencies": [],
            "author": None,
            "build_tag": None,
        }

    def process(self) -> None:
        if not self.open_file:
            return
        
        try:
            with zipfile.ZipFile(self.file_path, 'r') as whl_file:
                # Find the .dist-info directory and access the METADATA file
                metadata_file = None
                for name in whl_file.namelist():
                    if name.endswith('.dist-info/METADATA'):
                        metadata_file = name
                        break
                
                if metadata_file:
                    # Extract metadata content
                    with whl_file.open(metadata_file) as meta:
                        metadata_content = meta.read().decode('utf-8')
                        self._extract_metadata(metadata_content)
                else:
                    raise FileProcessingFailedError(f"METADATA file not found in {self.file_path}")
        except Exception as e:
            raise FileProcessingFailedError(
                f"Error encountered while processing {self.file_path}: {e}")

    def _extract_metadata(self, metadata_content: str) -> None:
        # Parse metadata content to extract fields
        self.metadata["package_name"] = self._extract_metadata_value(metadata_content, "Name")
        self.metadata["version"] = self._extract_metadata_value(metadata_content, "Version")
        self.metadata["python_compatibility"] = self._extract_metadata_value(metadata_content, "Requires-Python")
        self.metadata["author"] = self._extract_author(metadata_content)
        self.metadata["platform_compatibility"] = self._extract_platform_compatibility(metadata_content)
        self.metadata["optional_dependencies"] = self._extract_optional_dependencies(metadata_content)
        self.metadata["non_optional_dependencies"] = self._extract_non_optional_dependencies(metadata_content)
        self.metadata["build_tag"] = self._extract_build_tag()

    def _extract_author(self, content: str) -> str:
        # Try to extract from Author field first
        match = re.search(r"^Author: (.+)$", content, re.MULTILINE)
        if match:
            return match.group(1).strip()
    
        # If Author is not present, try Author-Email and extract only the name part
        match = re.search(r"^Author-Email: ([^<]+)", content, re.MULTILINE)
        if match:
            # Capture only the name before any email (in format `Name <email>`)
            return match.group(1).strip().split("<")[0].strip()
        return None

    def _extract_metadata_value(self, content: str, key: str) -> str:
        # Extract single metadata value based on key
        match = re.search(rf"^{key}: (.+)$", content, re.MULTILINE)
        return match.group(1) if match else None

    def _extract_platform_compatibility(self, content: str) -> str | list:
        platforms = re.findall(r"^Classifier: Operating System :: (.+)$", content, re.MULTILINE)
    
        if not platforms:
            return None
        elif len(platforms) == 1:
            return platforms[0]
        else:
            return platforms

    def _extract_optional_dependencies(self, content: str) -> list:
        # Extract Requires-Dist with extra conditions (e.g., `; extra == "test"`)
        matches = re.findall(r"^Requires-Dist: (.+); extra == \"(.+)\"", content, re.MULTILINE)
        return [f"{dep} (extra: {extra})" for dep, extra in matches]

    def _extract_non_optional_dependencies(self, content: str) -> list:
        non_optional_deps = []
        for line in content.splitlines():
            # Match 'Requires-Dist' lines without 'extra =='
            if line.startswith("Requires-Dist:") and "extra ==" not in line:
                dep = line.replace("Requires-Dist:", "").strip()
                non_optional_deps.append(dep)
        return non_optional_deps

    def _extract_build_tag(self) -> str:
        # Extract build tag from file name if possible (e.g., pandas-2.2.3-1-cp37-cp37m-manylinux1_x86_64.whl) would be 1
        file_path_str = str(self.file_path)
        match = re.search(r"-([0-9]+)-", file_path_str)
        return match.group(1) if match else None

    def save(self, output_path: str = None) -> None:
        try:
            output_path = output_path or str(self.file_path)
            shutil.copy2(self.file_path, output_path)
        except Exception as e:
            raise FileProcessingFailedError(
                f"Error encountered while saving {self.file_path}: {e}")
