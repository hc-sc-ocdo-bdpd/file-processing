<br>

# Getting started

There are 2 exported classes that must be initiatized to access their respective methods and attributes: the `File` and `Directory` classes

<br>

## File

This class is for extracting metadata from a single file:

```py
from file_processing import File

file = File('path/to/file')
```

<br>

### Metadata extraction

Once initialized, attributes can be directly extracted by `file.attribute_name`. For example:

```py
file.access_time
```

It is also possible to read all metadata from the File object as a dictionary. Note that the key names will vary as each file type may have its own metadata, as defined in the [Introduction](../index.rst)

```{tab} Code
    metadata = file.processor.__dict__
```
```{tab} Output
    {
        'file_path': './requirements.txt,
        'open_file': True,
        'file_name': 'requirements.txt',
        'owner': 'AD/BLUO',
        'extension': '.txt',
        'size': 411,
        'modification_time': 1707156577.8320045,
        'access_time': 1707224508.0667744,
        'creation_time': 1705332838.3662565,
        'parent_directory': 'report',
        'permissions': '666',
        'is_file': True,
        'is_symlink': False,
        'absolute_path': WindowsPath('C:/Users/User/Downloads/report/requirements.txt'),
        'metadata': {
            'text': ...
            'encoding': 'ascii',
            'lines': [...],
            'num_lines': 23,
            'num_words': 22
        }
    }
```

<br>

### Measuring similarity between 2 files

To check the similarity between 2 files, the file objects must first be defined. Afterward, `CosineSimilarity` or `LevenshteinDistance` objects can be used to compare the files:

```{tab} Cosine Similarity
```python
from file_processing import File, CosineSimilarity

a = File('path/to/fileA.docx')
b = File('path/to/fileA.pdf')

CosineSimilarity(a, b).calculate()

>>> 0.6715940803327793
```
```{tab} Levenshtein Distance
```python
from file_processing import File, LevenshteinDistance

a = File('path/to/fileA.docx')
b = File('path/to/fileA.pdf')

LevenshteinDistance(a, b).calculate()

>>> 4135
```

<br>

## Directory

This class is for extracting metadata from every file in a directory:

```py
from file_processing import Directory

directory = Directory('path/to/directory')
```

<br>

### Generating a metadata report from a directory

Use the `generate_report()` class method to create a CSV report with the metadata of all files in the directory. 

See more details and examples [here](../2_user_guide/1_directory_report.md)

```{eval-rst}
.. automethod:: file_processing.Directory.generate_report
```

<br>

### Analyzing a directory's metadata

Use the `generate_analytics()` class method to create a CSV report that aggregates the file count and file size for each file type. This is useful for analyzing the composition of a directory.

See more details and examples [here](../2_user_guide/2_directory_analytics.md)

```{eval-rst}
.. automethod:: file_processing.Directory.generate_analytics
```

<br>

### Identifying similar files within a directory

Use the `identify_duplicates()` class method to create a CSV that compares file similarities. There are 2 configurations for this: 
1. Use cosine similarity to compare every file against each other
2. Use FAISS indicies to return to return the `top_n` most similar files

See more details and examples [here](../2_user_guide/3_directory_similarity.md)

```{eval-rst}
.. automethod:: file_processing.Directory.identify_duplicates
```

<br>

For an end-to-end example on usage, see the [JupyTer notebook tutorial](https://github.com/hc-sc-ocdo-bdpd/file-processing-tools/blob/main/report_demo.ipynb)