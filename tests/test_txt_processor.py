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


def test_save_txt_metadata():
    test_txt_path = 'tests/resources/test_files/government_of_canada_wikipedia.txt'
    copy_test_txt_path = 'tests/resources/test_files/government_of_canada_wikipedia_copy.txt'
    
    # Copying file
    with open(test_txt_path, 'rb') as src_file:
        with open(copy_test_txt_path, 'wb') as dest_file:
            dest_file.write(src_file.read())

    try:
        
        # Load via File object
        txt_file = File(copy_test_txt_path)
        
        # Save
        txt_file.save()
        
        # Assert if .txt correctly saved
        assert len(txt_file.metadata['text']) == 38983

    finally:
        # Clean up by removing the copied file after the test is done
        os.remove(copy_test_txt_path)
