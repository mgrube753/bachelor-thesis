# Generating Educational Questions using Large Language Models

## Bachelor Thesis by Malte Grube

---

## Table of Contents

1. [Overview](#overview)
2. [Setup & Installation](#setup--installation)
3. [Project Structure](#project-structure)
4. [Running Experiments](#running-experiments-todo-needs-update-for-better-manual)
5. [Analysis & Evaluation](#analysis--evaluation)
6. [Documentation](#documentation)
7. [Thesis Source & Compilation](#thesis-source--compilation)
8. [Presentations](#presentations)
9. [Prior Experimental Runs](#prior-experimental-runs)
10. [License](#license)

---

## Overview

This repository implements and evaluates an automated pipeline for generating educational questions from instructional texts using various Large Language Models (LLMs). Experiments focus on:

- **Content Adherence & Error Detection** (Exp 1)
- **Relationship between Question Formats & Bloom’s Taxonomy Alignment** (Exp 2)

Results are analyzed quantitatively and qualitatively to assess the pedagogical quality of LLM-generated questions.

---

## Setup & Installation

1. Clone the repo  
   ```sh
   git clone https://github.com/mgrube753/bachelor-thesis.git
   cd bachelor-thesis
   ```
2. Create a Python 3.x virtual environment  
   ```sh
   python -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies  
   ```sh
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the project root with your API keys:

   ```ini
   GOOGLE_API_KEY=your_api_key_here
   OPENAI_API_KEY=your_api_key_here
   ANTHROPIC_API_KEY=your_api_key_here
   ```

---

## Project Structure

- **00_administration/** – Project concept, exposé, LaTeX sources ([00_administration/README.md])
- **10_literature_review/** – Systematic literature review, criteria, BibTeX files ([10_literature_review/README.md])
- **20_experiments/** – Experimental scripts, source texts, prompt templates, and sample outputs ([20_experiments/README.md])
- **30_documentation/** – Detailed documentation for each script and workflow ([30_documentation/README.md])
- **40_evaluation/** – Processed results, visualizations, and tables ([40_evaluation/README.md])
- **50_thesis/** – LaTeX source and compiled thesis files ([50_thesis/README.md])
- **60_presentations/** – Beamer slides for intermediate & final defenses ([60_presentations/README.md])
- **70_prior_exp_run/** – Archive of prior experiment runs and notes ([70_prior_exp_run/README.md])
- **.env** – Environment variables for API keys (not committed)
- **requirements.txt** – Python dependencies
- **PYTHON_LICENSES.md** – Dependency license summary
- **LICENSE** – Project license (MIT)

---

## Running Experiments #TODO needs update for better manual

Control experiments via the main orchestration script:

```sh
python 20_experiments/50_src/main.py
```

See [20_experiments/README.md] for detailed information.

---

## Analysis & Evaluation

- **Truncation Check**: Token-limit scans using `20_experiments/50_src/check_truncation.py`
- **Quantitative Analysis**: Automated metrics are calculated in `20_experiments/50_src/analysis_quantitative.py`
- **Qualitative Analysis**: Expert and student-ratings are stored in `20_experiments/60_analyses/`
- **Evaluation Notebooks**: Jupyter notebooks for manual evaluation in `20_experiments/50_src/evaluation*.ipynb`
- **Evaluation Results**: Tables & plots in `40_evaluation/`

---

## Documentation

All script-level documentation is in `30_documentation/`, including:

- API configuration: `api_config.py` & `api_config.md`
- Prompt & question generation: `question_generation.py` & `question_generation.md`
- API calls abstraction: `api_calls.py` & `api_calls.md`
- Constants & utilities: `constants.py` & `constants.md`

---

## Thesis Source & Compilation

Full LaTeX thesis is under `50_thesis/`. To compile if needed, run:

```sh
cd 50_thesis/10_thesis
latexmk -pdf titlepage.tex thesis.tex
```  

Refer to `50_thesis/README.md` for details.

---

## Presentations

Beamer slides for (intermediate) defense are in `60_presentations/`. Build if needed with:

```sh
cd 60_presentations/10_intermediate_defense
latexmk -pdf pres.tex
```  

And for the final defense:

```sh
cd 60_presentations/20_defense
latexmk -pdf pres.tex
```

---

## Prior Experimental Runs

Archived experiments and notes in `70_prior_exp_run/`.

---

## License

This project is released under the MIT License. A copy of the license is available in the `LICENSE` file in the root directory of this repository.

This project utilizes diverse Python libraries. A comprehensive list of these dependencies and their respective licenses is provided in the `PYTHON_LICENSES.md` file.

The used embedding model `"T-Systems-onsite/cross-en-de-roberta-sentence-transformer"` (Copyright (c) 2020 Philip May, T-Systems on site services GmbH) for the semantic similarity calculation used in this research is also distributed under the MIT License. For detailed information regarding its license terms, please refer to the official license file, which can be found [on the Hugging Face model hub](https://huggingface.co/T-Systems-onsite/cross-en-de-roberta-sentence-transformer/blob/main/LICENSE).
