import pytest
import sys, os
sys.path.append(os.path.join(sys.path[0],'file_processing'))
from file_processing.file import File

# To do: fix test_save_png_metadata
# Refactor invalid_save_location and _corrupted_file_processing

variable_names = "path, original_format, mode, width, height"
values = [
   ('tests/resources/test_files/Health_Canada_logo.png', 'GIF', 'P', 303, 40),
   ('tests/resources/test_files/MapCanada.png', 'PNG', 'RGBA', 3000, 2408)
]


@pytest.mark.parametrize(variable_names, values)
def test_png_metadata(path, original_format, mode, width, height):
    file_obj = File(path)
    assert file_obj.metadata['original_format'] == original_format
    assert file_obj.metadata['mode'] == mode
    assert file_obj.metadata['width'] == width
    assert file_obj.metadata['height'] == height

@pytest.mark.usefixtures('copy_file')
@pytest.mark.parametrize(variable_names, values)
def test_save_png_metadata(copy_file, original_format, mode, width, height):
        png = File(copy_file)
        png.save()
        test_png_metadata(copy_file, original_format, mode, width, height)


def test_png_invalid_save_location():
    import pytest
    from file_processing.file import File
    from errors import FileProcessingFailedError
    
    png_file = File('tests/resources/test_files/Health_Canada_logo.png')
    with pytest.raises(FileProcessingFailedError):
        png_file.processor.save('/non_existent_folder/Health_Canada_logo.png')

def test_png_corrupted_file_processing():
    import pytest
    from file_processing.file import File
    from errors import FileProcessingFailedError
    with pytest.raises(FileProcessingFailedError) as exc_info:
        File("tests/resources/test_files/MapCanada_corrupted.png")