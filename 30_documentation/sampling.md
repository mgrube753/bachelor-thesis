# `sampling.py`

This script is responsible for preparing the data for human evaluation. It automates the process of sampling the generated questions, creating CSV files for the evaluators, and renaming the sampled files for easy identification.

## Core Functionality

The script performs a three-step process to prepare the evaluation materials:

1.  **Sampling**: It randomly samples a small number of questions from each experimental condition.
2.  **CSV Generation**: It creates detailed CSV files tailored for different evaluation tasks (qualitative analysis by experts).
3.  **Renaming**: It copies the sampled question files to a new location with standardized, more informative filenames.

## Key Functions

-   `sample_questions(...)` and `walk_and_sample(...)`:
    -   These functions traverse the output directories of the experiments (`10_exp1`, `20_exp2`).
    -   They randomly select a specified number of question files (`.txt`) from each condition (e.g., for each LLM, prompt type, and source).
    -   The selected files are copied to the `70_samples` directory.

-   `parse_file_path(parts)`:
    -   A utility function that deconstructs a file path to extract the experimental parameters (like `exp_name`, `llm`, `layer`, etc.) it represents.

-   `generate_expert_csvs(sample_base, csv_path)`:
    -   Walks through the `70_samples` directory.
    -   Uses `parse_file_path` to create a structured record for each sampled question.
    -   Generates several CSV files in the `60_analyses/csv_files/qualitative` directory, formatted specifically for different expert evaluators and analysis types (e.g., for `exp1a`, `exp1b`, and the different phases of `exp2`).

-   `find_file(...)` and `get_source_type(...)`:
    -   Helper functions to locate the original file path of a sampled question and determine its source type for the renaming process.

-   `rename_samples(samples, csv_path, output_path)`:
    -   Reads the CSVs generated in the previous step.
    -   For each sampled question, it creates a new, standardized filename (e.g., `001_script_manipulated_1.txt`).
    -   Copies the files to the `80_samples_renamed` directory, making them ready for manual review without revealing the LLM that generated them.

-   `main()`:
    -   The main execution function that orchestrates the entire process.
    -   It sets a random seed for reproducibility, cleans up old output directories, and then calls the sampling, CSV generation, and renaming functions in sequence.
    -   Finally, it cleans up intermediate CSV files that are no longer needed.

## Dependencies

-   **External Libraries**:
    -   `pandas`: Used extensively for creating and managing the data for the CSV files.
-   **Internal Modules**:
    -   `constants`: Provides the base paths for the experiment, sample, and analysis directories.
