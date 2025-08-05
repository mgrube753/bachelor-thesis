# `file_utils.py`

This script provides utility functions for file operations, including loading several TXT files (e.g. source texts), saving generated questions, and also normalizing text for use as filenames.

## Functions

### `load_txt(file_path)`

Loads a text file from the given `file_path`.

- **Parameters:**
  - `file_path` (str): The path to the text file.
- **Returns:**
  - The content of the file as a string, or `None` if an error occurs.

### `save_result(file_path, content)`

Saves the given `content` to a file at the specified `file_path`. It creates the necessary directories if they don't exist.

- **Parameters:**
  - `file_path` (str): The path where the file will be saved.
  - `content` (str): The content to be written to the file.

### `slugify(text)`

Converts a string into a "slug" by making it lowercase and replacing spaces and hyphens with underscores. This is useful for creating valid filenames from text.

- **Parameters:**
  - `text` (str): The input string.
- **Returns:**
  - The normalized string.
