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
- **[`50_src/`](50_src/)** - Python implementation and analysis scripts
- **[`60_analyses/`](60_analyses/)** - Obtained analyses data for evaluation purposes
- **[`70_samples/`](70_samples/)** - Representative question samples
- **[`80_questions_renamed/`](80_questions_renamed/)** - Processed question collections

## Experimental Design

### Models Used
- **Anthropic Claude 3.7 Sonnet**
- **Google Gemini 2.5 Flash**
- **OpenAI o3**
- **DeepSeek R1**

### Source Materials
- **Script**: Lecture content from "Referenzarchitekturen" (Prof. Cap)
- **Transcript**: Audio-to-text conversion of lecture content
- **Tanenbaum**: Excerpts from "Computer Networks" textbook
- **Manipulated Script**: Intentionally altered lecture content for error detection testing

## Implementation Framework

### Prompt Engineering
- **[`40_prompts/experiment/`](40_prompts/experiment/)** - Generation templates
  - [`exp1_common_prompt.md`](40_prompts/experiment/exp1_common_prompt.md) - Basic question generation
  - [`exp1_complex_prompt.md`](40_prompts/experiment/exp1_complex_prompt.md) - Advanced cognitive prompting
  - [`exp2_type.md`](40_prompts/experiment/exp2_type.md) - Format-specific generation
  - [`exp2_bloom.md`](40_prompts/experiment/exp2_bloom.md) - Taxonomy-aligned generation
  - [`exp2_both.md`](40_prompts/experiment/exp2_both.md) - Combined specification

### Evaluation System
- **[`40_prompts/evaluation/`](40_prompts/evaluation/)** - Assessment rubrics
  - [`exp_eval.md`](40_prompts/evaluation/exp_eval.md) - Expert evaluation template
  - [`exp1a_rubric.md`](40_prompts/evaluation/exp1a_rubric.md) - Content adherence criteria
  - [`exp1b_rubric.md`](40_prompts/evaluation/exp1b_rubric.md) - Error detection criteria
  - [`exp2_rubric.md`](40_prompts/evaluation/exp2_rubric.md) - Format-taxonomy assessment

### Automation Pipeline
- **[`50_src/main.py`](50_src/main.py)** - Primary experiment orchestration
- **[`50_src/question_generation.py`](50_src/question_generation.py)** - LLM question generation
- **[`50_src/evaluation.py`](50_src/evaluation.py)** - Automated assessment execution
- **[`50_src/analysis_quantitative.py`](50_src/analysis_quantitative.py)** - Statistical analysis
- **[`50_src/analysis_qualitative.py`](50_src/analysis_qualitative.py)** - Expert evaluation processing
- **[`50_src/agreement.py`](50_src/agreement.py)** - Inter-annotator reliability calculation

## Bloom's Taxonomy Integration

The experiments utilize a comprehensive German-language Bloom's framework:

### Cognitive Levels ([`40_prompts/experiment/bloom.md`](40_prompts/experiment/bloom.md))
1. **Remembering**
2. **Understanding**
3. **Applying**
4. **Analyzing**
5. **Evaluating**
6. **Creating**

### Description & Verb Integration
Each level includes specific German descriptions and action verbs for each Bloom level to construct the prompts, parsed via [`50_src/prompt_utils.py`](50_src/prompt_utils.py) for systematic question generation targeting specific cognitive demands.

## Usage Instructions

### Basic Execution
```bash
# (Optional: perform first truncation check for source materials)
python check_truncation.py

# Generate questions and evaluations
python main.py

# Perform second truncation check which covers both -- source materials and questions
python check_truncation.py

# Run quantitative analysis
python analysis_quantitative.py

# Process qualitative assessments
python analysis_qualitative.py

# After inserting all results in the csv files, calculate agreement metrics
python agreement.py

# Perform evaluation step for tables and figures
python evaluation.py
```

### Configuration Requirements
- **API Keys**: OpenAI, Anthropic, Google configured via environment variables
- **Dependencies**: Listed in root [`requirements.txt`](../requirements.txt)
 **DeepSeek**: Manual prompting via web interface (R1 model access)

 #TODO more details needed

 #TODO think about 30_documentation as well so this readme and the documentation do not overlap much