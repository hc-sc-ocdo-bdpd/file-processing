import sys, os
sys.path.append(os.path.join(sys.path[0],'file_processing'))
import pytest
from file_processing.file import File

# copy_file fixture to be used in test_..._processor.py files
@pytest.fixture()
def copy_file(path, tmp_path_factory):
    from pathlib import Path
    copy_path = str(tmp_path_factory.mktemp("copy") / Path(path).name)
    file_obj = File(path)
    file_obj.save(copy_path)
    yield copy_path
