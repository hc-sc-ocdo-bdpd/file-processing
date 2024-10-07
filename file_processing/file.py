from pathlib import Path
from file_processing import processors
from file_processing.file_processor_strategy import FileProcessorStrategy
from file_processing.errors import (
    FileProcessingFailedError,
    TesseractNotFound,
    NotOCRApplicableError,
    NotTranscriptionApplicableError,
    OptionalDependencyNotInstalledError
)


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

    def __init__(self, path: str, use_ocr: bool = False, ocr_path: str = None, 
                 use_transcriber: bool = False, open_file: bool = True) -> None:
        self.path = Path(path)
        self.processor = self._get_processor(use_ocr, ocr_path, use_transcriber, open_file)
        self.process()

    def _get_processor(self, use_ocr: bool, ocr_path: str,
                       use_transcriber: bool, open_file: bool) -> FileProcessorStrategy:
        extension = self.path.suffix
        processor_class = File.PROCESSORS.get(extension, processors.GenericFileProcessor)
        processor = processor_class(str(self.path), open_file)

        if use_ocr:
            # Attempt to import the OCR library only when needed
            try:
                from file_processing_ocr.ocr_decorator import OCRDecorator
                import pytesseract

                if extension not in File.OCR_APPLICABLE_EXTENSIONS:
                    raise NotOCRApplicableError(f"OCR is not applicable for file type {extension}.")

                # Check for Tesseract installation
                if ocr_path:
                    pytesseract.pytesseract.tesseract_cmd = ocr_path

                pytesseract.get_tesseract_version()
            except ImportError:
                raise OptionalDependencyNotInstalledError("OCR functionality requires the 'file-processing-ocr' library. "
                                                          "Please install it using 'pip install file-processing-ocr'.")
            except Exception:
                raise TesseractNotFound(f"Tesseract is not installed or not added to PATH. Path: {pytesseract.pytesseract.tesseract_cmd}")

            return OCRDecorator(processor, ocr_path)

        if use_transcriber:
            from file_processing.decorators.transcription_decorator import TranscriptionDecorator

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
