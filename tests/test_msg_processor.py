import pytest
import sys, os
sys.path.append(os.path.join(sys.path[0],'file_processing'))
from file_processing.file import File


variable_names = "path, text_length, subject, date, sender"
values = [
   ('tests/resources/test_files/Test Email.msg', 19, 'Test Email', 'Mon, 18 Sep 2023 13:57:16 -0400', '"Burnett, Taylen (HC/SC)" <Taylen.Burnett@hc-sc.gc.ca>'),
   ('tests/resources/test_files/Health Canada Overview from Wikipedia.msg', 13876, 'Health Canada Overview from Wikipedia', 'Tue, 31 Oct 2023 14:54:03 -0400', '"Prazuch, Karolina (HC/SC)" <karolina.prazuch@hc-sc.gc.ca>')
]


@pytest.mark.parametrize(variable_names, values)
def test_msg_metadata(path, text_length, subject, date, sender):
    file_obj = File(path)
    assert len(file_obj.metadata['text']) == text_length
    assert file_obj.metadata['subject'] == subject
    assert file_obj.metadata['date'] == date
    assert file_obj.metadata['sender'] == sender
    

@pytest.mark.parametrize(variable_names, values)
def test_save_msg_metadata(copy_file, text_length, subject, date, sender):
    test_msg_metadata(copy_file, text_length, subject, date, sender)


@pytest.mark.parametrize("path", map(lambda x: x[0], values))
def test_msg_invalid_save_location(invalid_save_location):
    invalid_save_location


corrupted_files = [
    'tests/resources/test_files/Test Email_corrupted.msg'
]

@pytest.mark.parametrize("path", corrupted_files)
def test_msg_corrupted_file_processing(corrupted_file_processing):
    corrupted_file_processing