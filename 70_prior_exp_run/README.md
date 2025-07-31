# Prior Experimental Run

This directory contains the initial experimental run for the thesis project.

## Purpose

The results from this run were archived because the output questions in Experiment 1 lacked consistency. The common prompt did not specify a question format, leading to significant variation in outputs. This inconsistency could introduce bias in both expert and LLM-based evaluations, as questions were not directly comparable.

## Rationale for Rerun

A new experimental run was conducted to ensure uniformity in question formats. This was achieved by refining all prompts for each experiment, as visible in [`../20_experiments/40_prompts/`](../20_experiments/40_prompts/).

## Structure

The structure of this directory is minimal as follows:

- `10_exp1/`: Experiment 1 outputs (content and error runs)
- `20_exp2/`: Experiment 2 outputs (type, Bloom, and combined runs)
- `40_prompts/`: Prompt templates used in experiments
- `70_samples/`: Sample questions and data
- `80_questions_renamed/`: Renamed question sets for evaluation
- `for_eval/`: Materials prepared for evaluation

## Additional Notes

- Quantitative analysis was done by Anthropic Claude 3.7 Sonnet
- Qualitative analysis was done by Claude + OpenAI o3
- No temperature scores were changed at all
