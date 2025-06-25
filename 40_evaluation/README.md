# Evaluation

This directory is designated for evaluation results, illustrated as Tables and Plots, derived from the experimental data.

## Purpose

It is structured to facilitate the analysis and presentation of results from the experiments conducted in the [`20_experiments/`](../20_experiments/) directory, as depicted in the following structure:

- **Analysis Results** - Processed insights from qualitative expert ratings and quantitative analyses via [`20_experiments/50_src/analysis_quantitative.py`](../20_experiments/50_src/analysis_quantitative.py) were used, which are stored in [`20_experiments/60_analyses/`](../20_experiments/60_analyses/)
results from CSV files located in [`20_experiments/60_analyses/`](../20_experiments/60_analyses/)
- **Tables and Figures** - Based on the CSV files, statistical summaries and visualizations of experimental results are served here

## Integration with Experimental Framework

The evaluation results will be generated through:

1. **Agreement Calculation** - Via [`20_experiments/50_src/agreement.py`](../20_experiments/50_src/agreement.py)
2. **Automated Processing** - Via [`20_experiments/50_src/evaluation.ipynb`](../20_experiments/50_src/evaluation.ipynb)