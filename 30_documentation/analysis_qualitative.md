# `analysis_qualitative.py`

**Note:** This script is marked as discarded and is no longer in use. The qualitative analysis is now performed by human experts instead of using this prolonged python script.

This script was designed to automate the qualitative analysis of questions generated in two experiments (`exp1` and `exp2`). It uses Large Language Models (LLMs) from OpenAI and Anthropic to evaluate questions based on a predefined rubric.

## Core Functionality

The script reads experiment data from CSV files, retrieves the generated questions and their original contexts, and then uses LLMs to score the questions on various criteria. The results are saved back to new CSV files.

## Key Functions

### Evaluation Setup

- `get_rubric(exp_name)`: Loads the evaluation rubric for a given experiment.
- `get_eval_prompt()`: Loads the main prompt template for the evaluation task.
- `get_source(...)`: Retrieves the source text used as context for a question.
- `find_question(...)`: Finds and loads the text of a specific question file.

### Evaluation and Scoring

- `evaluate_single(clients, llm, question, context, rubric)`: Sends a request to an LLM to evaluate a single question against the context and rubric. It parses the scores from the response.
- `calculate_bloom_score(exp_name, bloom_rating, bloom_original=None)`: Calculates a score based on Bloom's Taxonomy levels, specific to Experiment 2.

### Experiment Processing

- `process_exp1(exp_name, clients)`: Manages the evaluation process for Experiment 1 (`exp1a`, `exp1b`). It handles file paths, loads data, and orchestrates the evaluation of each question in parallel.
- `process_exp2(exp_name, clients)`: Manages the evaluation process for Experiment 2 (`exp2a`, `exp2b`, `exp2c`). Similar to `process_exp1`, but adapted for the structure of the second experiment.

### Main Execution

- `main()`: Initializes the LLM clients and calls the processing functions for the specified experiments.

## Dependencies

- **External Libraries:**
  - `pandas`: For data manipulation with DataFrames.
  - `tqdm`: For displaying progress bars.
- **Internal Modules:**
  - [`constants`](../20_experiments/50_src/constants.py): Provides paths to various project directories.
  - [`file_utils`](../20_experiments/50_src/file_utils.py): For loading text files.
  - [`api_calls`](../20_experiments/50_src/api_calls.py): Handles the interaction with LLM APIs.
  - [`api_config`](../20_experiments/50_src/api_config.py): For initializing the API clients.
