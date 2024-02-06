import os
from pathlib import Path
import pandas as pd
import pytest
from file_processing import Directory

file_names = ['CPP_disability_benefits.txt', 'CPP_retirement_pension.txt', 'EI_regular_benefits.txt', 'aviation_safety.txt',
              'canadian_constitution.txt', 'climate_change_causes.txt', 'coronavirus_symptoms.txt', 'documents_for_express_entry.txt',
              'express_entry.txt', 'funding_culture_history_sport.txt', 'healthcare_system.txt', 'history_of_canada.txt',
              'how_courts_are_organized.txt', 'national_security_act.txt', 'net_zero_emissions_by_2050.txt', 'origin_of_name_canada.txt',
              'personal_income_tax.txt', 'start_a_business.txt', 'travel_advisories.txt', 'visitors_to_canada.txt']

variable_names = "filters, threshold, top_n, use_abs_path"
values = [
    ({}, 0, 0, True),
    ({'extensions': ['.txt']}, 0, 100, False),
    ({'min_size': 1000}, 0.5, 100, True),
    ({'max_size': 1e6}, 1, 0, False),
    (None, 0.3, 20, False),
    (None, 0.9, 3, False),
    (None, 0.1, 1, False)
]


@pytest.fixture
def mk_get_rm_dir(filters, threshold, top_n, use_abs_path, tmp_path_factory):
    output_path = str(tmp_path_factory.mktemp("outputs") / "test_output.csv")
    dir1 = Directory('tests/resources/similarity_test_files')
    dir1.identify_duplicates(output_path, filters, threshold, top_n, use_abs_path)
    data = pd.read_csv(output_path, index_col=0)
    yield data


def test_empty_report(tmp_path):
    dir1 = Directory('tests/resources/empty_dir')
    with pytest.raises(Exception):
        dir1.generate_report(tmp_path / "test_output.csv")


@pytest.mark.parametrize(variable_names, values)
def test_columns(mk_get_rm_dir, threshold, top_n, use_abs_path):
    # Cosine similarity (compares all files)
    if threshold == 0:
        if not use_abs_path:
            assert set(mk_get_rm_dir.columns).issubset(set(file_names)), 'File names are incorrect'
        elif use_abs_path:
            assert all([os.path.isabs(item) for item in mk_get_rm_dir.columns]), 'Paths are not absolute paths'
            extracted_names = [Path(item).name for item in mk_get_rm_dir.columns]
            assert set(extracted_names).issubset(set(file_names)), 'File names are incorrect'

    # FAISS indexes (returns top n matches)
    elif threshold != 0:
        headers = ['absolute_path' if use_abs_path else 'file_name']
        for n in range(min(top_n, len(file_names))):
            headers.append(f'{n+1}_file')
            headers.append(str(n+1))
        assert set(mk_get_rm_dir.columns) == set(headers), 'File names are incorrect'


@pytest.mark.parametrize(variable_names, values)
def test_values(mk_get_rm_dir, threshold, top_n):
    # Cosine similarity (compares all files)
    if threshold == 0:
        assert mk_get_rm_dir.map(lambda x: pd.to_numeric(x, errors='coerce')).notnull().all().all(), \
            'Non-numeric data found in output'
        assert mk_get_rm_dir.map(lambda x: pd.Series(x).between(-1, 1, inclusive='both').all()).all().all(), \
            'Numeric values outside of acceptable cosine similarity range of [-1, 1]'

    # FAISS indexes (returns top n matches)
    elif threshold != 0:
        similarities = mk_get_rm_dir[[str(n+1) for n in range(min(top_n, len(file_names)))]]
        assert similarities.map(lambda x: pd.Series(x).dropna().between(threshold, 1, inclusive='both').all()).all().all(), \
            f'Numeric values outside of acceptable similarity range of [{threshold}, 1]'
