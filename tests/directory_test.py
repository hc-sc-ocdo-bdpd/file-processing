import sys, os
import pandas as pd
import glob
sys.path.append(os.path.join(sys.path[0],'file_processing'))

def test_directory_report():
    from file_processing.directory import Directory
    dir1 = Directory('tests/resources/test_files')
    old_outputs = glob.glob('tests/outputs/*')
    for f in old_outputs:
        os.remove(f)
    dir1.generate_report(report_file="tests/outputs/test_output.csv")
    data = pd.read_csv("tests/outputs/test_output.csv")
    assert data.size > 1
    old_outputs = glob.glob('tests/outputs/*')
    for f in old_outputs:
        os.remove(f)


    