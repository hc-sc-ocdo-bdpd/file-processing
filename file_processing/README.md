# File Processing Extension Guide

## How Our Strategy Works

1. **Main File** ([`file.py`](./file.py)): Determines the file type based on its extension and delegates the processing to the appropriate processor.
2. **Strategy Base** ([`file_processor_strategy.py`](./file_processor_strategy.py)): An abstract base class that sets the foundation for all file processors.
3. **Specific File Processors** (like [`docx_processor.py`](./docx_processor.py), [`pdf_processor.py`](./pdf_processor.py), [`txt_processor.py`](./txt_processor.py)): Handle the unique processing for each file type. They inherit from the base strategy and implement the `process` method.
