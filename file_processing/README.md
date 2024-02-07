# File Processing Extension Guide



## How Our Strategy Works

1. **Main File** ([`file.py`](./file.py)): Determines the file type based on its extension and delegates the processing to the appropriate processor.
2. **Strategy Base** ([`file_processor_strategy.py`](./file_processor_strategy.py)): An abstract base class that sets the foundation for all file processors.
3. **Specific File Processors** (like [`docx_processor.py`](./docx_processor.py), [`pdf_processor.py`](./pdf_processor.py), [`txt_processor.py`](./txt_processor.py)): Handle the unique processing for each file type. They inherit from the base strategy and implement the `process` method.



## Steps to Extend Support for Additional File Types 

**Note**: The following is an example for adding support for `.html` files. When adding a new file type, ensure you follow the structure and conventions of existing file types (like `docx`, `pdf`, `txt`).

### 1. Create or Update Your File Processor

- Check if the processor for your file type, e.g., [`html_processor.py`](./html_processor.py), exists. If not, create it.
- Import the `FileProcessorStrategy` class.
- Define a class, for example, `HtmlFileProcessor`, inheriting from `FileProcessorStrategy`.
- Implement the abstract `process` method specific to your file type.



### 2. Update the Main File

- Import your processor at the top of [`file.py`](./file.py).
- Add the newly supported file extension and processor to the `PROCESSORS` dictionary.


### Important Notes

- **Avoid Modifying** [`file_processor_strategy.py`](./file_processor_strategy.py): This file is generic and shouldn't be tailored for specific file types.
- **Abstract Method**: The `process` method in the base strategy is abstract, meaning every specific file processor must provide its own implementation.


## Testing Your Extension

When extending the library, it's crucial to add tests to ensure everything works seamlessly.

1. **Add Tests**: Incorporate your tests into [`tests/file_test.py`](./tests/file_test.py). You can look at tests for other file types in the same file for guidance.
2. **Test Files**: Add two test files of the relevant file type to [`tests/resources/test_files`](./tests/resources/test_files). These files should be thorough and represent a wide range of content. For instance, a `.pptx` might include images, tables, etc.
3. **All Tests Must Pass**: Before submitting a PR, ensure all tests in the library pass.
4. **Unique Attributes**: Tests should be specific to the unique attributes of the file. For example, a `.pptx` might have a `num_slides` attribute and test.

Remember, the content of the test files can be broad (e.g., pull something from Wikipedia), but they should be thorough in terms of the file's features.


## Templates Available

Templates for the following file types might already exist. Use them as starting points if needed:

- html
- jpeg
- json
- msg
- png
- pptx
- pst
- rtf
- xml
- csv
- xlsx