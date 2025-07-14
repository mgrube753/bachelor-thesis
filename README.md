# Readme, but firstly primarily for todos

## Notes

.env is used:

```sh
GOOGLE_API_KEY=your_api_key_here
OPENAI_API_KEY=your_api_key_here
ANTHROPIC_API_KEY=your_api_key_here
```

Where to get the keys:

-   [Google API Key](https://aistudio.google.com/app/apikey)
-   [OpenAI API Key](https://platform.openai.com/api-keys)
-   [Anthropic API Key](https://console.anthropic.com/settings/keys)

## Todo

-   [ ] Refine evaluation setups via notebooks since the dir structure changed
-   [ ] Continue refining Eval chapter
-   [ ] Preparation for Exp 2:
    - [x] Refine experimental setup in workspace (better path structure!)
    - [x] Proper prompts more based on both prompts
    - [x] Create instruction manual for the experts for Exp 2
-   [ ] Use the expert reviews to get insights for exp 1a and 1b

---

## License

The source code of this project is released under the MIT License. A copy of the license is available in the `LICENSE` file in the root directory of this repository.

This project utilizes diverse Python libraries. A comprehensive list of these dependencies and their respective licenses is provided in the `PYTHON_LICENSES.md` file.

The embedding model "T-Systems-onsite/cross-en-de-roberta-sentence-transformer" for the semantic similarity calculation used in this research is also distributed under the MIT License. For detailed information regarding its license terms, please refer to the official license file, which can be found [on the Hugging Face model hub](https://huggingface.co/T-Systems-onsite/cross-en-de-roberta-sentence-transformer/blob/main/LICENSE).
