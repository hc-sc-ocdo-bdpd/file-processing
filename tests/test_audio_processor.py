import pytest
import sys, os
sys.path.append(os.path.join(sys.path[0], 'file_processing'))
from file_processing.file import File
from mutagen import File as MutagenFile
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from errors import FileProcessingFailedError


variable_names = "path, length, artist, date, title"
values = [
   ('tests/resources/test_files/How Canadas Universal HealthCare System Works.mp3', 576.048, '', '', ''),
   ('tests/resources/test_files/Super Easy French.mp3', 219.0, '', '', ''),
   ('tests/resources/test_files/How Canadas Universal HealthCare System Works.wav', 576.0123263888889, '', '', ''),
   ('tests/resources/test_files/Super Easy French.wav', 218.9706875, '', '', '')
]


@pytest.mark.parametrize(variable_names, values)
def test_audio_metadata(path, length, artist, date, title):
   file_obj = File(path)
   assert file_obj.metadata['length'] == length
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


@pytest.mark.parametrize("path, length", map(lambda x: x[:2], values))
def test_save_audio_metadata(copy_file, bitrate, length):

   # Load and change metadata via File object
   audio_file = File(copy_file)
   audio_file.metadata['artist'] = 'New Artist'
   audio_file.metadata['date'] = 'New Date'
   audio_file.metadata['title'] = 'New Title'

   # Save the updated file
   audio_file.save()
   test_audio_metadata(copy_file, bitrate, length, 'New Artist', 'New Date', 'New Title')


@pytest.mark.parametrize("path, length", map(lambda x: x[:2], values))
def test_change_audio_artist_title_date(copy_file, bitrate, length):

   # Change metadata via Document object
   audio_file = MutagenFile(copy_file)
   if isinstance(audio_file, MP3):
      audio_file = EasyID3(copy_file)
   audio_file['artist'] = "New Artist"
   audio_file['date'] = "New Date"
   audio_file['title'] = "New Title"

   # Save the file
   audio_file.save()
   test_audio_metadata(copy_file, length, 'New Artist', 'New Date', 'New Title')


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