

class FileProcessorError(Exception):
    """Base exception for the file processing library."""


class UnsupportedFileTypeError(FileProcessorError):
    """Raised when an unsupported file type is encountered."""


class FileProcessingFailedError(FileProcessorError):
    """Raised when there's a generic error during file processing."""


class FileCorruptionError(FileProcessorError):
    """Raised when the file is found to be corrupted."""

class EmptySelection(FileProcessorError):
    """Raised when the input directory is empty. This may be caused by the filter conditions."""


class NotDocumentBasedFile(KeyError):
    """Raised during file similarity testing when the input file does not have a 'text' field."""
