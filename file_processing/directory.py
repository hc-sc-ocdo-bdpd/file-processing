import os
import csv
from file import File
from typing import Optional
import json
from tqdm import tqdm
from corrupted_file import CorruptedFile
from datetime import datetime


class Directory:
    def __init__(self, path: str, use_ocr: bool = False) -> None:
        self.path = path
        self.use_ocr = use_ocr

    def _file_generator(self, filters: dict = None, open_files: bool = True):
        filters = filters or {}
        for root, _, filenames in os.walk(self.path):
            for filename in filenames:
                file_path = os.path.join(root, filename)

                try:
                    file = File(file_path, use_ocr=self.use_ocr,
                                open_file=open_files)
                    if not self._apply_filters(file, filters):
                        continue
                    yield file
                except Exception as e:
                    file = CorruptedFile(file_path)
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
                    'Size': file.size,
                    'Count': 1
                }
            else:
                extension_data[file.extension]['Size'] += file.size
                extension_data[file.extension]['Count'] += 1

        # Checks if an output file is specified and writes to it
        if report_file:
            try:
                with open(report_file, mode='w', newline='', encoding='utf-8') as file:

                    writer = csv.DictWriter(
                        file, fieldnames=['Extension', 'Size', 'Count'])
                    writer.writeheader()

                    for key, val in sorted(extension_data.items()):
                        row = {'Extension': key}
                        row.update(val)
                        writer.writerow(row)

            except Exception as e:
                raise

        return extension_data

    def generate_report(self, report_file: str, include_text: bool = False, filters: Optional[dict] = None,
                        keywords: Optional[list] = None, migrate_filters: Optional[dict] = None, open_files: bool = True) -> None:
        """
        Generates a report of the directory and writes it to a CSV file.

        :param report_file: The path to the output CSV file.
        :param include_text: Whether to include the 'text' attribute in the metadata column.
        :param filters: A dictionary of filters to apply to the files.
        :param migrate_filters: A dictionary of filters to mark whether an item should be migrated (True) or not (False).
        :param keywords: A list of keywords to count in the 'text' attribute of the metadata.
        :param open_files: Whether to open the files for extracting metadata. If False, files won't be opened.
        """

        try:
            # Count the total number of files that match the filters
            total_files = sum(1 for _ in self._file_generator(
                filters, open_files=open_files))

            with open(report_file, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)

                # Modify the header row to include the 'Keywords' column if keywords are provided
                header_row = ['File Path', 'File Name', 'Extension', 'Size', 'Modification Time', 'Access Time',
                              'Creation Time', 'Parent Directory', 'Is File?', 'Is Symlink?', 'Absolute Path', 'Metadata']
                if keywords:
                    header_row.append('Keywords')

                if migrate_filters:
                    header_row.append('Migrate?')

                writer.writerow(header_row)

                # Iterate over each file in the directory and write the information to the CSV file
                with tqdm(total=total_files, desc='Generating Report', unit='file') as pbar:
                    for file in self._file_generator(filters, open_files=open_files):
                        metadata = file.metadata.copy()
                        if not include_text or not open_files:
                            # Remove the 'text' attribute if it exists and include_text is False or files are not opened
                            metadata.pop('text', None)
                            metadata.pop('lines', None)
                            metadata.pop('words', None)
                            metadata.pop('docstrings', None)
                            metadata.pop('imports', None)

                        row_data = [
                            file.file_path,
                            file.file_name,
                            file.extension,
                            file.size,
                            datetime.fromtimestamp(file.modification_time),
                            datetime.fromtimestamp(file.access_time),
                            datetime.fromtimestamp(file.creation_time),
                            file.parent_directory,
                            int(file.is_file),
                            int(file.is_symlink),
                            file.absolute_path,
                            # Convert metadata to a JSON string
                            json.dumps(metadata, ensure_ascii=False)
                        ]

                        if keywords and include_text and open_files:
                            text = metadata.get('text', '')
                            if text is None:  # if {text: null} in metadata
                                text = ''
                            keyword_counts = self._count_keywords(
                                text, keywords)
                            row_data.append(json.dumps(
                                keyword_counts, ensure_ascii=False))

                        if migrate_filters:
                            row_data.append(
                                int(self._apply_filters(file, migrate_filters)))

                        writer.writerow(row_data)
                        pbar.update(1)
        except Exception as e:
            raise

    def _count_keywords(self, text: str, keywords: list) -> dict:
        """
        Counts the occurrences of each keyword in the given text.

        :param text: The text to search in.
        :param keywords: The list of keywords to count.
        :return: A dictionary with the keywords as keys and their counts as values.
        """

        keyword_dict = {}
        text = text.lower()

        for keyword in keywords:
            count = text.count(keyword.lower())
            keyword_dict[keyword] = count

        return keyword_dict
