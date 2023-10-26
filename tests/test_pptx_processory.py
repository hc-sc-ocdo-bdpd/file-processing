import pytest
import sys, os
sys.path.append(os.path.join(sys.path[0],'file_processing'))
from file_processing.file import File
from tests.file_test import copy_file
from errors import FileProcessingFailedError, FileCorruptionError
from pptx import Presentation


variable_names = "path, text_length, num_slides, last_modified_by, author"
values = [
   ('tests/resources/test_files/HealthCanadaOverviewFromWikipedia.pptx', 1655, 4, 'Test last_modified_by One', 'Test Author One'),
   ('tests/resources/test_files/SampleReport.pptx', 2037, 5, 'last_modified_by Test Author', 'Second Test Author')
]


@pytest.mark.parametrize(variable_names, values)
def test_pptx_metadata(path, text_length, num_slides, last_modified_by, author):
    file_obj = File(path)
    assert len(file_obj.metadata['text']) == text_length
    assert file_obj.metadata['num_slides'] == num_slides
    assert file_obj.metadata['last_modified_by'] == last_modified_by
    assert file_obj.metadata['author'] == author


@pytest.mark.usefixtures('copy_file')
@pytest.mark.parametrize('path', [x[0] for x in values])
def test_save_pptx_metadata(copy_file):
        
        # Load and change metadata via File object
        ppt_file = File(copy_file)
        ppt_file.metadata['author'] = 'New Author'
        ppt_file.metadata['last_modified_by'] = 'Modified New'

        #Save the updated file and load as Presentation
        ppt_file.save()
        ppt = Presentation(copy_file)

        # Check if modified metadata was correctly saved
        assert ppt.core_properties.author == "New Author"
        assert ppt.core_properties.last_modified_by == "Modified New"

@pytest.mark.usefixtures('copy_file')
@pytest.mark.parametrize('path', [x[0] for x in values])
def test_pptx_author_last_modified_by(copy_file):
        
        # Change metadata via Presentation object
        ppt_file = Presentation(copy_file)
        ppt_file.core_properties.author = "New Author"
        ppt_file.core_properties.last_modified_by = "Modified New"
        ppt_file.save(copy_file)

        # Load via File object and check if metadata was correctly changed
        ppt = File(copy_file)
        assert ppt.metadata['author'] == "New Author"
        assert ppt.metadata['last_modified_by'] == "Modified New"


invalid_save_locations = [
    ('tests/resources/test_files/HealthCanadaOverviewFromWikipedia_Locked.pptx', '/non_existent_folder/HealthCanadaOverviewFromWikipedia_Locked.pptx')
]

@pytest.mark.parametrize("path, save_path", invalid_save_locations)
def test_pptx_invalid_save_location(path, save_path):
    file_obj = File(path)
    with pytest.raises(FileProcessingFailedError):
        file_obj.processor.save(save_path)

corrupted_files = [
    'tests/resources/test_files/HealthCanadaOverviewFromWikipedia_corrupted.pptx'
]

@pytest.mark.parametrize("path", corrupted_files)
def test_pptx_corrupted_file_processing(path):
    with pytest.raises(FileCorruptionError):
        File(path)


locked_files = [
     ('tests/resources/test_files/SampleReport_Locked.pptx'), ('tests/resources/test_files/HealthCanadaOverviewFromWikipedia_Locked.pptx')
]

@pytest.mark.parametrize("path", locked_files)
def test_pptx_locked(path):
    assert File(path).metadata["has_password"] == True