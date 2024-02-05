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


===============
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

Test files can be found in `docs/sample_reports` and examples are shown below

.. tab:: Metadata Report

    Lists metadata of all files

    .. image:: ./resources/metadata_report.png
       :align: center
     

.. tab:: Analytics Report

    Second.

    .. image:: ./resources/analytics_report.png
       :align: center
     

.. tab:: Similarity Report (1)

    Second.

    .. image:: ./resources/cosine_similarity.png
       :align: center
     

.. tab:: Similarity Report (2)

    .. image:: ./resources/faiss_similarity.png
       :align: center
     

.. tab:: File Metadata

    .. code:: python

        from file_processing import File

        file = File('path/to/file')
        print(file.metadata)

    .. code:: none

        {
            'original_format': 'PNG', 
            'mode': 'RGBA', 
            'width': 1188, 
            'height': 429
        }

-------------------------------------------
Supported File Types and Extracted Metadata
-------------------------------------------

+--------------------------------+-----------------------+---------+
| File Type                      | Metadata Fields       | Example |
+================================+=======================+=========+
| [All file types]               | - file_path           |         |
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
| jpeg, png, heic/heif, tiff/tif | - original_format     |         |
|                                | - mode                |         |
|                                | - width               |         |
|                                | - height              |         |
+--------------------------------+-----------------------+---------+
| gif                            | - original_format     |         |
|                                | - mode                |         |
|                                | - width               |         |
|                                | - height              |         |
|                                | - animated            |         |
|                                | - frames              |         |
+--------------------------------+-----------------------+---------+
| csv                            | - text                |         |
|                                | - encoding            |         |
|                                | - num_rows            |         |
|                                | - num_cols            |         |
|                                | - num_cells           |         |
|                                | - empty_cells         |         |
+--------------------------------+-----------------------+---------+
| xlsx                           | - active_sheet        |         |
|                                | - sheet_names         |         |
|                                | - data                |         |
|                                | - last_modified_by    |         |
|                                | - creator             |         |
|                                | - has_password        |         |
+--------------------------------+-----------------------+---------+
| docx                           | - text                |         |
|                                | - author              |         |
|                                | - last_modified_by    |         |
|                                | - has_password        |         |
+--------------------------------+-----------------------+---------+
| pptx                           | - text                |         |
|                                | - author              |         |
|                                | - last_modified_by    |         |
|                                | - num_slides          |         |
|                                | - has_password        |         |
+--------------------------------+-----------------------+---------+
| html, txt, xml                 | - text                |         |
|                                | - encoding            |         |
|                                | - lines               |         |
|                                | - words               |         |
|                                | - num_lines           |         |
|                                | - num_words           |         |
+--------------------------------+-----------------------+---------+
| json                           | - text                |         |
|                                | - encoding            |         |
|                                | - num_keys            |         |
|                                | - key_names           |         |
|                                | - empty_values        |         |
+--------------------------------+-----------------------+---------+
| msg                            | - text                |         |
|                                | - subject             |         |
|                                | - date                |         |
|                                | - sender              |         |
+--------------------------------+-----------------------+---------+
| pdf                            | - text                |         |
|                                | - has_password        |         |
|                                | - author              |         |
|                                | - producer            |         |
+--------------------------------+-----------------------+---------+
| py                             | - num_lines           |         |
|                                | - num_functions       |         |
|                                | - num_classes         |         |
|                                | - imports             |         |
|                                | - docstrings          |         |
+--------------------------------+-----------------------+---------+
| rtf                            | - text                |         |
+--------------------------------+-----------------------+---------+
| py                             | - num_lines           |         |
|                                | - num_functions       |         |
|                                | - num_classes         |         |
|                                | - imports             |         |
|                                | - docstrings          |         |
+--------------------------------+-----------------------+---------+
| text                           | - num_lines           |         |
|                                | - num_functions       |         |
|                                | - num_classes         |         |
|                                | - imports             |         |
|                                | - docstrings          |         |
+--------------------------------+-----------------------+---------+
| zip                            | - num_files           |         |
|                                | - file_types          |         |
|                                | - file_names          |         |
+--------------------------------+-----------------------+---------+

