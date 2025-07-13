# `question_generation.py`

This script is the core engine for the entire project, responsible for executing the question generation experiments. It systematically generates questions by combining different LLMs, source texts, and prompt templates according to the defined experimental design.

## Core Functionality

The script is organized into functions, each corresponding to a specific part of the two main experiments. It uses a multi-threaded approach to send requests to the LLM APIs in parallel, significantly speeding up the generation process.

### General Workflow

1. **Task Preparation**: For each experiment, a list of `tasks` is created. Each task is a tuple containing all the necessary information for a single LLM call (LLM name, client, prompt, output path, etc.).
2. **CSV Creation**: An initial CSV file is created for each experiment to log the parameters of each generated question. This file is later used for analysis.
3. **Parallel Execution**: The `run_tasks` function uses a `ThreadPoolExecutor` to process the list of tasks concurrently.
4. **Progress Tracking**: A progress bar (`tqdm`) and custom counters provide real-time feedback on the generation process.
5. **Saving Results**: Each generated question is saved to a unique text file in a structured directory hierarchy.

## Experiment Functions

- `run_exp_1a(clients)`: **Content Fidelity**. Generates questions based on various source texts (`script`, `transcript`, `tanenbaum`) and prompt types.
- `run_exp_1b(clients)`: **Error Propagation**. Generates questions using source texts that contain known errors to see how LLMs handle them.
- `run_exp_1a_no_source(clients)`: A variation of 1a that prompts the LLM to generate questions about a topic *without* providing the source text directly in the prompt.
- `run_exp_2a(clients)`: **Question Type**. Generates questions of different types (e.g., Multiple-Choice, Open-Ended) based on a single source text.
- `run_exp_2b(clients)`: **Bloom Level**. Generates questions corresponding to different levels of Bloom's Taxonomy.
- `run_exp_2c(clients)`: **Combined**. Generates questions by combining both question type and Bloom's Taxonomy level as variables.

## Helper Functions

- `create_csvs(...)`: Creates the initial CSV log files for each experiment.
- `generate_task(...)`: A single worker function that formats a prompt, sends it to the appropriate LLM, and saves the result.
- `run_tasks(...)`: The multi-threading manager that executes all tasks for an experiment.

## Dependencies

- **External Libraries**:
  - `tqdm`: For displaying progress bars.
- **Internal Modules**:
  - `constants`: Provides all necessary paths, model names, and experiment parameters.
  - `file_utils`: For loading source texts and saving generated questions.
  - `prompt_utils`: For loading and formatting prompt templates.
  - `api_calls`: For making the actual calls to the LLM APIs.
