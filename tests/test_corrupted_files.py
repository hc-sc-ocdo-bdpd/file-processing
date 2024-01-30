import pytest
from file_processing import File
from file_processing.tools.errors import FileProcessingFailedError, FileCorruptionError

corrupted_files_processing = [
    'tests/resources/test_files/2021_Census_English_corrupted.csv',
    'tests/resources/test_files/Health - Canada.ca_corrupted.html',
    'tests/resources/test_files/MapCanada_corrupted.jpg',
    'tests/resources/test_files/Test Email_corrupted.msg',
    'tests/resources/test_files/SampleReportScreenShot_corrupted.pdf',
    'tests/resources/test_files/MapCanada_corrupted.png',
    'tests/resources/test_files/callbacks_corrupted.py',
    'tests/resources/test_files/Test_for_RTF_corrupted.rtf',
    'tests/resources/test_files/government_of_canada_wikipedia_corrupted.txt',
    'tests/resources/test_files/Sample_corrupted.xml',
    'tests/resources/test_files/SampleReport_corrupted.zip',
    'tests/resources/test_files/MSEdgeIcon_corrupted.gif',
    'tests/resources/test_files/MSWordIcon_corrupted.tiff',
    'tests/resources/test_files/MapleLeaf_corrupted.heif',
    'tests/resources/test_files/MapleLeaf_corrupted.heic',
    'tests/resources/test_files/CanadaLogo_corrupted.tif'

]


@pytest.mark.parametrize("path", corrupted_files_processing)
def test_corrupted_file_processing_error(path):
    with pytest.raises(FileProcessingFailedError):
        File(path)


corrupted_files_corruption = [
    'tests/resources/test_files/HealthCanadaOverviewFromWikipedia_corrupted.docx',
    'tests/resources/test_files/coffee_corrupted.json',
    'tests/resources/test_files/HealthCanadaOverviewFromWikipedia_corrupted.pptx',
    'tests/resources/test_files/Test_excel_file_corrupted.xlsx',
]


@pytest.mark.parametrize("path", corrupted_files_corruption)
def test_corrupted_file_corruption_error(path):
    with pytest.raises(FileCorruptionError):
        File(path)
