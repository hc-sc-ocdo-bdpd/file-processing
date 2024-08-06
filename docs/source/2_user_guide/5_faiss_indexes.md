<br>

# FAISS Indexes

The `faiss_index` import offers a collection of functions that make it easy to interface with FAISS indexes. A `faiss_index` object can be created by either:

* calling one of the create index methods such as `faiss_index.create_flat_index(embeddings)` or `faiss_index.create_ivf_index(embeddings, nlist=16)`.
* loading an index from a `.faiss` file using `faiss_index.load_index("path/to/file.faiss")`.

Once an index is created it can be queried. This involves providing a query vector as an input and the index will return the nearest `k` vectors contained in the index (as found by that algorithm). Consider the example below to view the functionality:

```python
index = faiss_index.load_index("path/to/file.faiss")
nearest_three_vectors = index.query(query_vector, k=3)
```

For large numbers of documents, creating the index can take a while so it is often a good idea to save the file to be loaded in for future use. This can be done by specifying the file path when creating the index or by calling `save()`.

```python
# save the index when creating it
index = faiss_index.create_flat_index(embeddings, "path/to/save.faiss")
# save the index afetr creating it
index = faiss_index.create_flat_index(embeddings)
index.save("path/to/save.faiss")
```

The ability to create indexes is limited to a select number of common indexes. More complex indexes can still be loaded and queried as with the other indexes but does not come with the ability to adjust hyperparameters during the query.