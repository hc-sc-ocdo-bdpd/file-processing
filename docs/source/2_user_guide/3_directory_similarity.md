# Identifying similar files within a directory

```{eval-rst}
.. automethod:: file_processing.Directory.identify_duplicates
   :no-index:
```

This method aims to identify similar document-based files in a directory. There are 2 similarity metrics

```{tab} Code
```python
from file_processing import Directory
directory = Directory('./tests/resources/similarity_test_files/')
directory.identify_duplicates(report_file='./docs/sample_reports/similarity_cosine.csv',
                              filters={}, 
                              threshold=0,
                              top_n=0,
                              use_abs_path=True)
```
```{tab} Compare all files
```{image} ../resources/cosine_similarity.png
:align: center
```
```{tab} Find top matches
```{image} ../resources/faiss_similarity.png
:align: center
```