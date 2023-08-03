# File Processing Library

This library contains tools for processing various file types for several purposes. This includes extracting metadata, calculating metrics between files such as cosine similarity and Levenshtein distance, and table data extraction. This software is under active development.

## Dependencies
This project has dependencies defined in `requirements.txt`. These dependencies should be installed using `pip3 install -r depencencies.txt`. Older versions of pip may result in an error.

Additionally, this project uses tesseract for OCR. This must be installed at: `C:/Users/USERNAME/AppData/Local/Programs/Tesseract-OCR/tesseract.exe`. See https://github.com/UB-Mannheim/tesseract/wiki.

The table detection performance tests use MikTex (https://miktex.org/download) for generating artificial test case tables. This needs to be installed at it's default location (C:\Users\USERNAME\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe).

## Structure

This library contains several components in different directories:

- file_processing: Utilities for opening a variety of different file types.
- utils: support functions for the file_processing components.
- resources: files used as inputs for various components of the software.
- table_processing: Table extraction tools
- tests: pytest test cases
- src: contains deprecated software from an earlier version of this library. This directory is planned for removal as it is being replaced with file_processing tools

These include file processing tools (in the file_processing directory). This code is structured as follows:

- `file_processing.File`: Entry point for processing a file. It selects the appropriate processor for a given file based on the file type.
- `utils.FileProcessorStrategy`: An abstract base class (ABC) for processing files. Subclasses must implement the `process` method.
- `file_processing.TextFileProcessor` and `PdfFileProcessor`: They inherit from `FileProcessorStrategy` and implement `process` method for .txt and .pdf files respectively.
- `file_processing.FileMetricStrategy`: An ABC for calculating metrics between files. Subclasses must implement the `calculate` method.
- `utils.CosineSimilarity` and `utils.LevenshteinDistance`: They inherit from `FileMetricStrategy` and implement the `calculate` method to compute cosine similarity and Levenshtein distance between files.
- `table_processing.Table_Detector`: Entry point for the table processing tools.
- `table_processing.benchmark_pipeline`: Performance testing pipeline for the table_processing components.

## Things To Do

- [ ] Migrate this list to project milestones and issues
- [ ] Extend `FileProcessorStrategy` to include more detailed metadata
- [ ] Replace `print` statements with `logging` module
- [ ] Implement OCR functionality for processing image-based PDF files
- [ ] Integrate table extraction functionality
- [ ] Add docstrings and type hinting to all classes and methods
- [ ] Write tests to ensure the functionality of the library
- [ ] Add support for more file types (.docx, .xlsx, .pptx, etc.)
- [ ] Add more metrics for comparison between files (ex. jaccard)
