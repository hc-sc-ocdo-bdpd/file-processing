class FileProcessorError(Exception):
    """
    Base exception for the file processing library.

    All custom exceptions related to file processing should inherit from this class.
    """


class UnsupportedFileTypeError(FileProcessorError):
    """
    Raised when an unsupported file type is encountered.

    This error indicates that a specific file type does not have a processor available
    in the library and cannot be processed.
    """


class FileProcessingFailedError(FileProcessorError):
    """
    Raised when there's a generic error during file processing.

    This error serves as a catch-all for issues that occur during file handling,
    reading, or writing processes.
    """


class FileCorruptionError(FileProcessorError):
    """
    Raised when the file is found to be corrupted.

    Indicates that the file cannot be processed due to corruption or unreadable content.
    """


class OCRError(FileProcessorError):
    """
    Base exception for OCR-related issues.

    Any OCR-specific error should inherit from this class.
    """


class OCRProcessingError(OCRError):
    """
    Raised when there's an issue during OCR processing.

    This error typically occurs when OCR processing fails due to issues with the file format
    or OCR library functions.
    """


class NotOCRApplicableError(OCRError):
    """
    Raised when attempting OCR on a file type that doesn't support it.

    This error indicates that OCR cannot be applied to the specified file format.
    """


class TranscriptionError(FileProcessorError):
    """
    Base exception for transcription-related issues.

    Any transcription-specific error should inherit from this class.
    """


class TranscriptionProcessingError(TranscriptionError):
    """
    Raised when there's an issue during transcription processing.

    This error typically occurs when transcription fails due to issues with the file format
    or transcription library functions.
    """


class NotTranscriptionApplicableError(TranscriptionError):
    """
    Raised when attempting transcription on a file type that doesn't support it.

    This error indicates that transcription cannot be applied to the specified file format.
    """


class TesseractNotFound(Exception):
    """
    Raised when Tesseract is either not installed or not added to PATH.

    This error occurs if OCR processing is requested but Tesseract OCR is not available.
    """


class OptionalDependencyNotInstalledError(FileProcessorError):
    """
    Raised when an optional dependency is not installed but is required.

    Indicates that a required library for a specific feature, like OCR or transcription, 
    is missing from the environment.
    """


class EmptySelection(FileProcessorError):
    """
    Raised when the input directory is empty, possibly due to filter conditions.

    This error is typically raised when a directory expected to contain files does not
    contain any files that match the criteria.
    """


class NotDocumentBasedFile(KeyError):
    """
    Raised during file similarity testing when the input file does not have a 'text' field.

    This error indicates that the required 'text' data is missing for document-based
    similarity operations.
    """


class FAISSIndexError(Exception):
    """
    Base exception for FAISS-related issues.

    All FAISS-specific errors should inherit from this class.
    """


class UnsupportedHyperparameterError(FAISSIndexError):
    """
    Raised when a hyperparameter value cannot be used in the FAISS index.

    This error is typically raised if a specified hyperparameter is not supported by
    the FAISS indexing algorithm.
    """
