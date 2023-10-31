import pytest
import sys, os
sys.path.append(os.path.join(sys.path[0],'file_processing'))
from file_processing.file import File

#To do: Fix test_html_corrupted_file_processing

variable_names = "path, text_length, num_lines, num_words"
values = [
   ('tests/resources/test_files/Health - Canada.ca.html', 165405, 3439, 11162)
]


@pytest.mark.parametrize(variable_names, values)
def test_html_metadata(path, text_length, num_lines, num_words):
    file_obj = File(path)
    assert len(file_obj.metadata['text']) == text_length
    assert file_obj.metadata['num_lines'] == num_lines
    assert file_obj.metadata['num_words'] == num_words



@pytest.mark.parametrize(variable_names, values)
def test_save_html_metadata(copy_file, text_length, num_lines, num_words):
        html = File(copy_file)
        html.save()
        test_html_metadata(copy_file, text_length, num_lines, num_words)

@pytest.mark.parametrize("path", map(lambda x: x[0], values))
def test_html_invalid_save_location(invalid_save_location):
    invalid_save_location


corrupted_files = [
    'tests/resources/test_files/Health - Canada.ca_corrupted.html'
]

def test_html_corrupted_file_processing():
    from errors import FileProcessingFailedError
    with pytest.raises(FileProcessingFailedError) as exc_info:
        File("tests/resources/test_files/Health - Canada.ca_corrupted.html")