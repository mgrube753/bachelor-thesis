# Experiment 1 Inter-Rater Agreement Analysis

**Generated:** 2025-06-25 10:28:22  
**Method:** Fleiss' Kappa with simulated expert ratings  
**Experts:** 5 experts per experiment  
**Rating Scale:** 1-10 (integer values)  

## Overview

This analysis calculates inter-rater agreement for Experiment 1 using Fleiss' kappa coefficient with simulated expert ratings.

## Detailed Results

| Experiment | Category | Kappa | Level | Mean Rating | Std Dev |
|------------|----------|-------|-------|-------------|---------|
| exp1a | relevance | 0.440 | Moderate | 7.3 | 1.2 |
| exp1a | clarity | 0.499 | Moderate | 7.1 | 1.2 |
| exp1a | answerability | 0.474 | Moderate | 7.5 | 1.3 |
| exp1a | challenging | 0.555 | Moderate | 7.2 | 1.6 |
| exp1a | correctness | 0.515 | Moderate | 7.8 | 1.2 |
| exp1b | relevance | 0.272 | Fair | 7.3 | 1.3 |
| exp1b | clarity | 0.579 | Moderate | 6.6 | 1.7 |
| exp1b | answerability | 0.432 | Moderate | 6.9 | 1.5 |
| exp1b | challenging | 0.498 | Moderate | 6.5 | 1.7 |
| exp1b | manipulation_handling | 0.619 | Substantial | 6.0 | 2.5 |

## Summary by Category

| Category | Mean Kappa | Std Dev |
|----------|------------|----------|
| answerability | 0.453 | 0.030 |
| challenging | 0.527 | 0.041 |
| clarity | 0.539 | 0.056 |
| correctness | 0.515 | nan |
| manipulation_handling | 0.619 | nan |
| relevance | 0.356 | 0.119 |

## Summary by Experiment

| Experiment | Mean Kappa | Std Dev |
|------------|------------|----------|
| exp1a | 0.497 | 0.043 |
| exp1b | 0.480 | 0.137 |

## Kappa Interpretation Guide

| Range | Interpretation |
|-------|---------------|
| < 0.20 | Slight agreement |
| 0.20-0.40 | Fair agreement |
| 0.41-0.60 | Moderate agreement |
| 0.61-0.80 | Substantial agreement |
| 0.81-1.00 | Almost perfect agreement |

## Methodology

- **Simulation Parameters:** Each category has different base rating distributions
- **Expert Variation:** Individual expert bias and random noise added
- **Fleiss' Kappa:** Calculated using statsmodels implementation
- **Rating Scale:** Integer values 1-10, converted to frequency tables for kappa calculation

## Category Parameters Used

| Category | Mean | Std Dev |
|----------|------|---------|
| Relevance | 7.5 | 1.2 |
| Clarity | 6.8 | 1.5 |
| Answerability | 7.2 | 1.3 |
| Challenging | 6.5 | 1.8 |
| Correctness | 7.8 | 1.0 |
| Manipulation Handling | 6.0 | 2.0 |
