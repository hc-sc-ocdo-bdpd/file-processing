import re
from file_processing.tools.errors import FileProcessingFailedError
from file_processing.tools import FileProcessorStrategy


class CssFileProcessor(FileProcessorStrategy):
    def __init__(self, file_path: str, open_file: bool = True) -> None:
        super().__init__(file_path, open_file)
        self.metadata = {'message': 'File was not opened'} if not open_file else {}

    def process(self) -> None:
        if not self.open_file:
            return
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            rules = re.findall(r'([^{]+)\{([^}]+)\}', content)
            self.metadata.update({
                'text': content,
                'num_rules': len(rules),
                'selectors': [rule.strip() for rule in rules],
                'properties': [rule.strip() for rule in rules]
            })
        except Exception as e:
            raise FileProcessingFailedError(
                f"Error encountered while processing {self.file_path}: {e}")

    def save(self, output_path: str = None) -> None:
        try:
            save_path = output_path or self.file_path
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(self.metadata.get('text', ''))
        except Exception as e:
            raise FileProcessingFailedError(
                f"Error encountered while saving file {self.file_path} to {save_path}: {e}")
