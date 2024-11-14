"""
file_processing: A versatile library for processing a variety of file types.

This package provides a unified interface through the `File` class, which dynamically
selects the appropriate file processor based on the file extension. Users can interact
with files of various types through this single interface, simplifying file handling,
metadata extraction, and data processing.

Exports:
    File: The main class for interacting with different file types in a unified way.
"""

from .file import File

__all__ = ['File']
