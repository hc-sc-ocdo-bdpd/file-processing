import pytest
from file_processing.errors import FileProcessingFailedError
from file_processing import File
from file_processing_test_data import get_test_files_path

test_files_path = get_test_files_path()

# Test basic metadata for the top-level directory using real files
def test_directory_metadata(temp_directory_with_files):
    # Specify real files to be used from file-processing-test-data
    files_to_copy = [
        test_files_path / "2021_Census_English.csv",
        test_files_path / "SampleReport.pdf",
        test_files_path / "Health_Canada_logo.png",
        test_files_path / "sample.json"
    ]

    # Create the temp directory with the specified files
    temp_dir = temp_directory_with_files(files_to_copy)

    # Initialize the directory as a "File" object
    dir_processor = File(str(temp_dir))

    # Ensure metadata for the top-level directory
    assert dir_processor.metadata['num_items_in_top_level'] == 5  # 4 files + 1 subdirectory
    assert dir_processor.metadata['total_size_of_files_in_top_level'] > 0  # Ensure size is calculated correctly
    assert 'permissions' in dir_processor.metadata  # Permissions should be captured

# Test listing files in the top-level directory and processing each with the File class
def test_list_files_in_top_level(temp_directory_with_files):
    files_to_copy = [
        test_files_path / "2021_Census_English.csv",
        test_files_path / "SampleReport.pdf",
        test_files_path / "Health_Canada_logo.png",
        test_files_path / "sample.json"
    ]

    temp_dir = temp_directory_with_files(files_to_copy)

    # Initialize the directory as a "File" object
    dir_processor = File(str(temp_dir))
    files_in_top_level = dir_processor.processor.list_files_in_top_level()  # Access via the processor

    # Ensure the correct files are listed (ignoring subdirectories)
    assert len(files_in_top_level) == 4
    file_names = [f.name for f in files_in_top_level]
    assert sorted(file_names) == ["2021_Census_English.csv", "Health_Canada_logo.png", "SampleReport.pdf", "sample.json"]

    # Process each file using the File class and verify basic metadata
    for file_path in files_in_top_level:
        file_obj = File(str(file_path))
        assert file_obj.file_name == file_path.name
        assert file_obj.size > 0  # Ensure size is not zero

# Test listing subdirectories in the top-level directory
def test_list_subdirectories_in_top_level(temp_directory_with_files):
    files_to_copy = [
        test_files_path / "2021_Census_English.csv",
        test_files_path / "SampleReport.pdf"
    ]

    temp_dir = temp_directory_with_files(files_to_copy)

    # Initialize the directory as a "File" object
    dir_processor = File(str(temp_dir))
    subdirectories_in_top_level = dir_processor.processor.list_top_level_subdirectories()  # Access via the processor

    # Ensure the subdirectory is listed
    assert len(subdirectories_in_top_level) == 1
    assert subdirectories_in_top_level[0].name == "subdir"

# Test invalid directory path
@pytest.mark.parametrize("invalid_path", ["/invalid_directory", "nonexistent_folder"])
def test_invalid_directory_path(invalid_path):
    with pytest.raises(FileProcessingFailedError):
        File(invalid_path)

# Test saving directory metadata (though saving may not apply directly to directories)
def test_save_directory_metadata(temp_directory_with_files):
    files_to_copy = [
        test_files_path / "2021_Census_English.csv",
        test_files_path / "SampleReport.pdf"
    ]

    temp_dir = temp_directory_with_files(files_to_copy)

    # Initialize the directory as a "File" object
    dir_processor = File(str(temp_dir))
    with pytest.raises(FileProcessingFailedError):
        # Trying to save to an invalid location
        dir_processor.processor.save("/non_existent_folder/save_file.txt")
