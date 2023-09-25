import os
import csv
from file import File
from typing import Optional
import json
from tqdm import tqdm

class Directory:
    def __init__(self, path: str, use_ocr: bool = False) -> None:
        self.path = path
        self.use_ocr = use_ocr


    def _file_generator(self, filters: dict = None):
        filters = filters or {}
        for root, _, filenames in os.walk(self.path):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                file = File(file_path, use_ocr=self.use_ocr)
                if not self._apply_filters(file, filters):
                    continue
                yield file


    def _apply_filters(self, file: File, filters: dict) -> bool:
        if filters.get('extensions') and file.extension not in filters['extensions']:
            return False
        
        if filters.get('min_size') and file.size < filters['min_size']:
            return False
        if filters.get('max_size') and file.size > filters['max_size']:
            return False
        
        # Additional filter conditions can be added here as needed
        
        return True  # Passes all filter conditions


    def get_files(self, filters: dict = None):
        return self._file_generator(filters)


    def generate_report(self, report_file: str, include_text: bool = True, filters: Optional[dict] = None) -> None:
        """
        Generates a report of the directory and writes it to a CSV file.

        :param report_file: The path to the output CSV file.
        :param include_text: Whether to include the 'text' attribute in the metadata column.
        :param filters: A dictionary of filters to apply to the files.
        """

        # Count the total number of files that match the filters
        total_files = sum(1 for _ in self._file_generator(filters))

        with open(report_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            # Write the header row to the CSV file
            writer.writerow([
                'File Path', 'File Name', 'Extension', 'Size', 'Modification Time', 'Access Time', 'Metadata'
            ])
            
            # Iterate over each file in the directory and write the information to the CSV file
            with tqdm(total=total_files, desc='Generating Report', unit='file') as pbar:
                for file in self._file_generator(filters):
                    metadata = file.metadata.copy()
                    if not include_text:
                        metadata.pop('text', None)  # Remove the 'text' attribute if it exists and include_text is False
                    
                    writer.writerow([
                        file.file_path,
                        file.file_name,
                        file.extension,
                        file.size,
                        file.modification_time,
                        file.access_time,
                        json.dumps(metadata, ensure_ascii=False)  # Convert metadata to a JSON string
                    ])
                    
                    # Update the progress bar after processing each file
                    pbar.update(1)


    def _count_keywords(self, text: str, keywords: list) -> dict:
        """
        Counts the occurrences of each keyword in the given text.

        :param text: The text to search in.
        :param keywords: The list of keywords to count.
        :return: A dictionary with the keywords as keys and their counts as values.
        """
        return 1



