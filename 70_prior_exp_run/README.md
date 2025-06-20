# Prior Experimental Run

This directory contains the prior experimental run of the thesis project.

## Why was a new run needed?

This experimental run of the directory was archived, since the output questions in Experiment 1 were not satisfactory. The questions' output formats differed a lot, since in the common prompt, in contrast to the complex prompt, the question format was not specified. In the expert-based evaluation -- and even in the LLM-based evaluation -- this could have led to a bias in the evaluation, since the questions were not that well comparable.

Therefore, a new run was needed to ensure that the questions were more consistent in their output format. This was achieved by refining all prompts for all experiments:

- Experiments 1a and 1b: Using the same common and complex prompts for both subexperiments
- Experiments 2a, 2b and 2c: Using a certain prompt for each subexperiment, which were based on the properties of the complex prompt of Experiment 1.