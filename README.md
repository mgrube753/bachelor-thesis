# Readme, but firstly primarily for todos

## Notes

.env is used:

```
GOOGLE_API_KEY=your_api_key_here
OPENAI_API_KEY=your_api_key_here
ANTHROPIC_API_KEY=your_api_key_here
```

## Todo

-   [x] Create similar sample question set for llms and experts
-   [x] Create analysis_qualitative.py script for LLM-based evaluation of sampled questions based on rubrics
-   [ ] Find top 5 papers to show Supervisors
---
-   [ ] Create analysis setup for expert evaluation, so these can rate the sampled questions based on the same rubrics, blind test
-   [ ] Optimize inter-annotator agreement calculation for the sampled questions between llms and expert
-   [ ] Create eval.py for pandas/matplotlib evaluation based on the csv files created by the analysis*.py scripts & expert eval
