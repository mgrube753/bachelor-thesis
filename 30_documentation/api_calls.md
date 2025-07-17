# `api_calls.py`

This script is the central hub for interacting with various Large Language Model (LLM) APIs. It provides a unified interface to generate text from Google, Anthropic, and OpenAI models.

Note: DeepSeek is not included in this script, as it is handled separately in `question_generation.py` creating empty files for these questions. The questions were generated using DeepSeek on its website instead of through API calls.

## Core Functionality

The script abstracts the specific implementation details of each API, allowing other parts of the application to request text generation simply by specifying the provider's name.

## Key Functions

### Provider-Specific Functions

- `gen_with_google(client, prompt_text, model_id, max_tokens)`: Handles text generation using the Google Gemini API. It includes logic to manage responses, especially when the output is truncated due to token limits.
  - **Source:** [Google AI Gemini API Docs](https://ai.google.dev/gemini-api/docs/text-generation)

- `gen_with_anthropic(client, prompt_text, model_id, max_tokens)`: Manages text generation with the Anthropic Claude API. It also checks for and handles cases where the maximum token limit is reached.
  - **Source:** [Anthropic API Docs](httpss://docs.anthropic.com/en/api/handling-stop-reasons)

- `gen_with_openai(client, prompt_text, model_id, max_tokens)`: Responsible for text generation via the OpenAI API. It includes checks for incomplete responses caused by token limits.
  - **Source:** [OpenAI API Docs](httpss://platform.openai.com/docs/quickstart)

### Main Interface

- `llm_generation(llm_name, clients, prompt_text, max_tokens)`: The primary function called by other scripts. It acts as a dispatcher, selecting the correct provider-specific function based on `llm_name`. It retrieves the appropriate client and model ID and introduces a delay between API calls to prevent rate-limiting issues.

## Dependencies

- **Internal Modules:**
  - `constants`: Provides the request delay duration and a mapping of LLM names to their specific model IDs.
- **External Libraries:**
  - `google.genai`: The official Python client for the Google Gemini API.
