from pathlib import Path
from file_processing.txt_processor import TextFileProcessor
from file_processing.pdf_processor import PdfFileProcessor
from file_processing.docx_processor import DocxFileProcessor
from file_processing.ocr_decorator import OCRDecorator
from file_processing.msg_processor import MsgFileProcessor
from file_processing.png_processor import PngFileProcessor
from file_processing.xlsx_processor import xlsxFileProcessor
from file_processing.pptx_processor import PptxFileProcessor
from file_processing.rtf_processor import RtfFileProcessor
from file_processing.html_processor import HtmlFileProcessor
from file_processing.xml_processor import XmlFileProcessor
from file_processing.jpeg_processor import JpegFileProcessor
from file_processing.csv_processor import CsvFileProcessor
from file_processing.json_processor import JsonFileProcessor
from file_processing.zip_processor import ZipFileProcessor
from file_processing.audio_processor import AudioFileProcessor
from file_processing.transcription_decorator import TranscriptionDecorator
from file_processing.generic_processor import GenericFileProcessor
from file_processing.py_processor import PyFileProcessor
from file_processing.gif_processor import GifFileProcessor
from file_processing.tiff_processor import TiffFileProcessor
from file_processing.heic_processor import HeicFileProcessor
from file_processing.errors import UnsupportedFileTypeError, NotOCRApplciableError, NotTranscriptionApplicableError

class File:
    OCR_APPLICABLE_EXTENSIONS = {".pdf", ".jpeg", ".jpg", ".png", ".gif", ".tiff", ".tif"}
    TRANSCRIPTION_APPLICABLE_EXTENSIONS = {".mp3", ".wav", ".mp4", ".flac", ".aiff", ".ogg"}

    PROCESSORS = {
        ".csv": CsvFileProcessor,
        ".txt": TextFileProcessor,
        ".pdf": PdfFileProcessor,
        ".docx": DocxFileProcessor,
        ".msg": MsgFileProcessor,
        ".pptx": PptxFileProcessor,
        ".rtf": RtfFileProcessor,
        ".html": HtmlFileProcessor,
        ".xml": XmlFileProcessor,
        ".png": PngFileProcessor,
        ".xlsx": xlsxFileProcessor,
        ".jpeg": JpegFileProcessor,
        ".jpg": JpegFileProcessor,
        ".json": JsonFileProcessor,
        ".zip": ZipFileProcessor,
        ".mp3": AudioFileProcessor,
        ".wav": AudioFileProcessor,
        ".mp4": AudioFileProcessor,
        ".flac": AudioFileProcessor,
        ".aiff": AudioFileProcessor,
        ".ogg": AudioFileProcessor,
        ".py": PyFileProcessor,
        ".gif": GifFileProcessor,
        ".tif": TiffFileProcessor,
        ".tiff": TiffFileProcessor,
        ".heic": HeicFileProcessor,
        ".heif": HeicFileProcessor
    }

    def __init__(self, path: str, use_ocr: bool = False, use_transcriber: bool = False, open_file: bool = True) -> None:
        self.path = Path(path)
        self.processor = self._get_processor(use_ocr, use_transcriber, open_file)
        self.process()

    def _get_processor(self, use_ocr: bool, use_transcriber: bool, open_file: bool) -> 'FileProcessorStrategy':
        extension = self.path.suffix
        processor_class = File.PROCESSORS.get(extension, GenericFileProcessor)
        processor = processor_class(str(self.path), open_file)

        if use_ocr:
            if extension not in File.OCR_APPLICABLE_EXTENSIONS:
                raise NotOCRApplciableError(f"OCR is not applicable for file type {extension}.")
            return OCRDecorator(processor)
        
        if use_transcriber:
            if extension not in File.TRANSCRIPTION_APPLICABLE_EXTENSIONS:
                raise NotTranscriptionApplicableError(f"Transcription is not applicable for file type {extension}.")
            return TranscriptionDecorator(processor)

        return processor



    def save(self, output_path: str = None) -> None:
        self.processor.save(output_path)


    def process(self) -> None:
        return self.processor.process()

    
    @property
    def file_path(self) -> str:
        return self.processor.file_path


    @property
    def file_name(self) -> str:
        return self.processor.file_name


    @property
    def extension(self) -> str:
        return self.processor.extension

    @property
    def owner(self) -> str:
        return self.processor.owner

    @property
    def size(self) -> str:
        return self.processor.size

    @property
    def modification_time(self) -> str:
        return self.processor.modification_time

    @property
    def access_time(self) -> str:
        return self.processor.access_time

    @property
    def creation_time(self) -> str:
        return self.processor.creation_time
    
    @property
    def parent_directory(self) -> str:
        return self.processor.parent_directory
    
    @property
    def permissions(self) -> str:
        return self.processor.permissions
    
    @property
    def is_file(self) -> bool:
        return self.processor.is_file
    
    @property
    def is_symlink(self) -> bool:
        return self.processor.is_symlink

    @property
    def absolute_path(self) -> str:
        return self.processor.absolute_path

    @property
    def metadata(self) -> dict:
        return self.processor.metadata
