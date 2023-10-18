
class FileProcessorError(Exception):
    """Base exception for the file processing library."""
    pass


class UnsupportedFileTypeError(FileProcessorError):
    """Raised when an unsupported file type is encountered."""
    pass


class FileProcessingFailedError(FileProcessorError):
    """Raised when there's a generic error during file processing."""
    pass

