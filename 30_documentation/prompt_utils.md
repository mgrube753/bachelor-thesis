# `prompt_utils.py`

This script provides a set of utility functions for loading, formatting, and managing prompt templates, with a special focus on handling data related to Bloom's Taxonomy.

## Core Functionality

The script streamlines the process of working with prompts by centralizing loading and formatting logic.

## Key Functions

- `load_prompt(prompt_name)`:
  - Loads a prompt template from the `40_prompts` directory.
  - It automatically appends the `.md` extension if it's not already present.

- `format_prompt(template, **values)`:
  - Formats a given prompt `template` by substituting placeholders (e.g., `{text}`) with actual values.
  - It includes error handling to prevent crashes if a key is missing in the provided `values`.

- `parse_bloom_md(md_content)`:
  - Parses the content of the `bloom.md` file.
  - It extracts the descriptions and action verbs for each level of Bloom's Taxonomy and organizes them into a structured dictionary.

- `get_bloom()`:
  - A cached function to retrieve the parsed Bloom's Taxonomy data.
  - On its first call, it loads and parses the `bloom.md` file using `parse_bloom_md`.
  - On subsequent calls, it returns the cached data, avoiding redundant file I/O and parsing. This improves efficiency.

- `q_format(q_type)`:
  - Returns a pre-defined format string for a given question type (`Multiple-Choice` or `Open-Ended`).
  - This ensures that the generated questions have a consistent structure.

## Dependencies

- **Internal Modules**:
  - `constants`: Provides the file path to the Bloom's Taxonomy data file (`BLOOM_DATA_FILE`) and the path to the prompt templates directory (`PROMPT_TEMPLATES_PATH`).
  - `file_utils`: Used to load the raw text content of the prompt and Bloom files.
