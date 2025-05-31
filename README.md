# Readme, but primarily for todos

## Notes

.env is used:

```
GOOGLE_API_KEY=your_api_key_here
OPENAI_API_KEY=your_api_key_here
ANTHROPIC_API_KEY=your_api_key_here
```

## Todo

-   [x] Inter-annotator agreement, check how to do it
-   [x] Add Bloom descriptions and verbs to exp2_rubric.md
-   [ ] Set up iaa calculation for the directory structure
-   [ ] Create analysis_quantitative.py script for cosine similarity and LLM-based content adherence ratings
-   [ ] Create analysis_qualitative.py script for LLM-based evaluation based on a rubric
-   [ ] Create eval.py for pandas/matplotlib evaluation based on the csv files created by the analysis.py script / expert eval
   -   Add division into exp1 and exp2, because exp2 will not have all data then
