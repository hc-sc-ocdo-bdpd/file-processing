import pytest
from pathlib import Path
from file_processing.file import File
from file_processing.generic_processor import GenericFileProcessor


unsupported_files = [
    'tests/resources/test_files/unsupported_file_1.xyz',
    'tests/resources/test_files/unsupported_file_2.abcd'
]


@pytest.mark.parametrize("file_path", unsupported_files)
def test_processor_is_generic(file_path):
    file_obj = File(file_path)
    assert isinstance(file_obj.processor, GenericFileProcessor)


@pytest.mark.parametrize("file_path", unsupported_files)
def test_metadata_has_message(file_path):
    file_obj = File(file_path)
    assert 'message' in file_obj.processor.metadata
    assert file_obj.processor.metadata['message'] == "This is a generic processor. Limited functionality available. File was not opened"


@pytest.mark.parametrize("file_path", unsupported_files)
def test_file_attributes(file_path):
    file_obj = File(file_path)
    processor = file_obj.processor

    assert processor.file_path == Path(file_path)
    assert processor.file_name == Path(file_path).name
    assert processor.extension == Path(file_path).suffix
    assert processor.size == Path(file_path).stat().st_size
    assert processor.modification_time == Path(file_path).stat().st_mtime
    assert processor.access_time == Path(file_path).stat().st_atime
    assert processor.creation_time == Path(file_path).stat().st_ctime
    assert processor.parent_directory == Path(file_path).parent
    assert processor.is_file == Path(file_path).is_file()
    assert processor.is_symlink == Path(file_path).is_symlink()
    assert processor.absolute_path == Path(file_path).resolve()
