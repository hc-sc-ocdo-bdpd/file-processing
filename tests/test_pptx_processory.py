import pytest
import sys, os
sys.path.append(os.path.join(sys.path[0],'file_processing'))
from file_processing.file import File
from tests.file_test import copy_file
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
@pytest.mark.parametrize(variable_names, values)
def test_save_pptx_metadata(copy_file, text_length, num_slides, last_modified_by, author):
        
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