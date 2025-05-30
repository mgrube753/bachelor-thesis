# Experiments Folder

This folder shows the experimental setup and data for evaluating automated question generation systems targeting the ISO-OSI networking model.

## Structure

### Experiments
- **10_exp1/** - First experiment comparing content accuracy and error detection
  - `run_a_content/` - Questions generated from original source material
  - `run_b_error/` - Questions generated from manipulated source material
- **20_exp2/** - Second experiment evaluating question types and cognitive complexity
  - `run_a_type/` - Questions categorized by format (multiple-choice, open-ended)
  - `run_b_bloom/` - Questions targeting specific Bloom's taxonomy levels
  - `run_c_both/` - Combined type and complexity evaluation

### Source Materials
- **30_input_sources/** - Original texts about OSI layers
  - `script/` - Lecture script content (original and manipulated versions)
  - `tanenbaum/` - Excerpts from Tanenbaum textbook
  - `transcript/` - Lecture transcript material

### Configuration
- **40_prompts/** - Template prompts for question generation and evaluation
- **50_src/** - Python scripts for experiment execution and data processing
- **60_eval/** - Generated evaluation data and results

## Key Components

The experiments evaluate four LLM providers

- Anthropic Claude 3.7 Sonnet
- Google Gemini 2.5 Flash
- OpenAI o3
- DeepSeek R1

across different source materials and generation strategies, with automated scoring based on relevance, clarity, answerability, cognitive level, and correctness. DeepSeek was manually prompted via their website interface.

## Usage

1. **Run experiments**: Execute `python main.py` from the root directory to generate questions and evaluations
2. **Generate automated results**: Run `python analysis.py` to create evaluation metrics using cosine similarity and LLM-based content adherence ratings
3. **Review experimental data**: Navigate to `10_exp1/` or `20_exp2/` to examine generated questions
4. **Examine source materials**: Check `30_input_sources/` for the original texts used in question generation
5. **Analyze prompts**: View `40_prompts/` to understand the templates used for LLM interactions
6. **Process data**: Use Python scripts in `50_src/` for additional data processing and analysis
7. **Check evaluations**: Review `60_eval/` for automated scoring results and analysis

## Todo

- [ ] Add Bloom descriptions and verbs to exp2_rubric.md
- [ ] Create analysis_quantitative.py script for cosine similarity and LLM-based content adherence ratings
- [ ] Create analysis_qualitative.py script for LLM-based evaluation based on a rubric
- [ ] Expert ratings with this rubric for qualitative evaluation are also missing
- [ ] Inter-annotator agreement needed
- [ ] Create eval.py for pandas/matplotlib evaluation based on the csv files created by the analysis.py script / expert eval