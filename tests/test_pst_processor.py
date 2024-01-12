# from errors import FileProcessingFailedError
# from unittest.mock import patch
# from file_processing.file import File
# import pytest
# import sys
# import os
# sys.path.append(os.path.join(sys.path[0], 'file_processing'))

# variable_names = "path, num_folders, num_files, file_types, file_names, emails"
# values = [
#     ('tests/resources/test_files/sample.pst', 2, 3, {'msg': 3},
#      ['1704726029000.msg', '1704870589000.msg', '1704380174000.msg'],
#      ['PD 5 Online - Winter 2024 - Announcements: CAPM Introduction for PD5',
#       'Upgrade by January 17, 2024, to keep your Azure data and services',
#       'Winter Featured Reads are here!']),
# ]


# @pytest.fixture(params=values, ids=[x[0] for x in values])
# def file_obj(request):
#     return File(request.param[0])


# def test_pst_extraction(file_obj):
#     import shutil
#     file_obj.processor.extract()

#     extraction_dir = os.path.splitext(file_obj.path)[0]
#     assert os.path.isdir(extraction_dir)

#     extracted_files = os.listdir(extraction_dir)
#     expected_files = file_obj.metadata['file_names']
#     assert set(extracted_files) == set(expected_files)

#     shutil.rmtree(extraction_dir)


# @pytest.mark.parametrize(variable_names, values)
# def test_pst_save(path, num_folders, num_files, file_types, file_names, emails):
#     import time
#     file = File(path)
#     saved_pst_path = f'{os.path.splitext(path)[0]}Copy.pst'
#     file.save(saved_pst_path)
#     assert os.path.exists(saved_pst_path)
#     assert set(emails) == set(File(saved_pst_path).metadata['emails'])
#     time.sleep(8)  # wait for Outlook to finish processing in the background
#     os.remove(saved_pst_path)


# @pytest.mark.parametrize(variable_names, values)
# def test_pst_metadata(path, num_folders, num_files, file_types, file_names, emails):
#     file_obj = File(path)
#     assert file_obj.metadata['num_folders'] == num_folders
#     assert file_obj.metadata['num_files'] == num_files
#     assert file_obj.metadata['file_types'] == file_types
#     assert file_obj.metadata['file_names'] == file_names
#     assert file_obj.metadata['emails'] == emails


# @pytest.mark.parametrize(variable_names, values)
# def test_save_pst_metadata(copy_file, num_folders, num_files, file_types, file_names, emails):
#     test_pst_metadata(copy_file, num_folders, num_files, file_types, file_names, emails)


# @pytest.mark.parametrize("path", map(lambda x: x[0], values))
# def test_pst_invalid_save_location(path):
#     pst_file = File(path)
#     invalid_save_path = '/non_existent_folder/' + os.path.basename(path)
#     with pytest.raises(FileProcessingFailedError):
#         pst_file.save(invalid_save_path)


# @pytest.mark.parametrize("path", map(lambda x: x[0], values))
# def test_not_opening_file(path):
#     with patch('builtins.open', autospec=True) as mock_open:
#         File(path, open_file=False)
#         mock_open.assert_not_called()
