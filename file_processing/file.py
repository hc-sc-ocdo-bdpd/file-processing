from pathlib import Path
import pytesseract
from file_processing import processors
from file_processing.tools import FileProcessorStrategy, OCRDecorator, TranscriptionDecorator
from file_processing.tools.errors import TesseractNotFound, NotOCRApplicableError, NotTranscriptionApplicableError


class File:
    OCR_APPLICABLE_EXTENSIONS = {".pdf", ".jpeg", ".jpg", ".png", ".gif", ".tiff", ".tif"}
    TRANSCRIPTION_APPLICABLE_EXTENSIONS = {".mp3", ".wav", ".mp4", ".flac", ".aiff", ".ogg"}

    PROCESSORS = {
        ".csv": processors.CsvFileProcessor,
        ".txt": processors.TextFileProcessor,
        ".pdf": processors.PdfFileProcessor,
        ".docx": processors.DocxFileProcessor,
        ".msg": processors.MsgFileProcessor,
        ".pptx": processors.PptxFileProcessor,
        ".rtf": processors.RtfFileProcessor,
        ".html": processors.HtmlFileProcessor,
        ".xml": processors.XmlFileProcessor,
        ".png": processors.PngFileProcessor,
        ".xlsx": processors.XlsxFileProcessor,
        ".jpeg": processors.JpegFileProcessor,
        ".jpg": processors.JpegFileProcessor,
        ".json": processors.JsonFileProcessor,
        ".zip": processors.ZipFileProcessor,
        ".mp3": processors.AudioFileProcessor,
        ".wav": processors.AudioFileProcessor,
        ".mp4": processors.AudioFileProcessor,
        ".flac": processors.AudioFileProcessor,
        ".aiff": processors.AudioFileProcessor,
        ".ogg": processors.AudioFileProcessor,
        ".py": processors.PyFileProcessor,
        ".gif": processors.GifFileProcessor,
        ".tif": processors.TiffFileProcessor,
        ".tiff": processors.TiffFileProcessor,
        ".heic": processors.HeicFileProcessor,
        ".heif": processors.HeicFileProcessor
    }

    def __init__(self, path: str, use_ocr: bool = False, use_transcriber: bool = False, open_file: bool = True) -> None:
        self.path = Path(path)
        self.processor = self._get_processor(
            use_ocr, use_transcriber, open_file)
        self.process()

    def _get_processor(self, use_ocr: bool, use_transcriber: bool, open_file: bool) -> FileProcessorStrategy:
        extension = self.path.suffix
        processor_class = File.PROCESSORS.get(extension, processors.GenericFileProcessor)
        processor = processor_class(str(self.path), open_file)

        if use_ocr:
            if extension not in File.OCR_APPLICABLE_EXTENSIONS:
                raise NotOCRApplicableError(f"OCR is not applicable for file type {extension}.")

            try:
                pytesseract.get_tesseract_version()
            except Exception:
                raise TesseractNotFound("Tesseract is not installed or not added to PATH")

            return OCRDecorator(processor)

        if use_transcriber:
            if extension not in File.TRANSCRIPTION_APPLICABLE_EXTENSIONS:
                raise NotTranscriptionApplicableError(
                    f"Transcription is not applicable for file type {extension}.")

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
