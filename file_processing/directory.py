import os
from file import File
from typing import Optional
import pandas as pd
from pathlib import Path
from tqdm import tqdm
import json


class Directory:
    def __init__(self, path: str, use_ocr: bool = False) -> None:
        self.path = path
        self.use_ocr = use_ocr

    def _file_generator(self, filters: dict = None, open_files: bool = True):
        filters = filters or {}

        total_files = sum(len(files) for _, _, files in os.walk(self.path))

        with tqdm(total=total_files, desc='Generating Report', unit='file') as pbar:
            for root, _, filenames in os.walk(self.path):
                for filename in filenames:
                    file_path = os.path.join(root, filename)

                    pbar.update(1)
                    
                    if filters and not self._apply_filters(file_path, filters):
                        continue

                    try:
                        file = File(file_path, use_ocr=self.use_ocr, open_file=open_files)
                        yield file
                    except Exception as e:
                        file = File(file_path, open_file=False)
                        file.metadata.pop('message')
                        file.metadata.update({'error': type(e).__name__})
                        yield file

    def _apply_filters(self, file_path: str, filters: dict) -> bool:
        file = Path(file_path).resolve()
        if filters.get('exclude_str') and set(str(file).split('\\')) & set(filters['exclude_str']):
            return False
        if filters.get('include_str') and not (set(str(file).split('\\')) & set(filters['include_str'])):
            return False
        if filters.get('extensions') and file.suffix not in filters['extensions']:
            return False
        if filters.get('exclude_extensions') and file.suffix in filters['exclude_extensions']:
            return False
        if filters.get('min_size') and file.stat().st_size < filters['min_size']:
            return False
        if filters.get('max_size') and file.stat().st_size > filters['max_size']:
            return False

        return True  # Passes all filter conditions

    def get_files(self, filters: dict = None):
        return self._file_generator(filters)

    def generate_analytics(self, report_file: str = None, filters: Optional[dict] = None) -> dict:
        """
        Returns analytics (size and count) on the file types inside the directory.

        :param report_file: The path to the output CSV file. If none is specified, the data is returned directly.
        :param filters: A dictionary of filters to apply to the files.
        """

        data = [file.processor.__dict__ for file in self._file_generator(filters, False)]
        df = pd.DataFrame(data)
        df = df.get(['size', 'extension'])
        df['count'] = 1
        df = df.groupby('extension').sum()
        df['size'] = df['size'] / 1e6
        df.rename(columns={'size': 'size (MB)'}, inplace=True)

        if report_file:
            df.to_csv(report_file)

        return df.to_dict()

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

        CHAR_LIMIT = 3000

        # Extracting the attributes from the File object
        data = [file.processor.__dict__ for file in self._file_generator(filters, open_files)]

        # Imposing a character limit on each metadata property or removing the verbose fields entirely
        for file in data:
            file.pop('open_file', None)
            file['size'] = file['size'] / 1e6
            if migrate_filters:
                file['migrate'] = int(self._apply_filters(file['file_path'], migrate_filters))
            if include_text and open_files:
                file['metadata'] = {k: str(v)[:CHAR_LIMIT] for k, v in file['metadata'].items()}
                if keywords and file['metadata'].get('text'):
                    file['keywords'] = self._count_keywords(file['metadata']['text'], keywords)
                elif keywords:
                    file['keywords'] = self._count_keywords('', keywords)
            elif not include_text:
                for field in ['text', 'docstrings', 'imports', 'words', 'lines', 'data']:
                    file['metadata'].pop(field, None)

        # Unpacking the metadata field so each metadata property becomes its own column
        if split_metadata:
            data = pd.json_normalize(data, max_level=1, sep='_')
        
        df = pd.DataFrame(data)

        if df.empty:
            raise Exception('Filtered selection of files is empty. Please try different filters')

        df.columns = df.columns.str.replace('metadata_', '')
        df.columns = df.columns.str.replace('keywords_', 'Keyword.')

        if not split_metadata:
            df['metadata'] = df['metadata'].apply(lambda x: json.dumps(x))

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
    