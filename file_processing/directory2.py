import os
import csv
from file import File
from typing import Optional
import pandas as pd
import numpy as np


class Directory:
    def __init__(self, path: str, use_ocr: bool = False) -> None:
        self.path = path
        self.use_ocr = use_ocr

    def _file_generator(self, filters: dict = None, open_files: bool = True):
        filters = filters or {}
        for root, _, filenames in os.walk(self.path):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                # TODO: Filter before initializing File()
                try:
                    file = File(file_path, use_ocr=self.use_ocr,
                                open_file=open_files)
                    if not self._apply_filters(file, filters):
                        continue
                    yield file
                except Exception as e:
                    file = File(file_path, use_ocr=False, open_file=False)
                    file.metadata.pop('message')
                    file.metadata.update({'error': type(e).__name__})
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

    def generate_analytics(self, report_file: str = None, filters: Optional[dict] = None) -> dict:
        """
        Returns analytics (size and count) on the file types inside the directory.

        :param report_file: The path to the output CSV file. If none is specified, the data is returned directly.
        :param filters: A dictionary of filters to apply to the files.
        """

        extension_data = {}

        # Grouping the files by extension and tracking their size (bytes) and count fields
        for file in self._file_generator(filters, open_files=False):
            if file.extension not in extension_data:
                extension_data[file.extension] = {
                    'Size (MB)': file.size/1e6,
                    'Count': 1
                }
            else:
                if 'Size (MB)' in extension_data[file.extension]:
                    extension_data[file.extension]['Size (MB)'] += file.size
                    extension_data[file.extension]['Count'] += 1

        # Checks if an output file is specified and writes to it
        if report_file:
            try:
                with open(report_file, mode='w', newline='', encoding='utf-8') as file:

                    writer = csv.DictWriter(file, fieldnames=['Extension', 'Size (MB)', 'Count'])
                    writer.writeheader()

                    for key, val in sorted(extension_data.items()):
                        row = {'Extension': key}
                        row.update(val)
                        writer.writerow(row)

            except Exception as e:
                raise

        return extension_data

    def generate_report(self, report_file: str, include_text: bool = False, filters: Optional[dict] = None,
                        keywords: Optional[list] = None, migrate_filters: Optional[dict] = None, 
                        open_files: bool = True, split_metadata: bool = False) -> None:
        """
        Generates a report of the directory and writes it to a CSV file.

        :param report_file: The path to the output CSV file.
        :param include_text: Whether to include the 'text' attribute in the metadata column.
        :param filters: A dictionary of filters to apply to the files.
        :param keywords: A list of keywords to count in the 'text' attribute of the metadata.   
        :param migrate_filters: A dictionary of filters to mark whether an item should be migrated (True) or not (False).
        :param open_files: Whether to open the files for extracting metadata. If False, files won't be opened.
        :param split_metadata: Whether to unpack the metadata dictionary into separate columns in the CSV file.
        """

        CHAR_LIMIT = 500

        # Extracting the attributes from the File object
        data = [file.processor.__dict__ for file in self._file_generator(filters, open_files)]

        # Imposing a character limit on each metadata property or removing the verbose fields entirely
        for file in data:
            if include_text:
                file['metadata'] = {k: str(v)[:CHAR_LIMIT] for k, v in file['metadata'].items()}
            elif not include_text:
                for field in ['text', 'docstrings', 'imports', 'words', 'lines']:
                    file['metadata'].pop(field, None)

        # Unpacking the metadata field so each metadata property becomes its own column
        if split_metadata:
            data = pd.json_normalize(data, max_level=1, sep='_')
        
        df = pd.DataFrame(data)

        df.columns = df.columns.str.replace('metadata_', '')
        df = df.drop(['open_file'], axis=1)
        df['size'] = df['size'] / 1e6

        # Converting booleans to integers (True->1; False->0)
        for boolean in ['is_file', 'is_symlink']:
            df[boolean] = df[boolean].astype(int)

        # Converting unix time to datetime
        for time in ['modification_time', 'access_time', 'creation_time']:
            df[time] = pd.to_datetime(df[time].round(0), unit='s')

        # df.replace(np.NaN, 'N/A', inplace=True)
        df.columns = df.columns.str.replace('_', ' ')
        df.columns = df.columns.str.title()
        df.rename(columns={'Size': 'Size (MB)'}, inplace=True)

        df.to_csv(report_file)