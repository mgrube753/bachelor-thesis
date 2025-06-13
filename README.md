# Readme, but firstly primarily for todos

## Notes

.env is used:

```
GOOGLE_API_KEY=your_api_key_here
OPENAI_API_KEY=your_api_key_here
ANTHROPIC_API_KEY=your_api_key_here
```

Where to get the keys:
-   [Google API Key](https://aistudio.google.com/app/apikey)
-   [OpenAI API Key](https://platform.openai.com/api-keys)
-   [Anthropic API Key](https://console.anthropic.com/settings/keys)

## Todo

-   [x] Create analysis setup for expert evaluation, so these can rate the sampled questions based on the same rubrics as the llm-based eval has, blind test
   -   Experiment 1 is Prof vs. Gemini
   -   Experiment 2 is Claude vs. OpenAI
-   [ ] While generating questions for the experiments, the CSV files shall be created with the needed initial columns...
-   [ ] Optimize inter-annotator agreement calculation for the sampled questions between llms and expert
-   [ ] Create eval.py for pandas/matplotlib evaluation based on the csv files created by the analysis*.py scripts & expert eval
