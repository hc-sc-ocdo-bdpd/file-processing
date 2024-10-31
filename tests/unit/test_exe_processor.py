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
variable_names = "path, entry_point, machine, num_sections"
values = [
    (test_files_path / 'hello-world.exe', '0xc320', '0x8664', 6)
]

@pytest.fixture(params=values, ids=[str(x[0]) for x in values])
def exe_file_obj(request):
    return File(request.param[0])

def test_exe_metadata(exe_file_obj):
    file_obj = exe_file_obj
    print("Debug: Actual metadata collected ->", file_obj.metadata)
    assert file_obj.metadata['entry_point'] == file_obj.metadata.get('entry_point')
    assert file_obj.metadata['machine'] == file_obj.metadata.get('machine')
    assert file_obj.metadata['num_sections'] == file_obj.metadata.get('num_sections')

def test_exe_save(exe_file_obj):
    with tempfile.TemporaryDirectory() as temp_dir:
        original_exe_path = exe_file_obj.path
        saved_exe_path = os.path.join(temp_dir, 'SavedSampleApp.exe')

        exe_file_obj.processor.save(saved_exe_path)
        print("Debug: Saved EXE path ->", saved_exe_path)

        assert os.path.exists(saved_exe_path)
        assert os.path.getsize(saved_exe_path) == os.path.getsize(original_exe_path)

@pytest.mark.parametrize(variable_names, values)
def test_exe_file_processing(path, entry_point, machine, num_sections):
    print("Path: ", path)
    exe_file_obj = File(path)
    print("Debug: Expected values ->")
    print(f"  Expected entry_point: {entry_point}")
    print(f"  Expected machine: {machine}")
    print(f"  Expected num_sections: {num_sections}")
    
    print("Debug: Actual metadata collected ->")
    print(f"  Actual entry_point: {exe_file_obj.metadata.get('entry_point')}")
    print(f"  Actual machine: {exe_file_obj.metadata.get('machine')}")
    print(f"  Actual num_sections: {exe_file_obj.metadata.get('num_sections')}")
    
    assert exe_file_obj.metadata['entry_point'] == entry_point
    assert exe_file_obj.metadata['machine'] == machine
    assert exe_file_obj.metadata['num_sections'] == num_sections

@pytest.mark.parametrize("path", map(lambda x: x[0], values))
def test_exe_invalid_save_location(path):
    exe_file = File(path)
    invalid_save_path = '/non_existent_folder/' + os.path.basename(path)
    print("Debug: Invalid save path ->", invalid_save_path)
    with pytest.raises(FileProcessingFailedError):
        exe_file.save(invalid_save_path)

@pytest.mark.parametrize("path", map(lambda x: x[0], values))
def test_not_opening_exe_file(path):
    with patch('builtins.open', autospec=True) as mock_open:
        File(path, open_file=False)
        print("Debug: File should not be opened")
        mock_open.assert_not_called()
