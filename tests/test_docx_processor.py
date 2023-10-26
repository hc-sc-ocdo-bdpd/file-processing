import pytest
import sys, os
sys.path.append(os.path.join(sys.path[0],'file_processing'))
from file_processing.file import File
from errors import FileProcessingFailedError, FileCorruptionError
from docx import Document


variable_names = "path, text_length, last_modified_by, author"
values = [
   ('tests/resources/test_files/HealthCanadaOverviewFromWikipedia.docx', 1631, 'Test last_modified_by One', 'Test Author One'),
   ('tests/resources/test_files/SampleReport.docx', 3220, 'last_modified_by Test Author', 'Second Test Author')
]


@pytest.mark.parametrize(variable_names, values)
def test_docx_metadata(path, text_length, last_modified_by, author):
    file_obj = File(path)
    assert len(file_obj.metadata['text']) == text_length
    assert file_obj.metadata['last_modified_by'] == last_modified_by
    assert file_obj.metadata['author'] == author


@pytest.mark.usefixtures('copy_file')
@pytest.mark.parametrize('path', [x[0] for x in values])
def test_save_docx_metadata(copy_file):
        
        # Load and change metadata via File object
        docx_file = File(copy_file)
        docx_file.metadata['author'] = 'New Author'
        docx_file.metadata['last_modified_by'] = 'Modified New'

        # Save the updated file and load as Document
        docx_file.save()
        docx = Document(copy_file)

        # Check if modified metadata was correctly saved
        assert docx.core_properties.author == "New Author"
        assert docx.core_properties.last_modified_by == "Modified New"

@pytest.mark.usefixtures('copy_file')
@pytest.mark.parametrize('path', [x[0] for x in values])
def test_change_docx_author_last_modified_by(copy_file):
        
        # Change metadata via Document object
        docx_file = Document(copy_file)
        docx_file.core_properties.author = "New Author"
        docx_file.core_properties.last_modified_by = "Modified New"
        
        # Save the file and load as File object
        docx_file.save(copy_file)
        docx = File(copy_file)

        # Assert metadata was correctly changed
        assert docx.metadata['author'] == "New Author"
        assert docx.metadata['last_modified_by'] == "Modified New"



invalid_save_locations = [
    ('tests/resources/test_files/HealthCanadaOverviewFromWikipedia.docx', '/non_existent_folder/HealthCanadaOverviewFromWikipedia.docx')
]

@pytest.mark.parametrize("path, save_path", invalid_save_locations)
def test_docx_invalid_save_location(path, save_path):
    file_obj = File(path)
    with pytest.raises(FileProcessingFailedError):
        file_obj.processor.save(save_path)


corrupted_files = [
    'tests/resources/test_files/HealthCanadaOverviewFromWikipedia_corrupted.pptx'
]

@pytest.mark.parametrize("path", corrupted_files)
def test_docx_corrupted_file_processing(path):
    with pytest.raises(FileCorruptionError):
        File(path)

locked_files = [
     ('tests/resources/test_files/SampleReport_Locked.docx'), ('tests/resources/test_files/HealthCanadaOverviewFromWikipedia_Locked.docx')
]

@pytest.mark.parametrize("path", locked_files)
def test_docx_locked(path):
    assert File(path).metadata["has_password"] == True
