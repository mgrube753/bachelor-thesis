# Evaluation Results

This directory contains all results and visualizations derived from the experiments in [`20_experiments/`](../20_experiments/).

## Overview

- **Quantitative & Qualitative Analysis**: CSV files (Expert ratings and processed automated metrics) in [`20_experiments/60_analyses/`](../20_experiments/60_analyses/) are used as input for evaluation.
- **Tables & Figures**: Statistical summaries and plots are generated from these CSV files and presented here for reporting.

Note: It is best to view the notebooks to understand the context and methodology behind the files.

- [`../20_experiments/50_src/evaluation1_quan.ipynb`](../20_experiments/50_src/evaluation1_quan.ipynb): Quantitative analysis of experiment 1.
- [`../20_experiments/50_src/evaluation1_qual.ipynb`](../20_experiments/50_src/evaluation2_qual.ipynb): Qualitative analysis of experiment 1.
- [`../20_experiments/50_src/evaluation2_qual.ipynb`](../20_experiments/50_src/evaluation2_qual.ipynb): Qualitative analysis of experiment 2.

## Workflow Integration

Results are produced and updated via:

1. **Agreement Calculation**: [`agreement.py`](../20_experiments/50_src/agreement.py)
2. **Analysis & Visualization**: [`evaluation.ipynb`](../20_experiments/50_src/evaluation.ipynb)

## Directory Structure

- [`exp1/qualitative/`](./exp1/qualitative/): Qualitative results for experiment 1 (expert ratings, rubrics, summaries)
  - [`plots/`](./exp1/qualitative/plots/): Visualizations
  - [`tables/`](./exp1/qualitative/tables/): Tabular summaries
- [`exp1/quantitative/`](./exp1/quantitative/): Quantitative results for experiment 1 (metrics, CSVs, plots)
  - [`plots/`](./exp1/quantitative/plots/): Visualizations
  - [`tables/`](./exp1/quantitative/tables/): Tabular summaries
- [`exp2/qualitative/`](./exp2/qualitative/): Qualitative results for experiment 2
  - [`plots/`](./exp2/qualitative/plots/): Visualizations
  - [`tables/`](./exp2/qualitative/tables/): Tabular summaries

All outputs in this directory support the final reporting and