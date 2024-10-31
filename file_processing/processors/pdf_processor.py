from pypdf import PdfReader, PdfWriter
from pypdf.errors import PdfReadError
from file_processing.errors import FileProcessingFailedError
from file_processing.file_processor_strategy import FileProcessorStrategy


class PdfFileProcessor(FileProcessorStrategy):
    def __init__(self, file_path: str, open_file: bool = True) -> None:
        super().__init__(file_path, open_file)
        self.metadata = {'message': 'File was not opened'} if not open_file else self._default_metadata()

    def _default_metadata(self) -> dict:
        return {
            'text': None,
            'has_password': False
        }

    def process(self) -> None:
        reader = None
        metadata = {}

        if not self.open_file:
            return

        try:
            reader = PdfReader(self.file_path)
        except Exception as e:
            raise FileProcessingFailedError(
                f"Error encountered while opening {self.file_path}: {e}")

        if not reader.is_encrypted:
            if reader:
                metadata = reader.metadata

            # Use self.extract_text_from_pdf as an instance method
            self.metadata.update({
                'text': self.extract_text_from_pdf(reader),
                'author': str(metadata.get('/Author')),
                'producer': str(metadata.get('/Producer'))
            })
        else:
            self.metadata['has_password'] = True

    def save(self, output_path: str = None) -> None:
        output_path = output_path or self.file_path

        try:
            pdf_read = PdfReader(self.file_path)
            if pdf_read.is_encrypted:
                raise FileProcessingFailedError(
                    f"Cannot save encrypted PDF {self.file_path} without password."
                )
            pdf = PdfWriter()
            for page in pdf_read.pages:
                pdf.add_page(page)

            with open(output_path, 'wb') as output_pdf:
                pdf.write(output_pdf)
        except Exception as e:
            raise FileProcessingFailedError(
                f"Error encountered while saving to {output_path}: {e}"
            )

    def extract_text_from_pdf(self, reader: PdfReader) -> str:
        try:
            text = ""
            for page_number, page in enumerate(reader.pages, start=1):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text
                except UnboundLocalError as e:
                    # Log the error and continue with the next page
                    print(f"Warning: Failed to extract text from page {page_number} in {self.file_path}: {e}")
                    continue
            return text
        except Exception as e:
            raise FileProcessingFailedError(
                f"Error encountered while extracting text from {self.file_path}: {e}"
            )