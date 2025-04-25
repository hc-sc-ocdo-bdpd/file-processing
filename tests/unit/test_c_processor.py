import os    
import pytest    
from unittest.mock import patch    
from file_processing import File    
from file_processing.errors import FileProcessingFailedError    
from file_processing_test_data import get_test_files_path    
  
test_files_path = get_test_files_path()    
  
variable_names = (  
    "path, encoding, num_lines, num_blank_lines, num_comment_lines, "  
    "num_code_lines, num_includes, num_defines, num_functions, num_todos"  
)  
  
values = [  
    (test_files_path / "avcodec.c",      "ascii", 820, 104, 48, 668, 24, 2, 54, 0),  
    (test_files_path / "mmio.c",         "ascii", 517, 97, 60, 360, 5, 1, 16, 0),  
    (test_files_path / "ptxgen.c",       "ascii", 267, 31, 43, 193, 6, 6, 22, 0),  
    (test_files_path / "vf_pixelize.c",  "ascii", 351, 41, 19, 291, 7, 5, 14, 0),  
]  
  
@pytest.mark.parametrize(variable_names, values)  
def test_c_file_metadata(path, encoding, num_lines, num_blank_lines, num_comment_lines,  
                         num_code_lines, num_includes, num_defines, num_functions, num_todos):  
    file_obj = File(path)  
    metadata = file_obj.metadata  
    assert metadata['encoding'] == encoding  
    assert metadata['num_lines'] == num_lines  
    assert metadata['num_blank_lines'] == num_blank_lines  
    assert metadata['num_comment_lines'] == num_comment_lines  
    assert metadata['num_code_lines'] == num_code_lines  
    assert metadata['num_includes'] == num_includes  
    assert metadata['num_defines'] == num_defines  
    assert metadata['num_functions'] == num_functions  
    assert metadata['num_todos'] == num_todos  
  
@pytest.mark.parametrize(variable_names, values)  
def test_save_c_file_metadata(copy_file, encoding, num_lines, num_blank_lines, num_comment_lines,  
                              num_code_lines, num_includes, num_defines, num_functions, num_todos):  
    file_obj = File(copy_file)  
    file_obj.processor.save()  
  
    saved_file_obj = File(copy_file)  
    metadata = saved_file_obj.metadata  
  
    assert metadata['encoding'] == encoding  
    assert metadata['num_lines'] == num_lines  
    assert metadata['num_blank_lines'] == num_blank_lines  
    assert metadata['num_comment_lines'] == num_comment_lines  
    assert metadata['num_code_lines'] == num_code_lines  
    assert metadata['num_includes'] == num_includes  
    assert metadata['num_defines'] == num_defines  
    assert metadata['num_functions'] == num_functions  
    assert metadata['num_todos'] == num_todos  
  
@pytest.mark.parametrize("valid_path", [path for path, *_ in values])  
def test_c_invalid_save_location(valid_path):  
    c_file = File(valid_path)  
    invalid_save_path = '/non_existent_folder/' + os.path.basename(valid_path)  
    with pytest.raises(FileProcessingFailedError):  
        c_file.processor.save(invalid_save_path)  
  
@pytest.mark.parametrize(variable_names, values)  
def test_not_opening_c_file(path, encoding, num_lines, num_blank_lines, num_comment_lines,  
                            num_code_lines, num_includes, num_defines, num_functions, num_todos):  
    with patch('builtins.open', autospec=True) as mock_open:  
        File(path, open_file=False)  
        mock_open.assert_not_called()  