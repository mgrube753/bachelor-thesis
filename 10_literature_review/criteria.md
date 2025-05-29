# Criteria for Literature Review

## Pipeline

1. Get all papers from Google Scholar and Elicit
2. Filter Duplicates
3. Doing TACID method on
    - First Filtering (main relevance, importance for thesis' topics), by inclusion/exclusion criteria; papers left with relevance to the thesis
    - Final Filtering (deeper analysis of the papers)

## Inclusion

-   recency (from 2021 on)
-   overall dealing with LLMs / comparative analysis
-   question generation focus
    -   using bloom's taxonomy with llms
-   showing evaluation metrics for llm performance
    -   e.g. semantic similarity, cognitive alignment (bloom), content fidelity
-   if preprint (no peer-review): high relevance (>= 10 citations)
-   workshops with > 0 cites

## Exclusion

-   not english
-   payment needed (no open access)
-   on beall's list
-   small language models only / multimodal
-   proprietary (without technical details on implementation, prompting or proper evaluation)
-   other domains besides llms / question generation via llms / evaluation of llms (common/bloom) --> no relevance
-   if conference/journal (not workshop) if 0 cites (soft criteria)
-   work is very related to another paper by authors (take the most relevant)

## Example Literature Review Table

| Model         | Developer | Release Date | Model Size (params) | Architecture                    | Context Window  | Training Data                      | Key Benchmarks            | Open Source        | Notable Capabilities                                                             | Limitations                                                                      |
| ------------- | --------- | ------------ | ------------------- | ------------------------------- | --------------- | ---------------------------------- | ------------------------- | ------------------ | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| GPT-4         | OpenAI    | March 2023   | Not disclosed       | Transformer (likely sparse MoE) | 32k-128k tokens | Not fully disclosed                | MMLU: 86.4%, GSM8K: 92.0% | No                 | Multimodal capabilities, strong reasoning, code generation                       | Limited transparency regarding training, closed source, potential hallucinations |
| Claude 3 Opus | Anthropic | March 2024   | Not disclosed       | Transformer-based               | 200k tokens     | Curated web text, books, dialogue  | MMLU: 86.8%, GSM8K: 94.2% | No                 | Long context handling, reduced hallucinations, strong instruction following      | Closed source, computationally expensive, limited multilingual abilities         |
| Llama 3 (70B) | Meta      | April 2024   | 70B                 | Transformer-based               | 8k tokens       | Web text, books, code repositories | MMLU: 78.5%, GSM8K: 84.3% | Yes (with license) | Strong open-weight performance, efficient scaling, improved multilingual support | Smaller context window than competitors, less capable on certain reasoning tasks |
