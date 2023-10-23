import sys, os
import pandas as pd
import pytest
import json
sys.path.append(os.path.join(sys.path[0],'file_processing'))
from file_processing.directory import Directory


variable_names = "include_text, filters, keywords"
values = [(True, None, None), 
          (False, None, None),
          (True, {}, None), 
          (True, {"extensions": '.csv', "min_size": 50000}, None), 
          (False, {"extensions": ['.docx', '.pptx'], "max_size": 50000}, None),
          (True, None, []), 
          (False, None, ['Canada']), 
          (True, None, ['Canada', 'Health'])]


@pytest.fixture
def mk_get_rm_dir(include_text, filters, keywords, tmp_path_factory):
    output_path = str(tmp_path_factory.mktemp("outputs") / "test_output.csv")
    dir1 = Directory('tests/resources/directory_test_files')
    dir1.generate_report(output_path, include_text, filters, keywords)
    data = pd.read_csv(output_path)
    yield data


@pytest.mark.parametrize(variable_names, values)
def test_directory_report(mk_get_rm_dir, include_text, filters, keywords):
    assert mk_get_rm_dir.size > 1


@pytest.mark.parametrize(variable_names, values)
def test_text(mk_get_rm_dir, include_text, filters, keywords):
    assert mk_get_rm_dir['Metadata'].str.contains("\"text\":").any() == include_text


@pytest.mark.parametrize(variable_names, values)
def test_filters(mk_get_rm_dir, include_text, filters, keywords):
    if filters:
        if "extensions" in filters.keys():
            assert mk_get_rm_dir["Extension"].str.contains(r'\b(?:{})\b'.format("|".join(filters.get("extensions")))).count() == mk_get_rm_dir.shape[0]
        if "min_size" in filters.keys():
            assert (mk_get_rm_dir["Size"] >= filters.get("min_size")).all()
        if "max_size" in filters.keys():
            assert (mk_get_rm_dir["Size"] <= filters.get("max_size")).all()
    else:
        assert mk_get_rm_dir.size > 1


@pytest.mark.parametrize(variable_names, values)
def test_keywords(mk_get_rm_dir, keywords):
    if keywords:
        assert (mk_get_rm_dir["Metadata"].apply(lambda x: json.loads(x).get('text')).fillna('').str.lower().apply(lambda x: sum(x.count(key.lower()) for key in keywords)) 
                == mk_get_rm_dir["Keywords"].apply(lambda x : sum(json.loads(x).values()))).all()
    else:
        assert "Keywords" not in mk_get_rm_dir.columns

# add invalid output test
# add corrupted folder test