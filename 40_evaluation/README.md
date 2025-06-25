# Evaluation

This directory is designated for evaluation results, illustrated as Tables and Plots, derived from the experimental data.

## Purpose

It is structured to facilitate the analysis and presentation of results from the experiments conducted in the [`20_experiments/`](../20_experiments/) directory, as depicted in the following structure:

- **Analysis Results** - Processed insights from the [`20_experiments/`](../20_experiments/) folder
- **Evaluation Data** - Synthesized results from CSV files located in [`20_experiments/60_analyses/`](../20_experiments/60_analyses/)
- **Tables and Figures** - Statistical summaries and visualizations of experimental results served here

## Integration with Experimental Framework

The evaluation results will be generated through:

1. **Automated Processing** - Via [`20_experiments/50_src/eval.py`](../20_experiments/50_src/evaluation.py)
2. **Statistical Analysis** - Using [`20_experiments/50_src/analysis_quantitative.py`](../20_experiments/50_src/analysis_quantitative.py)
3. **Qualitative Assessment** - Through [`20_experiments/50_src/analysis_qualitative.py`](../20_experiments/50_src/analysis_qualitative.py)
4. **Agreement Calculation** - Via [`20_experiments/50_src/agreement.py`](../20_experiments/50_src/agreement.py)