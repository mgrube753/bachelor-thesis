# Experiments

This directory contains the experimental framework for evaluating Large Language Model capabilities in educational question generation, focusing on the two assessments of content adherence and Bloom's Taxonomy alignment.

## Structure Overview

### Question Paths

- **[`10_exp1/`](10_exp1/)** - Content Adherence & Error Detection
  - [`run_a_content/`](10_exp1/run_a_content/) - Questions from original source materials
  - [`run_b_error/`](10_exp1/run_b_error/) - Questions from manipulated source materials
- **[`20_exp2/`](20_exp2/)** - Question Types & Bloom's Taxonomy
  - [`run_a_type/`](20_exp2/run_a_type/) - Format-specific question generation
  - [`run_b_bloom/`](20_exp2/run_b_bloom/) - Cognitive level-targeted questions
  - [`run_c_both/`](20_exp2/run_c_both/) - Combined format and taxonomy specification

### Supporting Infrastructure

- **[`30_input_sources/`](30_input_sources/)** - Source materials (script, transcript, Tanenbaum excerpts)
- **[`40_prompts/`](40_prompts/)** - Prompt templates for generation and evaluation
- **[`50_src/`](50_src/)** - Python implementation and evaluation notebooks
- **[`60_analyses/`](60_analyses/)** - Obtained analyses data used for evaluation purposes
- **[`70_samples/`](70_samples/)** - Representative question samples
- **[`80_samples_renamed/`](80_samples_renamed/)** - Processed question collections used for manual review

## Experimental Design

### Models Used

- **Anthropic Claude 3.7 Sonnet**
- **Google Gemini 2.5 Flash**
- **OpenAI o3**
- **DeepSeek R1**

### Source Materials (converted to TXT)

- **Script**: Lecture content from the primary supervisor: "Referenzarchitekturen"
- **Transcript**: Audio-to-text conversion of lecture content
- **Tanenbaum**: Excerpts from "Computer Networks" textbook by Andrew S. Tanenbaum
- **Manipulated Script**: Intentionally altered lecture content for error detection testing

## Implementation Framework

### Prompt Engineering

- **[`40_prompts/experiment/`](40_prompts/experiment/)** - Generation templates
  - [`exp1_common_prompt.md`](40_prompts/experiment/exp1_common_prompt.md) - Basic question generation
  - [`exp1_complex_prompt.md`](40_prompts/experiment/exp1_complex_prompt.md) - Advanced cognitive prompting
  - [`exp2_type.md`](40_prompts/experiment/exp2_type.md) - Format-specific generation
  - [`exp2_bloom.md`](40_prompts/experiment/exp2_bloom.md) - Taxonomy-aligned generation
  - [`exp2_both.md`](40_prompts/experiment/exp2_both.md) - Combined specification

### Evaluation Prompts

- **[`40_prompts/evaluation/`](40_prompts/evaluation/)** - Assessment rubrics
  - [`exp_eval.md`](40_prompts/evaluation/exp_eval.md) - Expert evaluation template
  - [`exp1a_rubric.md`](40_prompts/evaluation/exp1a_rubric.md) - Content adherence criteria
  - [`exp1b_rubric.md`](40_prompts/evaluation/exp1b_rubric.md) - Error detection criteria
  - [`exp2_rubric.md`](40_prompts/evaluation/exp2_rubric.md) - Format-taxonomy assessment

### Fundamental Scripts

- **[`50_src/check_truncation.py`](50_src/check_truncation.py)** - Token length validation for TXT files
  - Verifies source materials and generated questions fit within model limits for semantic similarity check
  - Uses the model's tokenizer to ensure that the content does not exceed the maximum token length before analyzing
  - Generates report in [`note_truncation.md`](50_src/note_truncation.md)

- **[`50_src/main.py`](50_src/main.py)** - Main execution script
  - Initializes LLM clients (OpenAI, Anthropic, Google, DeepSeek)
  - Executes all question generation experiments (exp1a, exp1b, exp2a, exp2b, exp2c)
  - Coordinates the entire experimental workflow using several utility scripts
    - **[`50_src/api_calls.py`](50_src/api_calls.py)** - LLM API interactions
    - **[`50_src/prompt_utils.py`](50_src/prompt_utils.py)** - Prompt parsing and generation
    - **[`50_src/question_generation.py`](50_src/question_generation.py)** - Question generation logic

- **[`50_src/analysis_quantitative.py`](50_src/analysis_quantitative.py)** - Experiment 1 quantitative analysis
  - Calculates cosine similarity between questions and source materials
  - Generates adherence scores between questions and source materials using o3 model and Claude 3.7 Sonnet
  - Processes experiments exp1a, exp1b, and exp1a_no_source

- **[`50_src/sampling.py`](50_src/sampling.py)** - Sample selection for manual review
  - Randomly samples questions for expert evaluation
  - Generates structured CSV templates for qualitative assessment
  - Creates renamed sample collections for blind evaluation

## Bloom's Taxonomy Integration

The second experiment utilizes Bloom's Taxonomy, described and used via [`40_prompts/experiment/bloom.md`](40_prompts/experiment/bloom.md):

1. **Remembering**
2. **Understanding**
3. **Applying**
4. **Analyzing**
5. **Evaluating**
6. **Creating**

### Description & Verb Integration

Each level includes specific German descriptions and action verbs for each Bloom level to construct the prompts, properly parsed via [`50_src/prompt_utils.py`](50_src/prompt_utils.py) for systematic question generation targeting specific cognitive demands + question type constraints.

## Usage Instructions

### Basic Execution

All data were generated using the scripts in this directory. \
To run the Python files and the notebooks, go to the [`50_src/`](50_src/) directory and execute the following commands:

```bash
python check_truncation.py        # Optional: Perform first truncation check for source materials
python main.py                    # Generate questions
python check_truncation.py        # Re-check after generating questions to check for truncation
python analysis_quantitative.py   # Quantitative analysis for experiment 1
python sampling.py                # Sample questions for manual review (experts in exp1, students in exp2)
```

This workflow will not work if the `.env` file is not set up with the necessary API keys for the LLMs. \
The `.env` file should contain the keys for OpenAI, Anthropic, and Google, to ensure the scripts can access the LLMs for question generation and analysis.

The script [`50_src/analysis_qualitative.py`](50_src/analysis_qualitative.py), which would have been LLM-based (using all questions instead of sampled ones), was not used as the qualitative analysis was performed manually by experts instead (using sample sets). This approach was used in the archived experimental run in [`../70_prior_exp_run/`](../70_prior_exp_run/) for both thesis experiments.

**Particularly useful for viewers**: Whether all ratings are available, run the Jupyter notebooks:

- [`50_src/evaluation1_quan.ipynb`](50_src/evaluation1_quan.ipynb) - Quantitative analysis of Experiment 1
- [`50_src/evaluation1_qual.ipynb`](50_src/evaluation1_qual.ipynb) - Qualitative analysis of Experiment 1
- [`50_src/evaluation2_qual.ipynb`](50_src/evaluation2_qual.ipynb) - Qualitative analysis of Experiment 2

Then, the notebooks' insights are available in [`../40_evaluation/`](../40_evaluation/).

### Notebook Conversion for Documentation

To include the notebooks in the thesis PDF, the following command was used (at [`50_src/`](50_src/)) to convert them to Python scripts:

```bash
jupyter nbconvert --output-dir='nb_to_py' --to script evaluation*.ipynb
```

These generated Python scripts in [`50_src/nb_to_py/`](50_src/nb_to_py/) are then included in the thesis PDF after compilation.

### Configuration Requirements

- **API Keys**: OpenAI, Anthropic, Google configured via environment variables
- **Dependencies**: Listed in root [`requirements.txt`](../requirements.txt)
- **DeepSeek**: Manual prompting via [web interface](https://chat.deepseek.com) (R1 model access)
