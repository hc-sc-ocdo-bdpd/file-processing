import os
from unittest.mock import patch
import pytest
from file_processing import File
from file_processing.errors import FileProcessingFailedError
from file_processing_test_data import get_test_files_path

test_files_path = get_test_files_path()

variable_names = "path, text_present, has_password, author, producer, expect_exception_on_process, expect_exception_on_save"

values = [
    # Unencrypted PDFs
    (test_files_path / 'ArtificialNeuralNetworksForBeginners.pdf', True, False, None, None, False, False),
    (test_files_path / 'HealthCanadaOverviewFromWikipedia.pdf', True, False, None, None, False, False),
    (test_files_path / 'SampleReport.pdf', True, False, None, None, False, False),
    (test_files_path / 'SampleReportScreenShot.pdf', True, False, None, None, False, False),
    # Encrypted PDFs
    (test_files_path / 'ArtificialNeuralNetworksForBeginners_Locked.pdf', False, True, None, None, False, True),
    (test_files_path / 'SampleReport_Locked.pdf', False, True, None, None, False, True),
    # Corrupted PDF
    (test_files_path / 'SampleReportScreenShot_corrupted.pdf', False, False, None, None, True, True),
]


@pytest.mark.parametrize(variable_names, values)
def test_pdf_metadata(
    path,
    text_present,
    has_password,
    author,
    producer,
    expect_exception_on_process,
    expect_exception_on_save,
):
    if expect_exception_on_process:
        with pytest.raises(FileProcessingFailedError):
            file_obj = File(str(path))
    else:
        file_obj = File(str(path))
        metadata = file_obj.metadata
        assert metadata['has_password'] == has_password
        if text_present:
            assert metadata['text'] is not None
            assert len(metadata['text']) > 0
        else:
            assert metadata['text'] is None
        if author is not None:
            assert metadata['author'] == author
        if producer is not None:
            assert metadata['producer'] == producer


@pytest.mark.parametrize(variable_names, values)
def test_save_pdf_metadata(
    path,
    text_present,
    has_password,
    author,
    producer,
    expect_exception_on_process,
    expect_exception_on_save,
    tmp_path,
):
    if expect_exception_on_process:
        with pytest.raises(FileProcessingFailedError):
            file_obj = File(str(path))
            # Cannot proceed to save
    else:
        file_obj = File(str(path))
        save_path = tmp_path / os.path.basename(path)
        if expect_exception_on_save:
            with pytest.raises(FileProcessingFailedError):
                file_obj.save(str(save_path))
        else:
            # Save to a new path
            file_obj.save(str(save_path))
            # Now read the saved file and check if it can be processed again
            file_obj_saved = File(str(save_path))
            metadata = file_obj_saved.metadata
            assert metadata['has_password'] == has_password
            if text_present:
                assert metadata['text'] is not None
                assert len(metadata['text']) > 0
            else:
                assert metadata['text'] is None
            if author is not None:
                assert metadata['author'] == author
            if producer is not None:
                assert metadata['producer'] == producer


@pytest.mark.parametrize("valid_path", [path for path, *_ in values])
def test_pdf_invalid_save_location(valid_path):
    file_obj = File(str(valid_path), open_file=False)  # Do not process the file
    invalid_save_path = '/non_existent_folder/' + os.path.basename(str(valid_path))
    with pytest.raises(FileProcessingFailedError):
        file_obj.save(invalid_save_path)


@pytest.mark.parametrize("path", [path for path, *_ in values])
def test_not_opening_pdf(path):
    file_obj = File(str(path), open_file=False)
    metadata = file_obj.metadata
    assert metadata == {'message': 'File was not opened'}
