import pytest
import sys, os
sys.path.append(os.path.join(sys.path[0],'file_processing'))
from file_processing.file import File
from unittest.mock import patch


variable_names = "path, ocr_text_length"
values = [
   ('tests/resources/test_files/SampleReportScreenShot.pdf', 3225),
   ('tests/resources/test_files/HealthCanadaOverviewFromWikipedia.pdf', 1673)
]


@pytest.mark.parametrize(variable_names, values)
def test_pdf_metadata(path, ocr_text_length):
    file_obj = File(path, use_ocr = True)
    assert len(file_obj.metadata['ocr_text']) == ocr_text_length


locked_files = [
     ('tests/resources/test_files/SampleReport_Locked.pdf'), 
     ('tests/resources/test_files/ArtificialNeuralNetworksForBeginners_Locked.pdf')
]

@pytest.mark.parametrize("path", locked_files)
def test_pdf_locked(path):
    assert File(path).metadata["has_password"] == True


@pytest.mark.parametrize("path", map(lambda x: x[0], values))
def test_pdf_invalid_save_location(invalid_save_location):
    invalid_save_location


@pytest.mark.parametrize("path", map(lambda x: x[0], values))
def test_not_opening_file(path):
    with patch('builtins.open', autospec=True) as mock_open:
        File(path, open_file=False)
        mock_open.assert_not_called()


corrupted_files = [
    'tests/resources/test_files/SampleReportScreenShot_corrupted.pdf'
]

@pytest.mark.parametrize("path", corrupted_files)
def test_pdf_corrupted_file_processing(corrupted_file_processing):
    corrupted_file_processing