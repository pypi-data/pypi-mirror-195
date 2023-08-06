# Sabia Utils

This is a collection of utilities for Sabia.

## Concat Module

This module is used to concatenate files.


### Concatenate all files from a path

Returns a concatenated dataframe from all files in a path.
Can save the concatenated dataframe to a file.

```python
from sabia_utils import concat

concat.concatenate_all_from_path(
    path='path/to/files',
    output_file='output/file/path', # optional
    fine_name='file_name'           # optional 
)
```
