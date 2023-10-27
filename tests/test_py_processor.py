import pytest
import sys, os
sys.path.append(os.path.join(sys.path[0], 'file_processing'))
from file import File
from errors import FileProcessingFailedError

variable_names = "path, num_lines, num_functions, num_classes, num_imports"
values = [
   ('tests/resources/test_files/sample1.py', 10, 2, 1, 3),
   ('tests/resources/test_files/sample2.py', 15, 3, 2, 2)
]

@pytest.mark.parametrize(variable_names, values)
def test_python_metadata(path, num_lines, num_functions, num_classes, num_imports):
    file_obj = File(path)
    assert file_obj.metadata['num_lines'] == num_lines
    assert file_obj.metadata['num_functions'] == num_functions
    assert file_obj.metadata['num_classes'] == num_classes
    assert len(file_obj.metadata['imports']) == num_imports

@pytest.fixture()
def copy_file(path, tmp_path_factory):
    from pathlib import Path
    copy_path = str(tmp_path_factory.mktemp("copy") / Path(path).name)
    file_obj = File(path)
    file_obj.save(copy_path)
    yield copy_path

@pytest.mark.parametrize(variable_names, values)
def test_save_python_metadata(copy_file, num_lines, num_functions, num_classes, num_imports):
    test_python_metadata(copy_file, num_lines, num_functions, num_classes, num_imports)

invalid_save_locations = [
    ('tests/resources/test_files/sample1.py', '/non_existent_folder/sample1.py')
]

@pytest.mark.parametrize("path, save_path", invalid_save_locations)
def test_python_invalid_save_location(path, save_path):
    file_obj = File(path)
    with pytest.raises(FileProcessingFailedError):
        file_obj.save(save_path)

corrupted_files = [
    'tests/resources/test_files/sample1_corrupted.py'
]

@pytest.mark.parametrize("path", corrupted_files)
def test_python_corrupted_file_processing(path):
    with pytest.raises(FileProcessingFailedError):
        File(path)
