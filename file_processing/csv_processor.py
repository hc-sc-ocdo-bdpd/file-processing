import csv
import chardet
from file_processing.errors import FileProcessingFailedError
from file_processing.file_processor_strategy import FileProcessorStrategy


class CsvFileProcessor(FileProcessorStrategy):
    def __init__(self, file_path: str, open_file: bool = True) -> None:
        super().__init__(file_path, open_file)
        self.metadata = {}
        self.metadata = {
            'message': 'File was not opened'} if not open_file else {}

    def process(self) -> None:
        if not self.open_file:
            return
        try:
            encoding = chardet.detect(
                open(self.file_path, 'rb').read())['encoding']
            with open(self.file_path, 'r', newline='\n', encoding=encoding) as f:
                reader = csv.reader(f)
                # List of rows, e.g. [['row', 'one'], ['row', 'two']]
                rows = [row for row in reader]
                text = '\n'.join(['","'.join(row) for row in rows])
                num_cells = 0
                empty_cells = 0
                for row in rows:
                    for cell in row:
                        num_cells += 1
                        if cell == '' or cell == ' ':
                            empty_cells += 1
                self.metadata.update({
                    'text': text,
                    'encoding': encoding,
                    'num_rows': len(rows),
                    'num_cols': len(rows[0]) if rows else 0,
                    'num_cells': num_cells,
                    'empty_cells': empty_cells
                })
        except Exception as e:
            raise FileProcessingFailedError(
                f"Error encountered while processing {self.file_path}: {e}")

    def save(self, output_path: str = None) -> None:
        try:
            save_path = output_path or self.file_path
            with open(save_path, 'w', newline='\n', encoding=self.metadata['encoding']) as f:
                writer = csv.writer(f)
                rows = self.metadata['text'].split('\n')
                for row in rows:
                    writer.writerow(row.split('","'))
        except Exception as e:
            raise FileProcessingFailedError(
                f"Error encountered while saving file {self.file_path} to {save_path}: {e}")
