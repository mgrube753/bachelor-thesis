# `sampling.py`

This script prepares data for human evaluation by automating the sampling of generated questions, the creation of CSV files for evaluators, and the renaming of sampled files for the blind tests of Experiment 1 and 2.

## Overview

The script follows a three-stage process:

1. **Sampling**: Randomly selects a specified number of question files from each experimental condition in the experiment output directories.
2. **CSV Generation**: Produces structured CSV files for different evaluation tasks (e.g. qualitative analysis by experts and students), including hint files and evaluation templates.
3. **Renaming**: Copies the sampled question files to a new directory with standardized, anonymized filenames for manual review.

## Main Functions

- `sample_questions(...)` and `walk_and_sample(...)`:
    - Traverse the experiment output directories ([`../20_experiments/10_exp1`](../20_experiments/10_exp1), [`../20_experiments/20_exp2`](../20_experiments/20_exp2)).
    - Randomly select a specified number of `.txt` question files from each condition (e.g. for each LLM, prompt type, and source).
    - Copy the selected files to the [`../20_experiments/70_samples/`](../20_experiments/70_samples/) directory.

- `parse_file_path(parts)`:
    - Parses a file path to extract experimental parameters (such as `exp_name`, `llm`, `layer`, etc.) for downstream processing.

- `generate_expert_csvs(sample_base, csv_path)`:
    - Walks through the [`../20_experiments/70_samples/`](../20_experiments/70_samples/) directory and uses `parse_file_path` to create structured records for each sampled question.
    - Generates multiple CSV files in [`../20_experiments/60_analyses/csv/`](../20_experiments/60_analyses/csv/), including:
        - Evaluation template CSVs for experts (exp1) and students (exp2), with appropriate columns for each experimental phase.
        - Hint files for each experiment phase (including information unknown to the raters, about the LLM used etc.).

- `find_file(...)` and `get_source_type(...)`:
    - Helper functions to locate the original file path of a sampled question and determine its source type for renaming.

- `rename_samples(samples, csv_path, output_path)`:
    - Reads the generated CSVs and, for each sampled question, creates a new anonymized filename (e.g. `001_script_2.txt`).
    - Copies the files to the [`../20_experiments/80_samples_renamed/`](../20_experiments/80_samples_renamed/) directory, making them ready for manual review without revealing the LLM or other sensitive details.

- `main()`:
    - Orchestrates the entire process: sets a random seed for reproducibility, ensures output directories exist, performs sampling, generates CSVs, and renames samples.
    - Prints progress and summary information.

## Dependencies

- **External Libraries**:
    - `pandas`: For creating and managing CSV files.
- **Internal Modules**:
    - [`constants`](../20_experiments/50_src/constants.py): Provides base paths for experiment, sample, and analysis directories.
