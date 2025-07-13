# `api_config.py`

This script is responsible for configuring and initializing the API clients required to communicate with the different Large Language Models (LLMs).

## Core Functionality

The script securely loads API keys from a `.env` file and uses them to create and configure client objects for Google, Anthropic, and OpenAI.

## Key Functions

- `load_api_keys()`:
  - Loads environment variables from a `.env` file using `python-dotenv`.
  - Retrieves the API keys for Google, Anthropic, and OpenAI.
  - Performs a crucial check to ensure all required keys are present, raising an error if any are missing.
  - **Source:** This function relies on the `python-dotenv` library. More information can be found here: [pypi.org/project/python-dotenv/](https://pypi.org/project/python-dotenv/)

- `init_clients()`:
  - Calls `load_api_keys()` to get the necessary credentials.
  - Initializes the client object for each of the three services (`google.genai.Client`, `anthropic.Anthropic`, `openai.OpenAI`).
  - Returns a dictionary containing the initialized clients, keyed by the provider name (`google`, `anthropic`, `openai`). This dictionary is then used by other parts of the application to make API calls.

## Usage

This script is typically called at the beginning of any process that needs to interact with an LLM. The returned dictionary of clients is passed to functions in `api_calls.py`.

## Dependencies

- **External Libraries:**
  - `python-dotenv`: To load API keys from a `.env` file.
  - `google.genai`: The client library for Google's API.
  - `anthropic`: The client library for Anthropic's API.
  - `openai`: The client library for OpenAI's API.
