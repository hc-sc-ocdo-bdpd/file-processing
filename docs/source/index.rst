:hide-toc: true:

.. toctree::
   :hidden:
   :glob:
   :maxdepth: 2
   :caption: Tutorial:

   1_tutorial/*

.. toctree::
   :hidden:
   :glob:
   :maxdepth: 2
   :caption: User Guide:

   2_user_guide/*

.. toctree::
   :hidden:
   :glob:
   :maxdepth: 2
   :caption: Developer Guide:

   3_developer_guide/*

.. toctree::
   :hidden:
   :glob:
   :maxdepth: 2
   :caption: Additional Information:

   4_additional_information/*


File Processing
===============



The file processing library is a metadata extraction tool that supports 26 common file types, 
including OCR for image files and transcription for audio/video files. There are 4 main use cases:

1. Extracting metadata from individual files 

2. Recursively extracting metadata from directories and generating CSV reports that

   - list metadata for each file

   - provide aggregate statistics on file size and file count versus file type

   - compare file similarity of text-based documents to identify possible duplicates


------------------------
Example Usage and Output
------------------------


-------------------------------------------
Supported File Types and Extracted Metadata
-------------------------------------------

+--------------------------------+-----------------------+---------+
| File Type                      | Metadata Fields       | Example |
+================================+=======================+=========+
| [Generic]                      | - file_path           |         |
|                                | - file_name           |         |
|                                | - extension           |         |
|                                | - owner               |         |
|                                | - size                |         |
|                                | - modification_time   |         |
|                                | - access_time         |         |
|                                | - creation_time       |         |
|                                | - permissions         |         |
|                                | - parent_directory    |         |
|                                | - is_file             |         |
|                                | - is_symlink          |         |
|                                | - absolute_path       |         |
+--------------------------------+-----------------------+---------+
| mp3, wav, mp4, flac, aiff, ogg | - bitrate             |         |
|                                | - length              |         |
|                                | - artist              |         |
|                                | - date                |         |
|                                | - title               |         |
+--------------------------------+-----------------------+---------+
| csv                            | - text                |         |
|                                | - encoding            |         |
|                                | - num_rows            |         |
|                                | - num_cols            |         |
|                                | - num_cells           |         |
|                                | - empty_cells         |         |
+--------------------------------+-----------------------+---------+

DOCX
text 
author 
last_modified_by 
has_password 

GIF: 
original_format 
mode 
width 
height 
animated 
frames 

jpeg, png, heic, heif, tiff, tif
original_format 
mode 
width 
height 

HTML: 
text 
encoding 
lines 
words 
num_lines 
num_words 

JSON: 
text 
encoding 
num_keys 
key_names 
empty_values 

MSG: 
text 
subject 
date 
sender 

PDF: 
text 
has_password 
author 
producer 

PPTX: 
text 
author 
last_modified_by 
num_slides 
has_password 

PY: 
num_lines 
num_functions 
num_classes 
imports 
docstrings 

RTF: 
text 

TXT: 
text 
encoding 
lines 
words 
num_lines 
num_words 

XLSX: 
active_sheet 
sheet_names 
data 
last_modified_by 
creator 
has_password 

XML: 
text 
encoding 
lines 
words 
num_lines 
num_words 

ZIP: 
num_files 
file_types 
file_names 
