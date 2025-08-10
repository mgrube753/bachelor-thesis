# `analysis_quantitative.py`

This script performs a quantitative analysis of the questions generated in Experiment 1 (`exp1a` and `exp1b`). It focuses on measuring the adherence of the questions to their source material using two methods: cosine similarity and LLM-based evaluation.

## Core Functionality

The script processes experiment data from CSV files, loads the generated questions and their corresponding source texts, and then calculates two types of adherence scores. The results, including both scores, are saved back to the CSV files.

## Key Functions

### Adherence Measurement

- `calc_cossim_batch(model, questions, sources)`: Calculates the cosine similarity between question embeddings and source text embeddings. It uses a `SentenceTransformer` model to generate the embeddings in batches for efficiency.
- `get_adherence_scores(clients, question, source_text, evaluator)`: Uses an LLM (OpenAI or Anthropic) to evaluate how well a question adheres to the provided source text. It returns a score between 0 and 1.
- `get_adherence_scores_parallel(...)`: Wraps `get_adherence_scores` to run evaluations for multiple question-source pairs in parallel, using both OpenAI and Anthropic models.

### File and Data Handling

- `get_question_path(...)`: Constructs the file path for a specific question based on experiment details.
- `get_source_file_path(...)`: Constructs the file path for a source text, handling normal, manipulated, and "no_source" cases.
- `expand_no_source_data(df)`: A special handler for the `exp1a_no_source` case. It expands the dataset so that questions generated without a source are compared against all three possible source texts (`script`, `tanenbaum`, `transcript`).

### Main Processing Logic

- `process_experiment(exp_name)`: The main function that orchestrates the analysis for a given experiment. It performs the following steps:
  1. Loads the appropriate sentence-embedding model and initializes LLM clients.
  2. Reads the experiment data from a CSV file.
  3. Loads all relevant question-source pairs.
  4. Calculates cosine similarity for all pairs and saves the results.
  5. Calculates LLM-based adherence scores for all pairs and saves the results.

## Dependencies

- **External Libraries:**
  - `pandas`: For data manipulation.
  - `numpy`: For numerical operations.
  - `sentence-transformers`: For generating text embeddings.
  - `scikit-learn`: For calculating cosine similarity.
  - `tqdm`: For progress bars.
- **Internal Modules:**
  - [`constants`](../20_experiments/50_src/constants.py): Provides file paths and model IDs.
  - [`file_utils`](../20_experiments/50_src/file_utils.py): For loading text files.
  - [`api_calls`](../20_experiments/50_src/api_calls.py): For making requests to LLM APIs.
  - [`api_config`](../20_experiments/50_src/api_config.py): For initializing API clients.
