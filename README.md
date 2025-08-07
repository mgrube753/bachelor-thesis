# Generating Educational Questions using Large Language Models

## Bachelor Thesis by Malte Grube

---

## Table of Contents

1. [Overview](#overview)
2. [Setup & Installation](#setup--installation)
3. [Project Structure](#project-structure)
4. [Running Experiments](#running-experiments)
5. [Analysis & Evaluation](#analysis--evaluation)
6. [Documentation](#documentation)
7. [Thesis & Compilation](#thesis--compilation)
8. [Presentations](#presentations)
9. [Prior Experimental Run](#prior-experimental-run)
10. [License Information](#license-information)

---

## Overview

This repository implements and evaluates a semi-automated pipeline for generating and evaluating educational questions from instructional texts using various Large Language Models (LLMs). \
The experiments focus on:

- **Content Adherence & Error Detection** (Exp 1)
- **Relationship between Question Formats & Bloom’s Taxonomy Alignment** (Exp 2)

Results are analyzed quantitatively (only Exp 1) and qualitatively (both experiments) to assess the quality of LLM-generated questions in certain dimensions.

---

## Setup & Installation

1. Clone the repo

   ```sh
   git clone https://github.com/mgrube753/bachelor-thesis.git
   cd bachelor-thesis
   ```

2. Create a Python 3.x virtual environment, 3.10.14 was used in this thesis. An example for creating a virtual environment is:

   ```sh
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies, but depending on your system (Linux/MacOS/Windows) and graphics card (NVIDIA/AMD), you may first need to install the desired PyTorch (CUDA, ROCm, or CPU-based) version based on [this guide](https://pytorch.org/get-started/locally/). \
Then install the requirements via:

   ```sh
   pip install -r requirements.txt
   ```

4. Create a [`.env`](.env) file in the project root with your API keys (without, scripts like [`20_experiments/50_src/main.py`](20_experiments/50_src/main.py) will not work):

   ```ini
   GOOGLE_API_KEY=your_api_key_here
   OPENAI_API_KEY=your_api_key_here
   ANTHROPIC_API_KEY=your_api_key_here
   ```

---

## Project Structure

For a detailed overview of the project structure, refer to the `README.md` files in each subdirectory:

- [`00_administration/README.md`](00_administration/README.md) – Project concept, exposé, LaTeX sources
- [`10_literature_review/README.md`](10_literature_review/README.md) – Systematic literature review, criteria, BibTeX files
- [`20_experiments/README.md`](20_experiments/README.md) – Experimental scripts, source texts, prompt templates, and sample outputs
- [`30_documentation/README.md`](30_documentation/README.md) – Detailed documentation for each script and workflow
- [`40_evaluation/README.md`](40_evaluation/README.md) – Processed results, visualizations, and tables
- [`50_thesis/README.md`](50_thesis/README.md) – LaTeX source and compiled thesis PDF
- [`60_presentations/README.md`](60_presentations/README.md) – Beamer source and compiled slides PDFs for intermediate & final defense
- [`70_prior_exp_run/README.md`](70_prior_exp_run/README.md) – Archive of prior experiment runs and notes

In the root directory, you will also find/need:

- **.env** – Environment variables for API keys (has to be created, since it is not committed to Git)
- [`requirements.txt`](requirements.txt) – Python dependencies
- [`PYTHON_LICENSES.md`](PYTHON_LICENSES.md) – Dependency license summary
- [`LICENSE`](LICENSE) – Project MIT license

---

## Running Experiments

This experiment is commonly controlled by several scripts which have to be executed sequentially. \
See [`20_experiments/README.md`](20_experiments/README.md) for detailed information, including information to the question generation, API calls, and result analysis.

---

## Analysis & Evaluation

- **Truncation Check**: Token-limit scans using [`20_experiments/50_src/check_truncation.py`](20_experiments/50_src/check_truncation.py)
- **Quantitative Analysis**: Automated metrics are calculated in [`20_experiments/50_src/analysis_quantitative.py`](20_experiments/50_src/analysis_quantitative.py). The results are stored in [`20_experiments/60_analyses/`](20_experiments/60_analyses/)
- **Qualitative Analysis**: Expert and student-ratings are also stored in [`20_experiments/60_analyses/`](20_experiments/60_analyses/)
- **Evaluation Notebooks**: Jupyter notebooks for evaluations:
  - [`evaluation1_quan.ipynb`](20_experiments/50_src/evaluation1_quan.ipynb) - Quantitative analysis of Experiment 1
  - [`evaluation1_qual.ipynb`](20_experiments/50_src/evaluation1_qual.ipynb) - Qualitative analysis of Experiment 1. This notebook has to be run twice, once with `USE_SUPERVISOR_DATA = True` and once with `USE_SUPERVISOR_DATA = False`.
  - [`evaluation2_qual.ipynb`](20_experiments/50_src/evaluation2_qual.ipynb) - Qualitative analysis of Experiment 2
- **Evaluation Results**: Tables & plots based on the notebooks are saved in [`40_evaluation/`](40_evaluation/).

---

## Documentation

All script-level documentation for the Python files in [`20_experiments/50_src/`](20_experiments/50_src/) is in [`30_documentation/`](30_documentation/), including:

- API configuration: [`api_config.md`](30_documentation/api_config.md)
- API calls abstraction: [`api_calls.md`](30_documentation/api_calls.md)
- Constants: [`constants.md`](30_documentation/constants.md)
- File utilities: [`file_utils.md`](30_documentation/file_utils.md)
- Main execution: [`main.md`](30_documentation/main.md)
- Prompt utilities: [`prompt_utils.md`](30_documentation/prompt_utils.md)
- Quantitative Analysis: [`analysis_quantitative.md`](30_documentation/analysis_quantitative.md)
- Question generation pipeline: [`question_generation.md`](30_documentation/question_generation.md)
- Sampling: [`sampling.md`](30_documentation/sampling.md)
- Truncation check: [`check_truncation.md`](30_documentation/check_truncation.md)
- Used in archived experimental run: [`analysis_qualitative.md`](30_documentation/analysis_qualitative.md)

---

## Thesis & Compilation

Full LaTeX thesis is under [`50_thesis/`](50_thesis/), including its PDF. From the root directory, to compile if needed, run:

```sh
cd 50_thesis/00_titlepage
latexmk -pdf titlepage.tex
```  

Then, compile the main thesis document:

```sh
cd ../10_thesis/20_content
latexmk -pdf thesis.tex
```

Refer to [`50_thesis/README.md`](50_thesis/README.md) for details.

---

## Presentations

Beamer slides for (intermediate) defense are in [`60_presentations/`](60_presentations/), including the PDF file for each presentation. From the root directory, build if needed with:

```sh
cd 60_presentations/10_intermediate_defense
latexmk -pdf pres.tex
```  

And for the final defense afterwards:

```sh
cd ../20_defense
latexmk -pdf pres.tex
```

---

## Prior Experimental Run

The prior experimental run was archived in the [`70_prior_exp_run/`](70_prior_exp_run/) directory, providing information on the experimental setup, data used, and results obtained.

---

## License Information

This project is released under the MIT License. A copy of the license is available in the [`LICENSE`](LICENSE) file in the root directory of this repository.

This project utilizes diverse Python libraries. A comprehensive list of these dependencies and their respective licenses is provided in the [`PYTHON_LICENSES.md`](PYTHON_LICENSES.md) file.

The used embedding model `"T-Systems-onsite/cross-en-de-roberta-sentence-transformer"` (Copyright (c) 2020 Philip May, T-Systems on site services GmbH) for the semantic similarity calculation used in this research is also distributed under the MIT License. For detailed information regarding its license terms, please refer to the official license file, which can be found [on the Hugging Face model hub](https://huggingface.co/T-Systems-onsite/cross-en-de-roberta-sentence-transformer/blob/main/LICENSE).
