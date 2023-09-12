class OCRDecorator:
    def __init__(self, processor):
        """Initializes the OCRDecorator with a given file processor."""
        self._processor = processor

    def process(self):
        """Processes the file using the wrapped processor and then applies OCR."""
        self._processor.process()
        ocr_text = self.extract_text_with_ocr()
        if 'text' in self._processor.metadata:
            self._processor.metadata['text'] += ocr_text
        else:
            self._processor.metadata['text'] = ocr_text

    def extract_text_with_ocr(self):
        """Extracts text from the file using OCR.

        Returns:
            str: The extracted text.
        """
        # TODO: Implement OCR extraction logic here
        pass

    @property
    def file_name(self):
        """Returns the file name of the processed file."""
        return self._processor.file_name

    @property
    def metadata(self):
        """Returns the metadata of the processed file."""
        return self._processor.metadata
