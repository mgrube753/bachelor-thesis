# `constants.py`

This script serves as a centralized configuration file, defining constants that are used across the entire project. This approach makes the codebase cleaner, easier to maintain, and less prone to errors, as key values are defined in a single location.

## Path Definitions

The script constructs absolute paths to the main project directories, ensuring that file access is consistent regardless of where the scripts are executed from.

- `BASE_PROJECT_PATH`: The root directory of the project.
- `EXPERIMENTS_BASE_PATH`: The main folder for all experiment-related files.
- `INPUT_SOURCES_PATH`: The location of the source texts.
- `PROMPT_TEMPLATES_PATH`: The directory containing all prompt templates.
- `ANALYSES_PATH`: The folder where analysis results and CSV files are stored.
- `EXP1_PATH` and `EXP2_PATH`: Paths to the specific directories for experiment 1 and 2.

## Model and API Configuration

- `LLM_MODEL_IDS`: A dictionary mapping the internal names of the LLMs (`google`, `anthropic`, `openai`) to their specific model identifiers used by the APIs.
- `LLM_NAMES`: The keys from `LLM_MODEL_IDS`, providing a simple list of the LLMs used.
- `EMBEDDING_MODEL_ID`: The identifier for the sentence-transformer model used for quantitative analysis. This model is sourced from Hugging Face.
  - **Source:** [T-Systems-onsite/cross-en-de-roberta-sentence-transformer](https://huggingface.co/T-Systems-onsite/cross-en-de-roberta-sentence-transformer)
- `REQUEST_DELAY_SECONDS`: A delay (in seconds) applied between API calls to prevent rate-limiting.

## Experiment-Specific Parameters

### Experiment 1

- `EXP1_PROMPT_TYPES`: The types of prompts used.
- `EXP1_SOURCE_TYPES_A`: The different source materials for experiment 1a.
- `EXP1_SOURCE_TYPE_B`: The source material for experiment 1b.
- `LAYERS`: The different layers or sections of the source texts.

### Experiment 2

- `TANENBAUM_LAYER_FOR_EXP2`: The specific layer of the "tanenbaum" source used.
- `EXP2_QUESTION_TYPES`: The types of questions generated.
- `BLOOM_LEVELS_ORDERED`: The levels of Bloom's Taxonomy, in order.
- `BLOOM_DATA_FILE`: The path to the markdown file containing data related to Bloom's Taxonomy.
