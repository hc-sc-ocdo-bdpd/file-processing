import pytest
from file_processing import File
from file_processing.errors import FileProcessingFailedError, FileCorruptionError
from file_processing_test_data import get_test_files_path

test_files_path = get_test_files_path()

corrupted_files_processing = [
    test_files_path / '2021_Census_English_corrupted.csv',
    test_files_path / 'Health - Canada.ca_corrupted.html',
    test_files_path / 'MapCanada_corrupted.jpg',
    test_files_path / 'Test Email_corrupted.msg',
    test_files_path / 'SampleReportScreenShot_corrupted.pdf',
    test_files_path / 'MapCanada_corrupted.png',
    test_files_path / 'callbacks_corrupted.py',
    test_files_path / 'Test_for_RTF_corrupted.rtf',
    test_files_path / 'government_of_canada_wikipedia_corrupted.txt',
    test_files_path / 'Sample_corrupted.xml',
    test_files_path / 'SampleReport_corrupted.zip',
    test_files_path / 'MSEdgeIcon_corrupted.gif',
    test_files_path / 'MSWordIcon_corrupted.tiff',
    test_files_path / 'MapleLeaf_corrupted.heif',
    test_files_path / 'MapleLeaf_corrupted.heic',
    test_files_path / 'CanadaLogo_corrupted.tif'
]


@pytest.mark.parametrize("path", corrupted_files_processing)
def test_corrupted_file_processing_error(path):
    with pytest.raises(FileProcessingFailedError):
        File(path)


corrupted_files_corruption = [
    test_files_path / 'HealthCanadaOverviewFromWikipedia_corrupted.docx',
    test_files_path / 'coffee_corrupted.json',
    test_files_path / 'HealthCanadaOverviewFromWikipedia_corrupted.pptx',
    test_files_path / 'Test_excel_file_corrupted.xlsx',
]


@pytest.mark.parametrize("path", corrupted_files_corruption)
def test_corrupted_file_corruption_error(path):
    with pytest.raises(FileCorruptionError):
        File(path)
