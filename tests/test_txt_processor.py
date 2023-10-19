import pytest
import sys, os
sys.path.append(os.path.join(sys.path[0],'file_processing'))
from file_processing.file import File

variable_names = "path, text_length, num_lines, num_words"
values = [
   ('tests/resources/test_files/government_of_canada_wikipedia.txt', 38983, 306, 5691),
   ('tests/resources/test_files/usa_government_wikipedia.txt', 47819, 383, 7160)
]

@pytest.fixture()
def file_metadata(path):
    file_obj = File(path)
    yield (len(file_obj.metadata['text']),
           file_obj.metadata['num_lines'],
           file_obj.metadata['num_words'])


@pytest.mark.parametrize(variable_names, values)
def test_txt_metadata(file_metadata, text_length, num_lines, num_words):
    assert (text_length, num_lines, num_words) == file_metadata


@pytest.fixture()
def copy_file(path, tmp_path_factory):
    from pathlib import Path
    copy_path = str(tmp_path_factory.mktemp("copy") / Path(path).name)
    file_obj = File(path)
    file_obj.save(copy_path)
    yield copy_path


@pytest.mark.parametrize(variable_names, values)
def test_save_txt_metadata(copy_file, text_length, num_lines, num_words):
    file_obj = File(copy_file)
    assert (len(file_obj.metadata['text']), 
           file_obj.metadata['num_lines'],
           file_obj.metadata['num_words']) == (text_length, num_lines, num_words)
