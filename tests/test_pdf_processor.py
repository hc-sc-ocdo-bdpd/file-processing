import os
from unittest.mock import patch
import pytest
from file_processing import File
from file_processing.tools.errors import FileProcessingFailedError

variable_names = "path, ocr_text_length"
values = [
    ('tests/resources/test_files/SampleReportScreenShot.pdf', 3225),
    ('tests/resources/test_files/HealthCanadaOverviewFromWikipedia.pdf', 1673)
]


locked_files = [
    ('tests/resources/test_files/SampleReport_Locked.pdf'),
    ('tests/resources/test_files/ArtificialNeuralNetworksForBeginners_Locked.pdf')
]


@pytest.mark.parametrize("path", locked_files)
def test_pdf_locked(path):
    assert File(path).metadata["has_password"] is True


@pytest.mark.parametrize("path", map(lambda x: x[0], values))
def test_pdf_invalid_save_location(path):
    pdf_file = File(path)
    invalid_save_path = '/non_existent_folder/' + os.path.basename(path)
    with pytest.raises(FileProcessingFailedError):
        pdf_file.processor.save(invalid_save_path)


@pytest.mark.parametrize("path", map(lambda x: x[0], values))
def test_not_opening_file(path):
    with patch('builtins.open', autospec=True) as mock_open:
        File(path, open_file=False)
        mock_open.assert_not_called()
