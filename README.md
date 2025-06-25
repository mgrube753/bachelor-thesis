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

-   [ ] Refine:
      - Related Work
      - Implementation
-   [ ] Create eval.py for pandas/matplotlib evaluation based on the csv files created by the analysis*.py scripts & expert eval
   - At first, quantitative analysis will be useful + maybe IAA till monday
---
-   [ ] (Refine qualitative analysis if needed (first we pass it since we have experts for exp1))

## License

The source code of this project is released under the MIT License. A copy of the license is available in the `LICENSE` file in the root directory of this repository.

This project utilizes diverse Python libraries. A comprehensive list of these dependencies and their respective licenses is provided in the `PYTHON_LICENSES.md` file.

The T-Systems RoBERTa model for the semantic similarity setup used in this research is also distributed under the MIT License. For detailed information regarding its license terms, please refer to the official license file, which can be found [on the Hugging Face model hub](https://huggingface.co/T-Systems-onsite/cross-en-de-roberta-sentence-transformer/blob/main/LICENSE).