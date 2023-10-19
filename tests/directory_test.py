import sys, os
import pandas as pd
import glob
import pytest
sys.path.append(os.path.join(sys.path[0],'file_processing'))
from file_processing.directory import Directory
from typing import Optional

variable_names = "include_text, filters, keywords"
values = [(True, None, None), (False, None, None), (False, {"extensions": '.csv'}, None), (False, {"extensions": ['.csv', '.pptx']}, None),
          (False, {"min_size": 50000}, None), (False, {"max_size": 50000}, None)]

@pytest.fixture
def mk_get_rm_dir(include_text, filters, keywords, tmp_path_factory):
    # if not os.path.exists('tests/outputs'): 
    #     os.mkdir('tests/outputs')
    # old_outputs = glob.glob('tests/outputs/*')
    # for f in old_outputs:
    #     os.remove(f)
    output_path = str(tmp_path_factory.mktemp("outputs") / "test_output.csv")
    dir1 = Directory('tests/resources/test_files')
    dir1.generate_report(output_path, include_text, filters, keywords)
    data = pd.read_csv(output_path)
    # dir1.generate_report("tests/outputs/test_output.csv", include_text, filters, keywords)
    # data = pd.read_csv("tests/outputs/test_output.csv")
    yield data #dir1
    # old_outputs = glob.glob('tests/outputs/*')
    # for f in old_outputs:
    #     os.remove(f)
    # os.rmdir('tests/outputs')

@pytest.mark.parametrize(variable_names, values)
def test_directory_report(mk_get_rm_dir, include_text, filters, keywords):
    assert mk_get_rm_dir.size > 1


# file generator method
    # filter
    # no filter

# apply_filters method
    # extension filter: nonexistent, file is in, file is not in
    # min_size filter: nonexistent, file is smaller (fail), file is larger (pass)
    # max_size filter: nonexistent, file is smaller (pass), file is larger (fail)

# get_files method
    # return generator object

# generate_report method
    # include_text
@pytest.mark.parametrize(variable_names, values)
def test_text(mk_get_rm_dir, include_text, filters, keywords):
    assert mk_get_rm_dir['Metadata'].str.contains("\"text\":").any() == include_text

    # filters
@pytest.mark.parametrize(variable_names, values)
def test_filters(mk_get_rm_dir, include_text, filters, keywords):
    if filters is not None:
        if "extensions" in filters.keys():
            assert mk_get_rm_dir["Extension"].str.contains(r'\b(?:{})\b'.format("|".join(filters.get("extensions")))).count() == mk_get_rm_dir.shape[0]
        if "min_size" in filters.keys():
            assert mk_get_rm_dir["Size"].all() >= filters.get("min_size")
        if "max_size" in filters.keys():
            assert mk_get_rm_dir["Size"].all() <= filters.get("max_size")
    # add some else statement
    # else:
    #     assert mk_get_rm_dir["Extension"].str.conta == mk_get_rm_dir.shape[0]
    
    # filters ALL THREE
    # keywords EMPTY LIST
    # keywords ONE
    # keywords MULTIPLE

# _count_keywords method
    # good text, one keyword -> match
    # good text, multiple keywords -> match
    # good text, one keyword -> no match
    # no text, one keyword

    