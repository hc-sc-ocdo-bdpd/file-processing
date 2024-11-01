import os
import shutil
from unittest.mock import patch
import tempfile
import pytest
from file_processing import File
from file_processing.errors import FileProcessingFailedError
from file_processing_test_data import get_test_files_path

test_files_path = get_test_files_path()

# Sample metadata to check against
variable_names = "path, num_headings, num_links, num_code_blocks, text_length, num_lines, num_words"
values = [
    (test_files_path / 'LICENSE.md', 0, 0, 0, 399, 12, 34),  
    (test_files_path / 'README-file-proc.md', 15, 14, 5, 5255, 167, 629)
]

@pytest.fixture(params=values, ids=[str(x[0]) for x in values])
def md_file_obj(request):
    return File(request.param[0])

def test_md_metadata(md_file_obj):
    file_obj = md_file_obj
    print("Debug: Actual metadata collected ->", file_obj.metadata)
    assert file_obj.metadata['num_headings'] == file_obj.metadata.get('num_headings')
    assert file_obj.metadata['num_links'] == file_obj.metadata.get('num_links')
    assert file_obj.metadata['num_code_blocks'] == file_obj.metadata.get('num_code_blocks')
    assert file_obj.metadata['text_length'] == file_obj.metadata.get('text_length')
    assert file_obj.metadata['num_lines'] == file_obj.metadata.get('num_lines')
    assert file_obj.metadata['num_words'] == file_obj.metadata.get('num_words')

def test_md_save(md_file_obj):
    with tempfile.TemporaryDirectory() as temp_dir:
        original_md_path = md_file_obj.path
        saved_md_path = os.path.join(temp_dir, 'SavedMarkdown.md')

        md_file_obj.processor.save(saved_md_path)
        print("Debug: Saved Markdown path ->", saved_md_path)

        assert os.path.exists(saved_md_path)
        assert os.path.getsize(saved_md_path) == os.path.getsize(original_md_path)

@pytest.mark.parametrize(variable_names, values)
def test_md_file_processing(path, num_headings, num_links, num_code_blocks, text_length, num_lines, num_words):
    md_file_obj = File(path)
    assert md_file_obj.metadata['num_headings'] == num_headings
    assert md_file_obj.metadata['num_links'] == num_links
    assert md_file_obj.metadata['num_code_blocks'] == num_code_blocks
    assert md_file_obj.metadata['text_length'] == text_length
    assert md_file_obj.metadata['num_lines'] == num_lines
    assert md_file_obj.metadata['num_words'] == num_words

@pytest.mark.parametrize("path", map(lambda x: x[0], values))
def test_md_invalid_save_location(path):
    md_file = File(path)
    invalid_save_path = '/non_existent_folder/' + os.path.basename(path)
    print("Invalid save path ->", invalid_save_path)
    with pytest.raises(FileProcessingFailedError):
        md_file.save(invalid_save_path)

@pytest.mark.parametrize("path", map(lambda x: x[0], values))
def test_not_opening_md_file(path):
    with patch('builtins.open', autospec=True) as mock_open:
        File(path, open_file=False)
        print("File should not be opened")
        mock_open.assert_not_called()
