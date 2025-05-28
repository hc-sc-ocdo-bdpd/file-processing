import os  
import pytest  
from unittest.mock import patch  
from file_processing import File  
from file_processing.errors import FileProcessingFailedError  
from file_processing_test_data import get_test_files_path  
  
test_files_path = get_test_files_path()  
  
variable_names = (  
    "path, encoding, num_lines, num_blank_lines, num_comment_lines, num_code_lines, "  
    "num_imports, num_exports, num_classes, num_interfaces, num_functions, num_todos"  
)  
  
values = [  
    (test_files_path / "scanner.ts",  "ascii", 1510, 822, 24, 664, 22, 1, 1, 2, 0, 0),  
    (test_files_path / "messages.ts", "ascii", 404, 234, 23, 147, 4, 14, 0, 0, 0, 0),  
    (test_files_path / "Logger.ts",   "ascii", 206, 114, 37, 55, 1, 6, 0, 1, 0, 0),  
    (test_files_path / "Driver.ts",   "ascii", 570, 331, 149, 90, 18, 2, 0, 1, 0, 0),  
]  
  
@pytest.mark.parametrize(variable_names, values)  
def test_ts_file_metadata(path, encoding, num_lines, num_blank_lines, num_comment_lines, num_code_lines,  
                          num_imports, num_exports, num_classes, num_interfaces, num_functions, num_todos):  
    file_obj = File(path)  
    metadata = file_obj.metadata  
    assert metadata['encoding'] == encoding  
    assert metadata['num_lines'] == num_lines  
    assert metadata['num_blank_lines'] == num_blank_lines  
    assert metadata['num_comment_lines'] == num_comment_lines  
    assert metadata['num_code_lines'] == num_code_lines  
    assert metadata['num_imports'] == num_imports  
    assert metadata['num_exports'] == num_exports  
    assert metadata['num_classes'] == num_classes  
    assert metadata['num_interfaces'] == num_interfaces  
    assert metadata['num_functions'] == num_functions  
    assert metadata['num_todos'] == num_todos  
  
@pytest.mark.parametrize(variable_names, values)  
def test_save_ts_file_metadata(copy_file, encoding, num_lines, num_blank_lines, num_comment_lines, num_code_lines,  
                               num_imports, num_exports, num_classes, num_interfaces, num_functions, num_todos):  
    file_obj = File(copy_file)  
    file_obj.processor.save()  
  
    saved_file_obj = File(copy_file)  
    metadata = saved_file_obj.metadata  
  
    assert metadata['encoding'] == encoding  
    assert metadata['num_lines'] == num_lines  
    assert metadata['num_blank_lines'] == num_blank_lines  
    assert metadata['num_comment_lines'] == num_comment_lines  
    assert metadata['num_code_lines'] == num_code_lines  
    assert metadata['num_imports'] == num_imports  
    assert metadata['num_exports'] == num_exports  
    assert metadata['num_classes'] == num_classes  
    assert metadata['num_interfaces'] == num_interfaces  
    assert metadata['num_functions'] == num_functions  
    assert metadata['num_todos'] == num_todos  
  
@pytest.mark.parametrize("valid_path", [path for path, *_ in values])  
def test_ts_invalid_save_location(valid_path):  
    ts_file = File(valid_path)  
    invalid_save_path = '/non_existent_folder/' + os.path.basename(valid_path)  
    with pytest.raises(FileProcessingFailedError):  
        ts_file.processor.save(invalid_save_path)  
  
@pytest.mark.parametrize(variable_names, values)  
def test_not_opening_ts_file(path, encoding, num_lines, num_blank_lines, num_comment_lines, num_code_lines,  
                             num_imports, num_exports, num_classes, num_interfaces, num_functions, num_todos):  
    with patch('builtins.open', autospec=True) as mock_open:  
        File(path, open_file=False)  
        mock_open.assert_not_called()  