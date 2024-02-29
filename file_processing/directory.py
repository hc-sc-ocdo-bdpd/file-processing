import os
import json
import logging
from typing import Optional
from pathlib import Path

import faiss
import pandas as pd
import numpy as np
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cdist
from file_processing import File
from file_processing.tools.errors import EmptySelection


class Directory:
    def __init__(self, path: str, use_ocr: bool = False) -> None:
        self.path = path
        self.use_ocr = use_ocr

    def _file_generator(self, filters: dict = None, open_files: bool = True,
                        start_at: int = 0, batch_size: int = 0):
        filters = filters or {}
        batch = []

        with tqdm(desc='Processing files', unit=' files completed') as pbar:
            for dirpath, _, filenames in os.walk(self.path):
                for filename in filenames:
                    pbar.update(1)
                    file_path = os.path.join(dirpath, filename)

                    if filters and not self._apply_filters(file_path, filters):
                        continue

                    # Start processing when the starting index is reached
                    if pbar.n > start_at:
                        file_obj = None

                        # Process the file
                        try:
                            file_obj = File(file_path, use_ocr=self.use_ocr, open_file=open_files)
                            logging.info('Processing file: %s', file_path)
                        except Exception as e:
                            logging.error('Error processing %s: %s', file_path, type(e).__name__)
                            file_obj = File(file_path, open_file=False)
                            file_obj.metadata.pop('message')
                            file_obj.metadata.update({'error': type(e).__name__})

                        # Batching; yield if batch_size = 0, otherwise wait until the batch size is reached
                        if batch_size == 0:
                            yield file_obj
                        elif batch_size > 0:
                            batch.append(file_obj)
                            batch_progress = pbar.n/batch_size

                            if int(batch_progress) == batch_progress:
                                yield batch
                                batch = []

            # Yield the last batch
            if len(batch) > 0:
                yield batch

    def _apply_filters(self, file_path: str, filters: dict) -> bool:
        file = Path(file_path).resolve()
        if filters.get('exclude_str') and \
                set(os.path.normpath(str(file)).split(os.path.sep)) & set(filters['exclude_str']):
            return False
        if filters.get('include_str') and \
                not set(os.path.normpath(str(file)).split(os.path.sep)) & set(filters['include_str']):
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

    def identify_duplicates(self, report_file: str = None, filters: Optional[dict] = None,
                            threshold: int = 0, top_n: int = 3, use_abs_path: bool = False) -> None:
        """
        Generates a CSV ranking the most similar files in the provided directory.

        :param report_file: The path to the output CSV file. If none, then the data is returned.
        :param filters: A dictionary of filters to apply to the files. Extensions are restricted to pdf/docx/txt by default.
        :param threshold: The cutoff similarity score (0-1) to write to the report.
        :param top_n: The top n closest files to check for. Only compatible with threshold > 0.
        """

        # Pre-processing data
        data = [file.processor.__dict__ for file in self._file_generator(filters, True)]
        data = pd.json_normalize(data, max_level=1, sep='_')
        df = pd.DataFrame(data)

        if df.empty:
            raise EmptySelection(f'Filtered selection of files is empty. \
                            Please try a different directory, or new filters. \
                            Filters: {filters}, Path: {Path(self.path).resolve()}')
        elif not df.empty:
            df = df.get(['size', 'extension', 'file_name',
                        'metadata_text', 'absolute_path'])

        df['metadata_text'] = df['metadata_text'].str.strip()
        df['metadata_text'] = df['metadata_text'].str.replace('\n', '')

        # Only keeping pdf/docx/txt files with sufficiently long 'text' metadata
        df = df[(df['extension'].isin(['.pdf', '.docx', '.txt'])) &
                (df['metadata_text'].str.len() > 10) &
                (df['metadata_text'].notnull())]
        df = df.reset_index(drop=True)
        file_names = df.absolute_path if use_abs_path else df.file_name

        # Encoding
        encoder = SentenceTransformer("paraphrase-MiniLM-L3-v2")
        vectors = encoder.encode(df['metadata_text'])

        if threshold == 0:
            # Brute force search via cosine similarity
            similarities = 1 - cdist(vectors, vectors, 'cosine')
            similarities = np.around(similarities, decimals=2)
            sim_df = pd.DataFrame(data=similarities, columns=file_names.tolist(),
                                  index=file_names.tolist())

            sim_df.sort_index(axis=1, inplace=True)
            sim_df.sort_index(axis=0, inplace=True)

            sim_df.to_csv(report_file)

        elif threshold != 0:
            # Search via FAISS indexes
            vector_dimension = vectors.shape[1]
            index = faiss.IndexFlatIP(vector_dimension)
            index = faiss.IndexIDMap(index)
            faiss.normalize_L2(vectors)
            index.add_with_ids(vectors, df.index.values.astype(np.int64))
            similarities, similarities_ids = index.search(vectors, k=top_n+1)

            # Cleaning the data (removing matches with low measures of similarity)
            sim = pd.DataFrame(similarities).astype('float64').round(2)
            sim = sim.where(sim >= threshold).fillna('')
            sim_ids = pd.DataFrame(similarities_ids)
            sim_ids = sim_ids.where(sim != '', '')

            # Creating the output dataframe
            df_out = pd.DataFrame(file_names)
            for i in range(min(top_n, len(df.file_name))):
                df_out[f'{i+1}_file'] = sim_ids[i+1].map(file_names)
                df_out[str(i+1)] = sim[i+1]

            df_out = df_out.fillna('')
            df_out.to_csv(report_file)

    def generate_analytics(self, report_file: str = None, filters: Optional[dict] = None) -> dict:
        """
        Returns analytics (size and count) on the file types inside the directory.

        :param report_file: The path to the output CSV file. If none, then the data is returned.
        :param filters: A dictionary of filters to apply to the files.
        """

        data = [file.processor.__dict__ for file in self._file_generator(filters, False)]
        df = pd.DataFrame(data)

        if df.empty:
            raise EmptySelection(f'Filtered selection of files is empty. \
                            Please try a different directory, or new filters. \
                            Filters: {filters}, Path: {Path(self.path).resolve()}')

        df = df.get(['size', 'extension'])
        df['count'] = 1
        df = df.groupby('extension').sum()
        df['size'] = df['size'] / 1e6
        df.rename(columns={'size': 'size (MB)'}, inplace=True)

        if report_file:
            df.to_csv(report_file)

        return df.to_dict()

    def generate_report(self, report_file: str, include_text: bool = False, filters: Optional[dict] = None,
                        keywords: Optional[list] = None, check_title_keywords: Optional[bool] = False,
                        migrate_filters: Optional[dict] = None, open_files: bool = True, 
                        split_metadata: bool = False, char_limit: int = 3000, batch_size: int = 500, 
                        start_at: int = 0, recovery_mode: bool = False) -> None:
        """
        Generates a report of the directory and writes it to a CSV file.

        :param report_file: The path to the output CSV file.
        :param include_text: Whether to include the 'text' attribute in the metadata column.
        :param filters: A dictionary of filters to apply to the files.
        :param keywords: A list of keywords to count in the 'text' (and file_name) attribute of the metadata.
        :param check_title_keywords: Whether to check for keywords in the file_name field
        :param migrate_filters: A dictionary of filters to mark whether an item should be migrated (True) or not (False).
        :param open_files: Whether to open the files for extracting metadata. If False, files won't be opened.
        :param split_metadata: Whether to unpack the metadata dictionary into separate columns in the CSV file.
        :param char_limit: The cut-off length for each metadata field.
        :param batch_size: The maximum number of files per report. If exceeded, then additional reports are created.
        :param start_at: Start analyzing files starting at this index.
        :param recovery_mode: Continue building on the output report instead of rebuilding it.
        """

        # Crash recovery: auto-computing start_at index to see when to start processing
        if recovery_mode and os.path.isfile(report_file):
            df = pd.read_csv(report_file)
            start_at = len(df)

        with tqdm(desc='Processing batches', unit=' batches completed') as pbar:
            for index, batch in enumerate(self._file_generator(filters, open_files, start_at, batch_size)):
                # Extracting the attributes from the File object
                data = [file.processor.__dict__ for file in batch]

                # Imposing a character limit on each metadata property, or removing the verbose fields
                for file in data:
                    file.pop('open_file', None)
                    file['size'] = file['size'] / 1e6
                    if migrate_filters:
                        file['migrate'] = int(self._apply_filters(file['file_path'], migrate_filters))
                    if include_text and open_files:
                        file['metadata'] = {k: str(v)[:char_limit] for k, v in file['metadata'].items()}
                        if keywords and file['metadata'].get('text'):
                            file['keywords'] = self._count_keywords(file['metadata']['text'], keywords)
                        elif keywords:
                            file['keywords'] = self._count_keywords('', keywords)
                    elif not include_text:
                        for field in ['text', 'docstrings', 'imports', 'words', 'lines', 'data']:
                            file['metadata'].pop(field, None)
                    if check_title_keywords and keywords:
                        file['title_keywords'] = self._count_keywords(file['file_name'], keywords)

                # Unpacking the metadata field so each metadata property becomes its own column
                if split_metadata:
                    data = pd.json_normalize(data, max_level=1, sep='_')

                df = pd.DataFrame(data)

                if df.empty:
                    raise EmptySelection(f'Filtered selection of files is empty. \
                                    Please try a different directory, or new filters. \
                                    Filters: {filters}, Path: {Path(self.path).resolve()}')

                df.columns = df.columns.str.replace('metadata_', '')
                df.columns = df.columns.str.replace('title_keywords_', 'Title.')
                df.columns = df.columns.str.replace('keywords_', 'Text.')

                if not split_metadata:
                    df['metadata'] = df['metadata'].apply(json.dumps)

                # Converting booleans to integers (True->1; False->0)
                for boolean in ['is_file', 'is_symlink']:
                    df[boolean] = df[boolean].astype(int)

                # Converting unix time to datetime (GMT time)
                for time in ['modification_time', 'access_time', 'creation_time']:
                    df[time] = pd.to_datetime(df[time].round(0), unit='s')

                # Converting file permissions from number to string (ex '666' to 'Unrestricted')
                df['permissions'] = df['permissions'].apply(
                    lambda x: f'Unrestricted ({x})' if x in ['666', '777'] else f'Restricted ({x})')

                # df.replace(np.NaN, 'N/A', inplace=True)
                df.columns = df.columns.str.replace('_', ' ')
                df.columns = df.columns.str.title()
                df.rename(columns={'Size': 'Size (MB)'}, inplace=True)

                if index > 1:
                    report = pd.read_csv(report_file)
                    report = pd.concat([report, df], ignore_index=True)
                    report.to_csv(report_file, index=False)
                elif not recovery_mode:
                    df.to_csv(report_file, index=False)

                pbar.update(1)

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
