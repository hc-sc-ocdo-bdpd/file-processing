import pytest
import sys, os
sys.path.append(os.path.join(sys.path[0], 'file_processing'))
from file_processing.file import File
import eyed3
from errors import FileProcessingFailedError


variable_names = "path, text_length, language, duration_seconds, title, artist"
values = [
   ('tests/resources/test_files/How Canadas Universal HealthCare System Works.mp3', 9570, 'en', 576.04, None, None),
   ('tests/resources/test_files/Super Easy French.mp3', 2704, 'fr', 219.0, None, None)
]


@pytest.mark.parametrize(variable_names, values)
def test_mp3_metadata(path, text_length, language, duration_seconds, title, artist):
   file_obj = File(path)
   assert len(file_obj.metadata['text']) == text_length
   assert file_obj.metadata['language'] == language
   assert file_obj.metadata['duration_seconds'] == duration_seconds
   assert file_obj.metadata['title'] == title
   assert file_obj.metadata['artist'] == artist


@pytest.fixture()
def copy_file(path, tmp_path_factory):
   from pathlib import Path
   copy_path = str(tmp_path_factory.mktemp("copy") / Path(path).name)
   file_obj = File(path)
   file_obj.save(copy_path)
   yield copy_path


@pytest.mark.parametrize("path, text_length, language, duration_seconds", map(lambda x: x[:4], values))
def test_save_mp3_metadata(copy_file, text_length, language, duration_seconds):
        
   # Load and change metadata via File object
   mp3_file = File(copy_file)
   mp3_file.metadata['title'] = 'Title New'
   mp3_file.metadata['artist'] = 'New Artist'

   # Save the updated file
   mp3_file.save()
   test_mp3_metadata(copy_file, text_length, language, duration_seconds, 'Title New', 'New Artist')


@pytest.mark.parametrize("path, text_length, language, duration_seconds", map(lambda x: x[:4], values))
def test_change_mp3_title_artist(copy_file, text_length, language, duration_seconds):
        
   # Change metadata via Document object
   mp3_file = eyed3.load(copy_file)
   mp3_file.tag.title = "Title New"
   mp3_file.tag.artist = "New Artist"
   
   # Save the file
   mp3_file.tag.save()
   test_mp3_metadata(copy_file, text_length, language, duration_seconds, 'Title New', 'New Artist')


invalid_save_locations = [
   ('tests/resources/test_files/How Canadas Universal HealthCare System Works.mp3', '/non_existent_folder/How Canadas Universal HealthCare System Works.mp3')
]


@pytest.mark.parametrize("path, save_path", invalid_save_locations)
def test_mp3_invalid_save_location(path, save_path):
   file_obj = File(path)
   with pytest.raises(FileProcessingFailedError):
      file_obj.save(save_path)


corrupted_files = [
   'tests/resources/test_files/Super Easy French Corrupted.mp3'
]

@pytest.mark.parametrize("path", corrupted_files)
def test_mp3_corrupted_file_processing(path):
   with pytest.raises(FileProcessingFailedError):
      File(path)
