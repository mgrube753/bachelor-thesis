# Thesis

Here, the complete LaTeX source code for the bachelor thesis: "Generating Educational Questions using Large Language Models: An Evaluation of Quality and Alignment with Pedagogical Principles".

## Structure

### Thesis Document
- **[`thesis/`](thesis/)** - Primary thesis content and compilation environment
  - [`content/thesis.tex`](thesis/content/thesis.tex) - Main LaTeX document
  - [`content/thesis.pdf`](thesis/content/thesis.pdf) - Compiled thesis document
  - [`content/secs/`](thesis/content/secs/) - Individual thesis sections
  - [`bibs/`](thesis/bibs/) - Bibliography files (.bib format)
  - [`extra/`](thesis/extra/) - LaTeX configuration and additional materials

### Title Page Generation
- **[`titlepage/`](titlepage/)** - Separate title page compilation
  - [`titlepage.tex`](titlepage/titlepage.tex) - Title page source
  - [`titlepage.pdf`](titlepage/titlepage.pdf) - Compiled title page

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
- **[`bibs/Positive.bib`](thesis/bibs/Positive.bib)** - Primary research papers
- **[`bibs/Extras.bib`](thesis/bibs/Extras.bib)** - Supporting literature cited in the positive papers
- **[`bibs/Eigenes.bib`](thesis/bibs/Eigenes.bib)** - Self-discovered resources and recent developments

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

1. **Compile Title Page**: Navigate to [`titlepage/`](titlepage/) and compile `titlepage.tex`
2. **Compile Main Document**: Navigate to [`thesis/content/`](thesis/content/) and compile `thesis.tex`

To properly compile the thesis, make sure to use e.g. `latexmk` or a similar tool that handles multiple passes for references and citations.