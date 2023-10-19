

class FileProcessorError(Exception):
    """Base exception for the file processing library."""
    pass



class UnsupportedFileTypeError(FileProcessorError):
    """Raised when an unsupported file type is encountered."""
    pass

class FileProcessingFailedError(FileProcessorError):
    """Raised when there's a generic error during file processing."""
    pass

class FileCorruptionError(FileProcessorError):
    """Raised when the file is found to be corrupted."""
    pass



class OCRError(FileProcessorError):
    """Base exception for OCR related issues."""
    pass

class OCRProcessingError(OCRError):
    """Raised when there's an issue during OCR processing."""
    pass

class NotOCRApplciableError(OCRError):
    """Raised when attempting OCR on a file type that doesn't support it."""
    pass