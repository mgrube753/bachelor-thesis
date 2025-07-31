# Thesis

This directory contains the complete LaTeX source and compiled documents for the bachelor thesis:  
**"Generating Educational Questions using Large Language Models: An Evaluation of Quality and Alignment with Pedagogical Principles"**

## Directory Structure

- **[`00_titlepage/`](00_titlepage/)**  
  Separate compilation for the official title page, including images and auxiliary files.

- **[`10_thesis/`](10_thesis/)**  
  Main thesis content, organized as follows:
  - **[`00_bibs/`](10_thesis/00_bibs/)**  
    - `Positive.bib` – Primary research papers  
    - `Extras.bib` – Supporting literature cited in the positive papers 
    - `Eigenes.bib` – Independently discovered resources
  - **[`10_extra/`](10_thesis/10_extra/)**  
    - LaTeX configuration, abbreviations, figures, and tables
  - **[`20_content/`](10_thesis/20_content/)**  
    - `thesis.tex` – Main LaTeX source  
    - `thesis.pdf` – Compiled thesis  
    - `secs/` – Individual chapter and section files

## Thesis Structure

The thesis follows a comprehensive academic structure addressing LLM-based educational question generation:

### Core Sections

1. **[Introduction](thesis/content/secs/1-introduction.tex)** - Research motivation, objectives, and thesis outline
2. **[Theoretical Foundations](thesis/content/secs/2-background.tex)** - LLMs, Bloom's Taxonomy, and evaluation methodologies
3. **[Related Work](thesis/content/secs/3-related-work.tex)** - Literature review and research gap identification
4. **[Experiment Design](thesis/content/secs/4-experiment-design.tex)** - Methodology and experimental setup
5. **[Implementation](thesis/content/secs/5-the-approach.tex)** - Technical approach and implementation details
6. **[Evaluation](thesis/content/secs/6-evaluation.tex)** - Results analysis and hypothesis testing
7. **[Conclusion](thesis/content/secs/7-conclusion.tex)** - Findings summary and future work

## Research Focus

The following research questions guide the thesis:

**RQ1**: *To what extent do LLMs adhere to the content of diverse provided instructional texts when generating questions?*

**RQ2**: *How does the relationship between diverse question formats and Bloom’s Taxonomy levels influence the pedagogical effectiveness of Large Language Model (LLM)-generated questions?*

## Bibliography Organization

### Literature Sources

- **[`00_bibs/Positive.bib`](10_thesis/00_bibs/Positive.bib)** - Primary research papers
- **[`00_bibs/Extras.bib`](10_thesis/00_bibs/Extras.bib)** - Supporting literature cited in the positive papers
- **[`00_bibs/Eigenes.bib`](10_thesis/00_bibs/Eigenes.bib)** - Self-discovered resources and recent developments

### Key Research Areas

- Large Language Model architectures and capabilities
- Automated question generation systems and methodologies
- Bloom's Taxonomy integration in educational technology

## Technical Implementation

The thesis incorporates comprehensive technical documentation:

### Source Code Integration

- **API Configuration**: Multi-provider LLM integration (OpenAI, Anthropic, Google, DeepSeek)
- **Prompt Engineering**: Systematic template-based prompts
- **Data Processing**: Automated experimental pipeline and result synthesis
- **Evaluation Framework**: Assessment combining automated metrics and expert evaluation

### Appendices Structure

- **Source Code Listings** - Core experimental implementation
- **Prompt Templates** - Complete experimental and evaluation prompts
- **Source Materials** - ISO-OSI layer content in multiple formats
- **Evaluation Rubrics** - Structured assessment criteria and scoring guidelines

## Compilation Instructions

To compile the thesis, follow these steps:

1. **Compile Title Page**: Navigate to [`00_titlepage/`](00_titlepage/) and compile `titlepage.tex`
2. **Compile Main Document**: Navigate to [`10_thesis/20_content/`](10_thesis/20_content/) and compile `thesis.tex`

Use `latexmk` or a similar tool to ensure proper handling of references and citations.