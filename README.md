# File Processing Library

This library contains tools for processing various file types for several purposes. This includes extracting metadata, calculating metrics between files such as cosine similarity and Levenshtein distance, and table data extraction. This software is under active development.

## Dependencies

This project has dependencies defined in `requirements.txt`. These dependencies should be installed using `pip3 install -r depencencies.txt`. Older versions of pip may result in an error.

Additionally, this project uses tesseract for OCR. This must be installed at: `C:/Users/USERNAME/AppData/Local/Programs/Tesseract-OCR/tesseract.exe`. See https://github.com/UB-Mannheim/tesseract/wiki.

The table detection performance tests use MikTex (https://miktex.org/download) for generating artificial test case tables. This needs to be installed at it's default location (C:\Users\USERNAME\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe).

## Running the Table Extraction Tool
There are two versions of the table extraction tool: a command line version and a graphical version which runs in a web browswer.

- Command line version implementation: table_processing/Table_processor_main.py
- GUI version: table_processing/GUI.py

## Structure

This library contains several components in different directories:

- file_processing: Utilities for opening a variety of different file types.
- utils: support functions for the file_processing components.
- resources: files used as inputs for various components of the software.
- table_processing: Table extraction tools
- tests: pytest test cases
- src: contains deprecated software from an earlier version of this library. This directory is planned for removal as it is being replaced with file_processing tools
- table_trials_results: Results in .xlsx format of the tests run on generated tables with a variety of randomized parameters including rows, columns, vertical/horizontal lines, font size, row height, margin, orientation, and special characters. Parameter values and performance metrics are tracked for each of the roughly 7000 generated tables along with overall summaries for each individual metric (mean, stdev, min, max, median, etc.). Running these table generation tests starts in the benchmark_pipeline.py script which calls the GeneratedTable, Table_Detector, & Table classes. When this script calls the GeneratedTable class, its parameters can be customized to fit whatever test is needed to run. Once all the results have been exported, named appropriately, and placed in the table_trials_results directory, the metrics_results.py script can be run which combines all the results into the table_metrics_ALL.xlsx file. This sheet holds data for each individual table, a summary of all the metrics, the results grouped by each different combination of the parameters, and the results grouped by every individual value of every parameter. This facilitates the analysis to discern on which parameters (and specific combination of parameters) the table extraction model performs well and poorly.

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
