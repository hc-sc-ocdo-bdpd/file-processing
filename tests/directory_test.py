import sys, os
import pandas as pd
import glob
import pytest
sys.path.append(os.path.join(sys.path[0],'file_processing'))

@pytest.fixture
def mk_get_rm_dir():
    from file_processing.directory import Directory
    if not os.path.exists('tests/outputs'): 
        os.mkdir('tests/outputs')
    old_outputs = glob.glob('tests/outputs/*')
    for f in old_outputs:
        os.remove(f)
    dir1 = Directory('tests/resources/test_files')
    dir1.generate_report(report_file="tests/outputs/test_output.csv")
    data = pd.read_csv("tests/outputs/test_output.csv")
    yield data
    old_outputs = glob.glob('tests/outputs/*')
    for f in old_outputs:
        os.remove(f)
    os.rmdir('tests/outputs')
    

def test_directory_report(mk_get_rm_dir):
    assert mk_get_rm_dir.size > 1



    