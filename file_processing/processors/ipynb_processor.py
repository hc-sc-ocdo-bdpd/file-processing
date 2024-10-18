import json
from file_processing.errors import FileProcessingFailedError
from file_processing.file_processor_strategy import FileProcessorStrategy

class IpynbFileProcessor(FileProcessorStrategy):
    def __init__(self, file_path: str, open_file: bool = True) -> None:
        super().__init__(file_path, open_file)
        self.metadata = {'message': 'File was not opened'} if not open_file else {}

    def process(self) -> None:
        if not self.open_file:
            return
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                notebook = json.load(f)
            cells = notebook.get('cells', [])
            text = []
            for cell in cells:
                if cell['cell_type'] == 'markdown':
                    text.append(' '.join(cell['source']))
                elif cell['cell_type'] == 'code':
                    text.append(' '.join(cell['source']))
            self.metadata.update({
                'text': '\n'.join(text),
                'num_cells': len(cells),
                'num_code_cells': sum(1 for cell in cells if cell['cell_type'] == 'code'),
                'num_markdown_cells': sum(1 for cell in cells if cell['cell_type'] == 'markdown')
            })
        except Exception as e:
            raise FileProcessingFailedError(
                f"Error encountered while processing {self.file_path}: {e}")

    def save(self, output_path: str = None) -> None:
        try:
            save_path = output_path or self.file_path
            with open(self.file_path, 'r', encoding='utf-8') as f:
                notebook = json.load(f)
            text = self.metadata.get('text', '').split('\n')
            idx = 0
            for cell in notebook.get('cells', []):
                if cell['cell_type'] in ['markdown', 'code']:
                    cell['source'] = text[idx].split(' ')
                    idx += 1
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(notebook, f, indent=4)
        except Exception as e:
            raise FileProcessingFailedError(
                f"Error encountered while saving file {self.file_path} to {save_path}: {e}")
