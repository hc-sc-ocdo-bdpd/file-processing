import os
import shutil
import pytest
from unittest.mock import patch
from pathlib import Path
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
    else:
        file_obj = File(str(path))
        save_path = tmp_path / os.path.basename(path)
        if expect_exception_on_save:
            with pytest.raises(FileProcessingFailedError):
                file_obj.save(str(save_path))
        else:
            file_obj.save(str(save_path))
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
    file_obj = File(str(valid_path), open_file=False)
    invalid_save_path = '/non_existent_folder/' + os.path.basename(str(valid_path))
    with pytest.raises(FileProcessingFailedError):
        file_obj.save(invalid_save_path)


@pytest.mark.parametrize("path", [path for path, *_ in values])
def test_not_opening_pdf(path):
    file_obj = File(str(path), open_file=False)
    metadata = file_obj.metadata
    assert metadata == {'message': 'File was not opened'}


@pytest.mark.parametrize("path", [path for path, *rest in values if not rest[-2]])  # Only non-corrupt
@pytest.mark.parametrize("algorithm", ["md5", "sha256"])
def test_pdf_copy_with_integrity(path, algorithm, tmp_path):
    file_obj = File(str(path), open_file=False)
    expected_hash = file_obj.processor.compute_hash(algorithm)

    dest_path = tmp_path / Path(path).name
    file_obj.copy(dest_path, verify_integrity=True)

    copied = File(dest_path)
    assert copied.processor.compute_hash(algorithm) == expected_hash


@pytest.mark.parametrize("path", [path for path, *rest in values if not rest[-2]])  # Only non-corrupt
def test_pdf_copy_integrity_failure(path, tmp_path, monkeypatch):
    file_obj = File(str(path), open_file=False)

    def corrupt(src, dst, *, follow_symlinks=True):
        with open(dst, 'w') as f:
            f.write("INVALID PDF FILE")

    monkeypatch.setattr(shutil, "copy2", corrupt)

    with pytest.raises(FileProcessingFailedError) as excinfo:
        file_obj.copy(tmp_path / Path(path).name, verify_integrity=True)
    assert "Integrity check failed" in str(excinfo.value)
