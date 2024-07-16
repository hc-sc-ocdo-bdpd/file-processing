import sys
import io
from pathlib import Path
import getpass
import pypdf
import pytesseract
from PIL import Image
from file_processing.tools import FileProcessorStrategy
from file_processing.tools.errors import OCRProcessingError

try:
    pytesseract.get_tesseract_version()
except:
    if sys.platform == 'win32':
        pytesseract.pytesseract.tesseract_cmd = Path('C:/Users') / \
        getpass.getuser() / 'AppData/Local/Programs/Tesseract-OCR/tesseract.exe'
    elif sys.platform == 'linux':
        pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'


class OCRDecorator:
    def __init__(self, processor: FileProcessorStrategy, ocr_path: str) -> None:
        """Initializes the OCRDecorator with a given file processor."""
        if ocr_path:
            pytesseract.pytesseract.tesseract_cmd = ocr_path

        self._processor = processor

    def process(self) -> None:
        """Processes the file using the wrapped processor and then applies OCR."""
        self._processor.process()
        ocr_text = self.extract_text_with_ocr()
        self._processor.metadata['ocr_text'] = ocr_text

    def extract_text_with_ocr(self) -> str:
        """Extracts text from the file using OCR.

        Returns:
            str: The extracted text.
        """
        extension = self._processor.extension

        if extension == ".pdf":
            return self._ocr_pdf()
        else:
            return self._ocr_image()

    def _ocr_image(self) -> str:
        try:
            ocr_result = pytesseract.image_to_string(str(self._processor.file_path))
            return ocr_result
        except Exception as e:
            raise OCRProcessingError(f"Error during OCR processing: {e}")

    def _ocr_pdf(self) -> str:
        text = ''
        ocr_text = ''

        try:
            with open(self._processor.file_path, 'rb') as pdf_file_obj:
                reader = pypdf.PdfReader(pdf_file_obj)
                num_pages = len(reader.pages)

                start_page = 0
                end_page = num_pages

                for i in range(start_page, end_page):
                    page_obj = reader.pages[i]

                    text += page_obj.extract_text()

                    for image in page_obj.images:
                        ocr_text += pytesseract.image_to_string(
                            Image.open(io.BytesIO(image.data)))

                # Combine the extracted text and OCR text
                combined_text = text + "\n" + ocr_text
                return combined_text

        except Exception as e:
            raise OCRProcessingError(f"Error during OCR processing: {e}")

    @property
    def file_name(self) -> str:
        """Returns the file name of the processed file."""
        return self._processor.file_name

    @property
    def extension(self) -> str:
        """Returns the file extension of the processed file."""
        return self._processor.extension

    @property
    def owner(self) -> str:
        """Returns the owner of the processed file."""
        return self._processor.owner

    @property
    def size(self) -> str:
        """Returns the size of the processed file."""
        return self._processor.size

    @property
    def modification_time(self) -> str:
        """Returns the modification time of the processed file."""
        return self._processor.modification_time

    @property
    def access_time(self) -> str:
        """Returns the access time of the processed file."""
        return self._processor.access_time

    @property
    def creation_time(self) -> str:
        """Returns the creation time of the processed file."""
        return self._processor.creation_time

    @property
    def parent_directory(self) -> str:
        """Returns the parent directory of the processed file."""
        return self._processor.parent_directory

    @property
    def permissions(self) -> str:
        """Returns the permissions of the processed file."""
        return self._processor.permissions

    @property
    def is_file(self) -> bool:
        """Returns True if the processed file is a regular file."""
        return self._processor.is_file

    @property
    def is_symlink(self) -> bool:
        """Returns True if the processed file is a symbolic link."""
        return self._processor.is_symlink

    @property
    def absolute_path(self) -> str:
        """Returns the absolute path of the processed file."""
        return self._processor.absolute_path

    @property
    def metadata(self) -> dict:
        """Returns the metadata of the processed file."""
        return self._processor.metadata