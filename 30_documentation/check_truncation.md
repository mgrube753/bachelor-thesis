# `check_truncation.py`

This script is a diagnostic tool used to check whether text files will be truncated by the sentence-embedding model due to exceeding its maximum sequence length. This sentence transformer model was used to generate embeddings between source texts and generated questions which are explicitly comparable by calculating cosine similarity. Before running the quantitative analysis, it is crucial to ensure that all source materials and as many generated questions as possible fit within the model's token limits.

## Core Functionality

The script scans specified directories for `.txt` files, tokenizes their content, and compares the token count against the model's limit. It generates a summary report and saves it to a markdown file.

## Key Components

### `OutputCapture` Class

A helper class to capture all `print` statements into a buffer, allowing the entire script's output to be saved to a file.

### File Processing

- `load_embedding_model(model_name)`: Loads the `SentenceTransformer` model specified by `EMBEDDING_MODEL_ID` from the `constants` module.
- `process_file(file_path, model)`:
  - Reads a single text file.
  - Uses the model's tokenizer to count the number of tokens in the file's content.
  - Determines if the token count exceeds the model's `max_seq_length`.
  - Prints a status line for the file and returns a dictionary with the analysis results.

### Directory Scanning

- `scan_directory(directory, description, model)`:
  - Traverses a given directory to find all `.txt` files.
  - Calls `process_file` for each file found.
  - Compiles the results into a `pandas` DataFrame.
  - Prints a summary for the directory, highlighting any files that will be truncated.

### Main Execution

- `main()`:
  - Initializes the `OutputCapture`.
  - Loads the embedding model.
  - Defines the directories to be scanned (`INPUT_SOURCES_PATH` and `EXP1_PATH`).
  - Calls `scan_directory` for each target directory.
  - Combines the results and prints an overall summary.
  - Saves the captured output, including all summaries and details, to `note_truncation.md`.

## Usage

Running this script provides a clear overview of which source texts or generated questions are too long for the embedding model, which is crucial for the quantitative analysis (`analysis_quantitative.py`).

## Dependencies

- **External Libraries:**
  - `torch`: Used by `sentence-transformers`.
  - `pandas`: For data aggregation and summary.
  - `sentence-transformers`: To access the tokenizer and model properties.
- **Internal Modules:**
  - [`constants`](../20_experiments/50_src/constants.py): Provides file paths and the embedding model ID.
