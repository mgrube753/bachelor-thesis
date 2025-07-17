# `main.py`

This script is the main entry point for running the question generation experiments. It orchestrates the entire process by initializing necessary components and then executing the selected experiment runs.

## Core Functionality

The `main` function serves as the master controller for the project's experiments.

### Key Steps in `main()`

1. **Initialize API Clients**:
   - It begins by calling `init_clients()` from `api_config.py`.
   - This step is critical as it sets up the connection to the various LLM services (Google, Anthropic, OpenAI).
   - It includes error handling to gracefully exit if the API keys are not configured correctly in the `.env` file.

2. **Preload Bloom Data**:
   - It calls `get_bloom()` from `prompt_utils.py`.
   - This function loads and caches the Bloom's Taxonomy data, which is used in prompts for experiment 2. Pre-loading it ensures it's readily available and doesn't need to be read from disk multiple times.

3. **Run Experiments**:
   - The script then calls the specific functions for each part of the experiments.
   - The functions (`run_exp_1a`, `run_exp_1b`, etc.) are imported from `question_generation.py`.
   - The script is structured to allow for selective execution of experiments by commenting or uncommenting the relevant function calls, depending on the desired experiments to run sequentially.

## Execution

To run the experiments, this script is executed from the command line. The commented-out lines can be modified to run any combination of the defined experiments.

## Dependencies

- **Internal Modules**:
  - `api_config`: For initializing the LLM API clients.
  - `question_generation`: Contains the logic for running each specific experiment.
  - `prompt_utils`: For preloading utility data like the Bloom's Taxonomy information.
