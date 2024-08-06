import os
import re
import json
import numpy as np
import pandas as pd
from typing import List
from tqdm import tqdm
from langchain.text_splitter import RecursiveCharacterTextSplitter
from file_processing import Directory
from file_processing import faiss_index
from file_processing.tools.errors import FileTypeError
from file_processing.tools.errors import EncodingModelError
from sentence_transformers import SentenceTransformer

class SearchDirectory:
    def __init__(self, folder_path: str):
        self.folder_path = folder_path
        # get chunking file path
        if os.path.exists(os.path.join(self.folder_path, "data_chunked.csv")):
            self.chunks_path = os.path.join(self.folder_path, "data_chunked.csv")
        else:
            self.chunks_path = None
        # get json data
        if os.path.exists(os.path.join(self.folder_path, "setup_data.json")):
            with open(os.path.join(self.folder_path, "setup_data.json"), 'r') as f:
                setup_data = json.load(f)
                self.encoding_name = setup_data['encoding_model']
                self.n_chunks = setup_data['number_of_chunks']
        else:
            self.n_chunks = None
            self.encoding_name = None
        # get the faiss index
        if os.path.exists(os.path.join(self.folder_path, "index.faiss")):
            self.index = faiss_index.load_index(os.path.join(self.folder_path, "index.faiss"))
        else:
            self.index = None
        # load the encoding model
        if self.encoding_name is not None:
            self.load_embedding_model(self.encoding_name)
        else:
            self.encoder = None

    def _get_text_chunks(self, text: str, chunk_size: int, chunk_overlap: int) -> List[str]:
        chunks = []
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        for chunk in splitter.split_text(text):
            chunks.append(chunk)
        return chunks
    
    def _embed_string(self, text: str):
        embedding = self.encoder.encode(text)
        return embedding
    
    def _save_to_json(self):
        setup_data = {
            'encoding_model': self.encoding_name,
            'number_of_chunks': self.n_chunks
        }
        with open(os.path.join(self.folder_path, "setup_data.json"), 'w') as f:
            json.dump(setup_data, f, indent=4)

    def _combine_embeddings(self):
        batch_path = os.path.join(self.folder_path, "embedding_batches")
        pattern = r"\((\d+)-(\d+)\)"

        file_ranges = []

        for filename in os.listdir(batch_path):
            match = re.search(pattern, filename)
            file_ranges.append((filename, int(match.group(1)), int(match.group(2))))

        file_ranges.sort(key=lambda x: x[1])

        if file_ranges[0][1] == 0:
            start = 0
            for filename, batch_start, batch_end in file_ranges:
                emb = np.load(os.path.join(batch_path, filename))
                if batch_start == 0:
                    emb_full = emb
                else:
                    if start >= batch_start:
                        emb_full = np.vstack((emb_full, emb[start - batch_start:]))
                start = batch_end
            if emb_full.shape[0] == self.n_chunks:
                np.save(os.path.join(self.folder_path, "embeddings.npy"), emb_full)
                print("Embeddings combined and saved to embeddings.npy")
        else:
            print("Embeddings not yet combined. The remainder of the embeddings left must be completed before they can be combined.")

    def _check_for_embeddings(self, embeddings: np.ndarray) -> np.ndarray:
        if embeddings is None:
            if os.path.exists(os.path.join(self.folder_path, "embeddings.npy")):
                embeddings = np.load(os.path.join(self.folder_path, "embeddings.npy"))
            else:
                raise FileNotFoundError("No embeddings found.")
        return embeddings
    
    def load_embedding_model(self, model_name: str = "paraphrase-MiniLM-L3-v2"):
        self.encoding_name = model_name
        self.encoder = SentenceTransformer(model_name)
        self._save_to_json()

    def report_from_directory(self, directory_path: str) -> None:
        directory = Directory(directory_path)
        directory.generate_report(
            report_file = os.path.join(self.folder_path,"report.csv"),
            split_metadata=True,
            include_text=True,
        )

    def chunk_text(self,
                   input_file_path: str = None,
                   document_path_column: str = "File Path",
                   document_text_column: str = "Text",
                   chunk_size: int = 1024,
                   chunk_overlap: int = 10):
        
        # check if there is a report
        if input_file_path is None:
            if os.path.exists(os.path.join(self.folder_path, "report.csv")):
                input_file_path = os.path.join(self.folder_path, "report.csv")
            else:
                raise FileNotFoundError("No input file specified and no report provided. \
                                        Please provide a file path to a .csv or run 'report_from_directory'.")

        # load into a dataframe
        if input_file_path.lower().endswith('.csv'):
            df = pd.read_csv(input_file_path)
        else:
            raise FileTypeError(f"File path {input_file_path} is not a .csv file.")
        
        # check if the column names are valid
        if document_path_column not in df.columns:
            raise KeyError(f"'{document_path_column}' is not a column in {input_file_path}.")
        elif document_text_column not in df.columns:
            raise KeyError(f"'{document_text_column}' is not a column in {input_file_path}.")

        # Initialize an empty list to collect all rows
        all_new_rows = []

        # Get the total number of rows
        total_rows = len(df)
        print(f"Total rows (excluding header): {total_rows}")

        # Process each row with tqdm to show progress
        for index, row in tqdm(df.iterrows(), total=total_rows, desc="Processing rows"):
            file_path = row[document_path_column]
            content = row[document_text_column]
            
            # Get chunks for the current content
            chunks = self._get_text_chunks(content, chunk_size, chunk_overlap)
            
            # Create new rows for each chunk
            for chunk_text in chunks:
                new_row = {
                    'file_path': file_path,
                    'content': chunk_text
                }
                all_new_rows.append(new_row)

        # Create a new DataFrame from the collected new rows
        chunked_df = pd.DataFrame(all_new_rows)

        # Save the new DataFrame to a new CSV file
        chunked_df.to_csv(os.path.join(self.folder_path, 'data_chunked.csv'), index=False)
        self.chunks_path = os.path.join(self.folder_path, 'data_chunked.csv')
        self.n_chunks = len(chunked_df)
        self._save_to_json()

        print("Chunking complete and saved to 'data_chunked.csv'.")

    def embed_text(self, row_start: int = 0, row_end: int = None, batch_size: int = 1000) -> None:
        if self.chunks_path is None:
            raise FileNotFoundError(f"Error: data_chunked.csv not located in {self.folder_path}")
        if self.encoder is None:
            raise EncodingModelError("Error: no encoding model found. Run 'load_embedding_model' first.")
        else:
            os.makedirs(os.path.join(self.folder_path, "embedding_batches"), exist_ok=True)
            chunked_df = pd.read_csv(self.chunks_path)
            n_chunks = len(chunked_df)

            if (row_end is None) or (row_end > n_chunks):
                row_end = n_chunks

            # handle index error values and negative indexes
            if row_start < -n_chunks - 1:
                raise IndexError(f"Row start {row_start} is out of bounds for {n_chunks} chunks.")
            elif row_start < 0:
                row_start = n_chunks + row_start + 1
            if row_end < -n_chunks -1:
                raise IndexError(f"Row end {row_end} is out of bounds for {n_chunks} chunks.")
            elif row_end < 0:
                row_end = n_chunks + row_end +1
            if row_start >= n_chunks:
                raise IndexError(f"Start index of {row_start} is out of bounds for {n_chunks} chunks")
            if row_end <= row_start:
                raise ValueError(f"Row end ({row_end}) cannot be less than the row start ({row_start}).")
        
            batch_path = os.path.join(self.folder_path, "embedding_batches")
            pattern = r"\((\d+)-(\d+)\)"

            contained_ranges = []

            for filename in os.listdir(batch_path):
                match = re.search(pattern, filename)
                batch_start = int(match.group(1))
                batch_end = int(match.group(2))
                if (batch_start < row_end) and (batch_end > row_start):
                    if batch_start < row_start:
                        batch_start = row_start
                    if batch_end > row_end:
                        batch_end = row_end
                    contained_ranges.append((batch_start, batch_end))
            
            contained_ranges.sort(key=lambda x: x[1])

            segments = []
            for batch_start, batch_end in contained_ranges:
                print(row_start)
                if row_start < row_end:
                    if (batch_start > row_start):
                        segments.append((row_start, batch_start))
                    row_start = batch_end
            if row_start < row_end:
                segments.append((row_start, row_end))

            for start, end in segments:
                current_row = start

                while current_row < end:
                    df = chunked_df[current_row:min(end, current_row + batch_size)]

                    tqdm.pandas()
                    embeddings = np.array(df['content'].progress_apply(self._embed_string).to_list())

                    # Save the new DataFrame to a new CSV file
                    np.save(os.path.join(self.folder_path, f"embedding_batches/embeddings ({current_row}-{min(end, current_row + batch_size)}).npy"), embeddings)
                    print(f"Embedding batch complete and saved to embeddings ({current_row}-{min(end, current_row + batch_size)}).npy').")
                    current_row += batch_size

            self._combine_embeddings()

    def create_flat_index(self, embeddings: np.ndarray = None):
        embeddings = self._check_for_embeddings(embeddings)
        self.index = faiss_index.create_flat_index(embeddings, file_path=os.path.join(self.folder_path, "index.faiss"))

    def create_ivf_flat_index(self, embeddings: np.ndarray = None, nlist: int = None):
        embeddings = self._check_for_embeddings(embeddings)
        self.index = faiss_index.create_IVF_flat_index(embeddings, nlist=nlist, file_path=os.path.join(self.folder_path, "index.faiss"))

    def create_hnsw_index(self,
                          embeddings: np.ndarray = None,
                          M: int = 64,
                          efConstruction: int = 64):
        embeddings = self._check_for_embeddings(embeddings)
        self.index = faiss_index.create_HNSW_index(embeddings, M=M, efConstruction=efConstruction, file_path=os.path.join(self.folder_path, "index.faiss"))

    def search(self, query: str, k: int = 1, *args):
        if self.chunks_path is None:
            raise FileNotFoundError(f"Error: data_chunked.csv not located in {self.folder_path}")
        if self.index is None:
            raise FileNotFoundError(f"Error: no FAISS index found in {self.folder_path}")
        if self.encoder is None:
            raise EncodingModelError("Error: no encoding model found. Run 'load_embedding_model' first.")
        xq = np.expand_dims(self._embed_string(query), axis=0)
        df = pd.read_csv(os.path.join(self.folder_path, 'data_chunked.csv'))
        _, indexes = self.index.query(xq, k, *args)
        return df.iloc[indexes[0]]
