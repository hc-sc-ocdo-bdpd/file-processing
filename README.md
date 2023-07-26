# File Processing Library

This library processes various file types, extracts metadata, and provides utility functions for calculating metrics between files. Currently, it supports processing of .txt and .pdf files and can calculate cosine similarity and Levenshtein distance.

## Dependencies
This project has dependencies defined in `requirements.txt`. These dependencies should be installed using `pip3 install -r depencencies.txt`. Older versions of pip may result in an error.

Additionally, this project uses tesseract for OCR. This must be installed at: `C:/Users/USERNAME/AppData/Local/Programs/Tesseract-OCR/tesseract.exe`. See https://github.com/UB-Mannheim/tesseract/wiki.

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

## Steps to setup testing Table Extraction features
- Download `Tesseract` and `MikTex` on laptop using the following links respectfully: https://github.com/UB-Mannheim/tesseract/wiki & https://miktex.org/download
- Search for `Environment Variable for your account` from the windows search bar
    - Select `Path` and then Edit
    - When the `Edit Environment variable` appears, select `New` and then paste the following line and replacing `USERNAME` with your personal username: C:\Users\USERNAME\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe
    - Select Ok on both the `Edit Environment variable` and the `Environment variable` windows;
- (Re)Create a new Environment for the File-Processing Tools on your local device:
    - Open `Command Palette` (under the View Tab);
    - Search and select `Python: Create Environment`;
    - Select `Venv` option;
- After completing Steps, close and re-open VScode and run `benchmark_pipeline.py` file