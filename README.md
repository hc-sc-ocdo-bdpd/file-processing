# File Processing Library

This library contains tools for processing various file types for several purposes. This includes extracting metadata, calculating metrics between files such as cosine similarity and Levenshtein distance. This software is under active development.

## Dependencies

This project has dependencies defined in `requirements.txt`. These dependencies should be installed using `pip3 install -r depencencies.txt`. Older versions of pip may result in an error.

Additionally, this project uses tesseract for OCR. This must be installed at: `C:/Users/USERNAME/AppData/Local/Programs/Tesseract-OCR/tesseract.exe`. See https://github.com/UB-Mannheim/tesseract/wiki.

This project also uses ffmpeg for audio/video file transcripting. You can install it via PowerShell using the following steps: 
1. Install scoop: `iwr -useb get.scoop.sh | iex` 
2. Install ffmpeg: `scoop install ffmpeg`
3. It may be necessary to restart the IDE and computer after these installs have been completed

## Structure

This library contains several components in different directories:

- file_processing: utilities for opening a variety of different file types.
- utils: support functions for the file_processing components.
- tests: pytest test cases
- tests/resources: files used as inputs for tests.

These include file processing tools (in the file_processing directory). This code is structured as follows:

- `file_processing.File`: Entry point for processing a file. It selects the appropriate processor for a given file based on the file type.
- `utils.FileProcessorStrategy`: An abstract base class (ABC) for processing files. Subclasses must implement the `process` method.
- `file_processing.TextFileProcessor` and `PdfFileProcessor`: They inherit from `FileProcessorStrategy` and implement `process` method for .txt and .pdf files respectively.
- `file_processing.FileMetricStrategy`: An ABC for calculating metrics between files. Subclasses must implement the `calculate` method.
- `utils.CosineSimilarity` and `utils.LevenshteinDistance`: They inherit from `FileMetricStrategy` and implement the `calculate` method to compute cosine similarity and Levenshtein distance between files.
