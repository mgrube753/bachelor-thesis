# Documentation

This directory contains comprehensive technical documentation for the bachelor thesis project.

## Purpose

- **API Integration Guides:**  
  Step-by-step instructions for configuring and using LLM providers (OpenAI, Anthropic, Google, DeepSeek).

- **Code Reference:**  
  Detailed documentation for each experimental script, including usage, dependencies, and workflow.

- **Setup Instructions:**  
  Environment setup, dependency installation, and configuration tips.

- **Analysis Workflows:**  
  Guides for running quantitative and qualitative analyses, including evaluation procedures and result interpretation.

## Structure

- Each Python script in [`20_experiments/50_src/`](../20_experiments/50_src/) is documented by a corresponding `.md` file in this directory.
- Jupyter notebooks for analysis are located in [`20_experiments/50_src/`](../20_experiments/50_src/):
  - [`50_src/evaluation1_quan.ipynb`](../20_experiments/50_src/evaluation1_quan.ipynb)
  - [`50_src/evaluation1_qual.ipynb`](../20_experiments/50_src/evaluation1_qual.ipynb)
  - [`50_src/evaluation2_qual.ipynb`](../20_experiments/50_src/evaluation2_qual.ipynb)
- Prompt templates and evaluation rubrics are in [`20_experiments/40_prompts/`](../20_experiments/40_prompts/).
- API key setup has to be done in a [`.env`](../.env) file, as explained in the main [`README.md`](../README.md).
- Python dependencies are listed in [`requirements.txt`](../requirements.txt).
