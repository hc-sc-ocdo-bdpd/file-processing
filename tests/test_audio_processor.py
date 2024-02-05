import pytest
import sys, os
sys.path.append(os.path.join(sys.path[0], 'file_processing'))
from file_processing.file import File
from mutagen import File as MutagenFile
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.oggvorbis import OggVorbis
from mutagen.mp4 import MP4
from errors import FileProcessingFailedError
from unittest.mock import patch


variable_names = "path, bitrate, length, artist, date, title, organization"
values = [
   ('tests/resources/test_files/How Canadas Universal HealthCare System Works.mp3', 230679, 576.048, '', '', '', ''),
   ('tests/resources/test_files/Super Easy French.wav', 1536000 , 218.9706875, '', '', '', ''),
   ('tests/resources/test_files/Taylor Swift.mp4', 0, 228.4843537414966, '', '', '', ''),
   ('tests/resources/test_files/Jingle Bell Rock.flac', 710366 , 145.61233560090702, '', '', '', ''),
   ('tests/resources/test_files/Katy Perry.aiff', 1411200, 289.9243537414966, '', '', '', ''),
   ('tests/resources/test_files/Frosty the Snowman.ogg', 112000 , 137.71755102040817, '', '', '', '')
]


@pytest.mark.parametrize(variable_names, values)
def test_audio_metadata(path, bitrate, length, artist, date, title, organization):
   file_obj = File(path)
   assert file_obj.metadata['bitrate'] == bitrate
   assert file_obj.metadata['length'] == length
   assert file_obj.metadata['artist'] == artist
   assert file_obj.metadata['date'] == date
   assert file_obj.metadata['title'] == title
   assert file_obj.metadata['organization'] == organization

@pytest.fixture()
def copy_file(path, tmp_path_factory):
   try:
      from pathlib import Path
      copy_path = str(tmp_path_factory.mktemp("copy") / Path(path).name)
      file_obj = File(path)
      file_obj.save(copy_path)
      yield copy_path
   except:
      yield path


@pytest.mark.parametrize("path, bitrate, length", map(lambda x: x[:3], values))
def test_save_audio_metadata(copy_file, bitrate, length):
   audio_file = File(copy_file)
   if audio_file.extension in [".mp3", ".mp4", ".flac", ".ogg"]:
      # Load and change metadata via File object
      audio_file.metadata['artist'] = 'New Artist'
      audio_file.metadata['date'] = '2023-11-22'
      audio_file.metadata['title'] = 'New Title'
      audio_file.metadata['organization'] = 'Health Canada'
      # Save the updated file
      audio_file.save()
      test_audio_metadata(copy_file, bitrate, length, 'New Artist', '2023-11-22', 'New Title', 'Health Canada')
   else:
      with pytest.raises(FileProcessingFailedError):
         audio_file.save()


@pytest.mark.parametrize("path, bitrate, length", map(lambda x: x[:3], values))
def test_change_audio_artist_title_date(copy_file, bitrate, length):
   audio_file = MutagenFile(copy_file)
   if isinstance(audio_file, (MP3, FLAC, OggVorbis, MP4)):
      # Change metadata via Document object
      audio_file = MutagenFile(copy_file)
      if isinstance(audio_file, MP3):
         audio_file = EasyID3(copy_file)
         audio_file['artist'] = "New Artist"
         audio_file['date'] = "2023-11-22"
         audio_file['title'] = "New Title"
         audio_file['organization'] = "Health Canada"
      elif isinstance(audio_file, (FLAC, OggVorbis)):
         audio_file['ARTIST'] = "New Artist"
         audio_file['DATE'] = "2023-11-22"
         audio_file['TITLE'] = "New Title"
         audio_file['ORGANIZATION'] = "Health Canada"
      elif isinstance(audio_file, MP4):
         audio_file.tags['\xa9ART'] = "New Artist"
         audio_file.tags['\xa9day'] = "2023-11-22"
         audio_file.tags['\xa9nam'] = "New Title"
         audio_file.tags['\xa9wrk'] = "Health Canada"
      # Save the file
      audio_file.save()
      test_audio_metadata(copy_file, bitrate, length, 'New Artist', '2023-11-22', 'New Title', 'Health Canada')
   else:
      with pytest.raises(FileProcessingFailedError):
         File(copy_file).save()


@pytest.mark.parametrize(variable_names, values)
def test_not_opening_file(path, bitrate, length, artist, date, title, organization):
    with patch('builtins.open', autospec=True) as mock_open:
        file_obj = File(path, open_file=False)
        mock_open.assert_not_called()


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