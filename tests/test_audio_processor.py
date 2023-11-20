import pytest
import sys, os
sys.path.append(os.path.join(sys.path[0], 'file_processing'))
from file_processing.file import File
import audio_metadata
from errors import FileProcessingFailedError


variable_names = "path, bitrate, duration, artist, date, title"
values = [
   ('tests/resources/test_files/How Canadas Universal HealthCare System Works.mp3', 64000, 2076.306, None, None, None),
   ('tests/resources/test_files/Super Easy French.mp3', 64000, 681.48, None, None, None)
]


@pytest.mark.parametrize(variable_names, values)
def test_audio_metadata(path, bitrate, duration, artist, date, title):
   file_obj = File(path)
   assert file_obj.metadata['bitrate'] == bitrate
   assert file_obj.metadata['duration'] == duration
   assert file_obj.metadata['artist'] == artist
   assert file_obj.metadata['date'] == date
   assert file_obj.metadata['title'] == title

@pytest.fixture()
def copy_file(path, tmp_path_factory):
   from pathlib import Path
   copy_path = str(tmp_path_factory.mktemp("copy") / Path(path).name)
   file_obj = File(path)
   file_obj.save(copy_path)
   yield copy_path


@pytest.mark.parametrize("path, bitrate, duration", map(lambda x: x[:3], values))
def test_save_audio_metadata(copy_file, bitrate, duration):

   # Load and change metadata via File object
   audio_file = File(copy_file)
   audio_file.metadata['artist'] = 'New Artist'
   audio_file.metadata['date'] = 'New Date'
   audio_file.metadata['title'] = 'New Title'

   # Save the updated file
   audio_file.save()
   test_audio_metadata(copy_file, bitrate, duration, 'New Artist', 'New Date', 'New Title')


@pytest.mark.parametrize("path, bitrate, duration", map(lambda x: x[:3], values))
def test_change_audio_artist_title_date(copy_file, bitrate, duration):

   # Change metadata via Document object
   audio_file = audio_metadata.load(copy_file)
   audio_file.tags.artist = "New Artist"
   audio_file.tags.date = "New Date"
   audio_file.tags.title = "New Title"

   # Save the file
   audio_file.tags.save()
   test_audio_metadata(copy_file, bitrate, duration, 'New Artist', 'New Date', 'New Title')


invalid_save_locations = [
   ('tests/resources/test_files/How Canadas Universal HealthCare System Works.mp3', '/non_existent_folder/How Canadas Universal HealthCare System Works.mp3')
]


@pytest.mark.parametrize("path, save_path", invalid_save_locations)
def test_audio_invalid_save_location(path, save_path):
   file_obj = File(path)
   with pytest.raises(FileProcessingFailedError):
      file_obj.save(save_path)


corrupted_files = [
   'tests/resources/test_files/Super Easy French Corrupted.mp3'
]

@pytest.mark.parametrize("path", corrupted_files)
def test_audio_corrupted_file_processing(path):
   with pytest.raises(FileProcessingFailedError):
      File(path)