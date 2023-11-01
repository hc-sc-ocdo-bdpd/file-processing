import pytest
import sys, os
sys.path.append(os.path.join(sys.path[0],'file_processing'))
from file_processing.file import File

variable_names = "path, text_length, num_lines, num_words"
values = [
   ('tests/resources/test_files/Sample.xml', 4429, 120, 336)
]

@pytest.mark.parametrize(variable_names, values)
def test_xml_metadata(path, text_length, num_lines, num_words):
    file_obj = File(path)
    assert len(file_obj.metadata['text']) == text_length
    assert file_obj.metadata['num_lines'] == num_lines
    assert file_obj.metadata['num_words'] == num_words

@pytest.mark.parametrize(variable_names, values)
def test_save_xml_metadata(copy_file, text_length, num_lines, num_words):
        test_xml_metadata(copy_file, text_length, num_lines, num_words)


@pytest.mark.parametrize("path", map(lambda x: x[0], values))
def test_xml_invalid_save_location(invalid_save_location):
    invalid_save_location

corrupted_files = [
    'tests/resources/test_files/Sample_corrupted.xml'
]

@pytest.mark.parametrize("path", corrupted_files)
def test_xml_corrupted_file_processing(corrupted_file_processing):
    corrupted_file_processing

