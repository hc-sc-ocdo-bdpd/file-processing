# File Processing Library

This library processes various file types, extracts metadata, and provides utility functions for calculating metrics between files. Currently, it supports processing of .txt and .pdf files and can calculate cosine similarity and Levenshtein distance.

## Structure

The main classes in this library are:

- `File`: Entry point for processing a file. It selects the appropriate processor for a given file based on the file type.
- `FileProcessorStrategy`: An abstract base class (ABC) for processing files. Subclasses must implement the `process` method.
- `TextFileProcessor` and `PdfFileProcessor`: They inherit from `FileProcessorStrategy` and implement `process` method for .txt and .pdf files respectively.
- `FileMetricStrategy`: An ABC for calculating metrics between files. Subclasses must implement the `calculate` method.
- `CosineSimilarity` and `LevenshteinDistance`: They inherit from `FileMetricStrategy` and implement the `calculate` method to compute cosine similarity and Levenshtein distance between files.

## Things To Do

- [ ] Extend `FileProcessorStrategy` to include more detailed metadata
- [ ] Replace `print` statements with `logging` module
- [ ] Implement OCR functionality for processing image-based PDF files
- [ ] Integrate table extraction functionality
- [ ] Add docstrings and type hinting to all classes and methods
- [ ] Write tests to ensure the functionality of the library
- [ ] Add support for more file types (.docx, .xlsx, .pptx, etc.)
- [ ] Add more metrics for comparison between files (ex. jaccard)


