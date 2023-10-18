import pytest
import sys, os
sys.path.append(os.path.join(sys.path[0],'file_processing'))
from file_processing.file import File

variable_names = "path, text_length, num_lines, num_words"
values = [
   ('tests/resources/test_files/government_of_canada_wikipedia.txt', 38983, 306, 5691),
   ('tests/resources/test_files/usa_government_wikipedia.txt', 47819, 383, 7160)
]

@pytest.mark.parametrize(variable_names, values)
def test_txt_metadata(path, text_length, num_lines, num_words):
    text = File(path)
    assert len(text.metadata['text']) == text_length
    assert text.metadata['num_lines'] == num_lines
    assert text.metadata['num_words'] == num_words


@pytest.fixture(scope="function")
def copy_file_paths(tmp_path_factory):
    from pathlib import Path
    file_path = 'tests/resources/test_files/government_of_canada_wikipedia.txt'
    copy_path = str(tmp_path_factory.mktemp("copy") / Path(file_path).name)
    yield file_path, copy_path


@pytest.fixture()
def copy_file_length(copy_file_paths):
    file_path, copy_path = copy_file_paths

    # Copying file
    with open(file_path, 'rb') as src_file:
        with open(copy_path, 'wb') as dest_file:
            dest_file.write(src_file.read())

    # Load via File object
    txt_file = File(copy_path)
        
    # Save
    txt_file.save()

    copy_path_length = len(txt_file.metadata['text'])

    yield copy_path_length 


def test_save_txt_metadata(copy_file_length):
    # Assert if .txt correctly saved
    assert copy_file_length == 38983
