#!/usr/bin/env python
# coding: utf-8

# # Notebook: Qualitative Evaluation -- Experiment 1

# In[ ]:


import pandas as pd
import os
from IPython.display import display
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

plt.style.use('default')
sns.set_palette("Set2")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 100)

pd.set_option('display.notebook_repr_html', True)

def create_seaborn_boxplot(data, x, y, ax, title, ylabel, xlabel, custom_means=None):
    colors = ['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3', '#a6d854', '#ffd92f', '#e5c494', '#b3b3b3']
    unique_vals = sorted(data[x].unique())
    palette = colors[:len(unique_vals)]
    
    sns.boxplot(data=data, x=x, y=y, ax=ax, palette=palette,
                medianprops={'color': 'black', 'linewidth': 2.5, 'linestyle': ':'})
    
    plot_labels = [tick.get_text() for tick in ax.get_xticklabels()]
    
    if custom_means is not None:
        # Use custom means if provided, mapping them to the correct plot positions
        for i, plot_label in enumerate(plot_labels):
            reverse_mapping = {
                'Anthropic': 'anthropic',
                'OpenAI': 'openai', 
                'Google': 'google',
                'DeepSeek': 'deepseek',
                'Common': 'common',
                'Complex': 'complex',
                'Script': 'script',
                'Transcript': 'transcript', 
                'Tanenbaum': 'tanenbaum',
                'Script (Manipulated)': 'script_manipulated',
                'No Source': 'no_source',
                'Exp 1a': '1a',
                'Exp 1b': '1b'
            }
            original_category = reverse_mapping.get(plot_label, plot_label.lower())
            
            if original_category in custom_means.index:
                mean_val = custom_means[original_category]
                ax.scatter(i, mean_val, color='red', marker='D', s=50, zorder=3, 
                          edgecolor='darkred', linewidth=1)
    else:
        # Use original behavior if no custom means provided
        for i, val in enumerate(unique_vals):
            mean_val = data[data[x] == val][y].mean()
            ax.scatter(i, mean_val, color='red', marker='D', s=50, zorder=3, 
                      edgecolor='darkred', linewidth=1)
    
    label_mapping = {
        'anthropic': 'Anthropic',
        'openai': 'OpenAI', 
        'google': 'Google',
        'deepseek': 'DeepSeek',
        'common': 'Common',
        'complex': 'Complex',
        'script': 'Script',
        'transcript': 'Transcript', 
        'tanenbaum': 'Tanenbaum',
        'script_manipulated': 'Script (Manipulated)',
        'no_source': 'No Source',
        '1a': 'Exp 1a',
        '1b': 'Exp 1b'
    }
    
    current_labels = [tick.get_text() for tick in ax.get_xticklabels()]
    new_labels = [label_mapping.get(label, label) for label in current_labels]
    ax.set_xticklabels(new_labels, rotation=0)
    
    if 'cosine_similarity' in y.lower():
        ylabel = 'Cosine Similarity'
        if '(-1 to 1)' not in title:
            title = title.replace('Cosine Similarity', 'Cosine Similarity (-1 to 1)')
    elif 'adherence_score' in y.lower():
        ylabel = 'Adherence Score'
        if '(0 to 1)' not in title:
            title = title.replace('Adherence Score', 'Adherence Score (0 to 1)')
    
    if x.lower() == 'llm':
        xlabel = 'LLM'
    elif x.lower() == 'prompt_type':
        xlabel = 'Prompt Type'
    elif x.lower() == 'input_source':
        xlabel = 'Input Source'
    elif x.lower() == 'comparison_source':
        xlabel = 'Comparison Source'
    elif x.lower() == 'layer':
        xlabel = 'Layer'
    elif x.lower() == 'experiment':
        xlabel = 'Experiment'
    
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.set_ylabel(ylabel, fontsize=11, labelpad=15)
    ax.set_xlabel(xlabel, fontsize=11, labelpad=10)
    ax.grid(True, alpha=0.3)

BASE_PROJECT_PATH = os.path.abspath(os.path.join(os.getcwd(), "..", ".."))
INPUT_PATH = os.path.join(BASE_PROJECT_PATH, "20_experiments/60_analyses/csv_files/quantitative")
OUTPUT_PATH = os.path.join(BASE_PROJECT_PATH, "40_evaluation/exp1/quantitative/")

exp1a_path = os.path.join(INPUT_PATH, "exp1a.csv")
exp1b_path = os.path.join(INPUT_PATH, "exp1b.csv")
exp1a_no_source_path = os.path.join(INPUT_PATH, "exp1a_no_source.csv")

output_dir_exp1a = os.path.join(OUTPUT_PATH, "tables/exp1a")
output_dir_exp1b = os.path.join(OUTPUT_PATH, "tables/exp1b")
output_plot_dir_exp1a = os.path.join(OUTPUT_PATH, "plots/exp1a")
output_plot_dir_exp1b = os.path.join(OUTPUT_PATH, "plots/exp1b")

tables = {}
plots = {}

for path in [output_dir_exp1a, output_dir_exp1b, output_plot_dir_exp1a, output_plot_dir_exp1b]:
    os.makedirs(path, exist_ok=True)

if not os.path.exists(exp1a_path) or not os.path.exists(exp1b_path):
    print("Error: Quantitative data files not found.")
    print(f"Looked for {exp1a_path} and {exp1b_path}")
else:
    exp1a_df = pd.read_csv(exp1a_path)
    exp1b_df = pd.read_csv(exp1b_path)
    
    # Load exp1a_no_source if available
    exp1a_no_source_df = None
    if os.path.exists(exp1a_no_source_path):
        exp1a_no_source_df = pd.read_csv(exp1a_no_source_path)
        if 'comparison_source' in exp1a_no_source_df.columns:
            exp1a_no_source_df["adherence_score"] = exp1a_no_source_df[
                ["adherence_score_openai", "adherence_score_anthropic"]
            ].mean(axis=1)
            exp1a_no_source_df = exp1a_no_source_df.drop(
                columns=["adherence_score_openai", "adherence_score_anthropic"]
            )
        else:
            exp1a_no_source_df["adherence_score"] = exp1a_no_source_df[
                ["adherence_score_openai", "adherence_score_anthropic"]
            ].mean(axis=1)
            exp1a_no_source_df = exp1a_no_source_df.drop(
                columns=["adherence_score_openai", "adherence_score_anthropic"]
            )
        
        print("Data loaded and preprocessed for exp1a, exp1b, and exp1a_no_source.")
    else:
        print("Warning: exp1a_no_source data not found. Some plots may be skipped.")
        print("Data loaded and preprocessed for exp1a and exp1b only.")

    exp1a_df["adherence_score"] = exp1a_df[
        ["adherence_score_openai", "adherence_score_anthropic"]
    ].mean(axis=1)
    exp1b_df["adherence_score"] = exp1b_df[
        ["adherence_score_openai", "adherence_score_anthropic"]
    ].mean(axis=1)

    exp1a_df = exp1a_df.drop(
        columns=["adherence_score_openai", "adherence_score_anthropic"]
    )
    exp1b_df = exp1b_df.drop(
        columns=["adherence_score_openai", "adherence_score_anthropic"]
    )


# In[ ]:


exp1a_no_source_path = os.path.join(INPUT_PATH, "exp1a_no_source.csv")
output_dir_exp1a_no_source = os.path.join(OUTPUT_PATH, "tables/exp1a_no_source")
output_plot_dir_exp1a_no_source = os.path.join(OUTPUT_PATH, "plots/exp1a_no_source")

for path in [output_dir_exp1a_no_source, output_plot_dir_exp1a_no_source]:
    os.makedirs(path, exist_ok=True)


# In[ ]:


def create_annotation_matrix(mean_df, std_df):
    annot = mean_df.copy()
    for i in range(len(mean_df.index)):
        for j in range(len(mean_df.columns)):
            mean_val = mean_df.iloc[i, j]
            std_val = std_df.iloc[i, j]
            if pd.notna(mean_val) and pd.notna(std_val):
                annot.iloc[i, j] = f"{mean_val:.2f}\n({std_val:.2f})"
            elif pd.notna(mean_val):
                annot.iloc[i, j] = f"{mean_val:.2f}"
    return annot

def apply_label_mappings(df):
    mappings = {
        'anthropic': 'Anthropic', 'openai': 'OpenAI', 'google': 'Google', 'deepseek': 'DeepSeek',
        'script': 'Script', 'transcript': 'Transcript', 'tanenbaum': 'Tanenbaum',
        'script_manipulated': 'Script (Manipulated)', 'common': 'Common', 'complex': 'Complex'
    }
    
    if hasattr(df, 'index'):
        df.index = df.index.map(lambda x: mappings.get(x, x))
    if hasattr(df, 'columns'):
        df.columns = df.columns.map(lambda x: mappings.get(x, x))
    return df

def create_dual_heatmap(cosine_pivot, adherence_pivot, title_base, exp_label):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
    
    cos_mean = cosine_pivot["mean"].copy()
    cos_std = cosine_pivot["std"].copy()
    cos_annot = create_annotation_matrix(cos_mean, cos_std)
    
    cos_mean = apply_label_mappings(cos_mean)
    cos_annot = apply_label_mappings(cos_annot)
    
    sns.heatmap(cos_mean, annot=cos_annot, fmt='', cmap='RdYlBu_r',
                center=cos_mean.mean().mean(), square=True, linewidths=0.5, linecolor='white',
                cbar_kws={'shrink': 0.8, 'label': 'Cosine Similarity'},
                annot_kws={'size': 10, 'weight': 'bold'}, ax=ax1)
    ax1.set_title(f"Cosine Similarity (-1 to 1): {title_base} ({exp_label})\nValues: Mean (Std)", 
                  fontsize=12, fontweight='bold', pad=15)
    
    adh_mean = adherence_pivot["mean"].copy()
    adh_std = adherence_pivot["std"].copy()
    adh_annot = create_annotation_matrix(adh_mean, adh_std)
    
    adh_mean = apply_label_mappings(adh_mean)
    adh_annot = apply_label_mappings(adh_annot)
    
    sns.heatmap(adh_mean, annot=adh_annot, fmt='', cmap='RdYlBu_r',
                center=adh_mean.mean().mean(), square=True, linewidths=0.5, linecolor='white',
                cbar_kws={'shrink': 0.8, 'label': 'Adherence Score'},
                annot_kws={'size': 10, 'weight': 'bold'}, ax=ax2)
    ax2.set_title(f"Adherence Score (0 to 1): {title_base} ({exp_label})\nValues: Mean (Std)", 
                  fontsize=12, fontweight='bold', pad=15)
    
    # Set labels
    for ax in [ax1, ax2]:
        ax.set_ylabel("LLM", fontsize=11, labelpad=15)
        if "Input Source" in title_base:
            ax.set_xlabel("Input Source", fontsize=11, labelpad=10)
        elif "Prompt Type" in title_base:
            ax.set_xlabel("Prompt Type", fontsize=11, labelpad=10)
    
    plt.tight_layout()
    plt.show()
    return fig


# # Experiment 1a - Content Analysis

# ## 1.1: Metrics by LLM

# In[ ]:


llm_metrics_1a = exp1a_df.groupby("llm")[["cosine_similarity", "adherence_score"]].agg(
    ["mean", "std"]
)
tables["exp1a_metrics_by_llm"] = llm_metrics_1a
display(llm_metrics_1a)


# ## 1.2: Metrics by Input Source

# In[ ]:


input_source_metrics_1a = exp1a_df.groupby("input_source")[
    ["cosine_similarity", "adherence_score"]
].agg(["mean", "std"])
tables["exp1a_metrics_by_input_source"] = input_source_metrics_1a
display(input_source_metrics_1a)


# ## 1.3: Metrics by Prompt Type

# In[ ]:


prompt_type_metrics_1a = exp1a_df.groupby("prompt_type")[
    ["cosine_similarity", "adherence_score"]
].agg(["mean", "std"])
tables["exp1a_metrics_by_prompt_type"] = prompt_type_metrics_1a
display(prompt_type_metrics_1a)


# ## 1.4: Analysis of MCQ vs Open-Ended Questions

# In[ ]:


import os
import glob
import re
import pandas as pd

def extract_info_from_path(file_path):
    parts = file_path.split(os.sep)
    
    for i, part in enumerate(parts):
        if part in ['common_prompt', 'complex_prompt']:
            prompt_type = 'common' if part == 'common_prompt' else 'complex'
            llm = parts[i + 1] if i + 1 < len(parts) else None
            input_source = parts[i + 2] if i + 2 < len(parts) else None
            
            layer = None
            if i + 3 < len(parts):
                layer_match = re.search(r'layer(\d+)', parts[i + 3])
                layer = int(layer_match.group(1)) if layer_match else None
            
            return input_source, layer, llm, prompt_type
    
    return None, None, None, None

def get_scores_from_df(df, input_source, layer, llm, prompt_type):
    if not all([df is not None, input_source, layer is not None, llm, prompt_type]):
        return None, None
    
    matching_rows = df[
        (df['input_source'] == input_source) & 
        (df['layer'] == layer) & 
        (df['llm'] == llm) & 
        (df['prompt_type'] == prompt_type)
    ]
    
    if not matching_rows.empty:
        return matching_rows['cosine_similarity'].iloc[0], matching_rows['adherence_score'].iloc[0]
    
    fallback_rows = df[(df['input_source'] == input_source) & (df['layer'] == layer)]
    if not fallback_rows.empty:
        return fallback_rows['cosine_similarity'].mean(), fallback_rows['adherence_score'].mean()
    
    return None, None

def analyze_free_text_questions():
    base_path = os.path.join(BASE_PROJECT_PATH, "20_experiments/10_exp1")
    question_files = [f for f in glob.glob(os.path.join(base_path, "**/*_question.txt"), recursive=True) 
                     if not ("complex_prompt" in f and "no_source" in f)]
    
    free_text_data = []
    total_counts = {"exp1a": 0, "exp1b": 0}
    
    for file_path in question_files:
        if "run_a_content" in file_path:
            total_counts["exp1a"] += 1
        elif "run_b_error" in file_path:
            total_counts["exp1b"] += 1
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if "Antwort:" in content and "Antwortmöglichkeiten:" not in content:
                input_source, layer, llm, prompt_type = extract_info_from_path(file_path)
                
                if "run_a_content" in file_path:
                    df, experiment = exp1a_df, "Exp1a"
                elif "run_b_error" in file_path:
                    df, experiment = exp1b_df, "Exp1b"
                    if input_source == 'script':
                        input_source = 'script_manipulated'
                else:
                    continue
                
                cosine_sim, adherence_score = get_scores_from_df(df, input_source, layer, llm, prompt_type)
                
                free_text_data.append({
                    'path': file_path,
                    'experiment': experiment,
                    'input_source': input_source,
                    'layer': layer,
                    'llm': llm,
                    'prompt_type': prompt_type,
                    'cosine_similarity': cosine_sim,
                    'adherence_score': adherence_score
                })
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    return free_text_data, total_counts

free_text_data, total_counts = analyze_free_text_questions()
free_text_df = pd.DataFrame(free_text_data)

exp_counts = free_text_df['experiment'].value_counts()
exp1a_count = exp_counts.get("Exp1a", 0)
exp1b_count = exp_counts.get("Exp1b", 0)

print("FREE TEXT QUESTIONS ANALYSIS")
print("=" * 80)
print(f"Free Text Questions:")
print(f"  Exp1a: {exp1a_count} | Exp1b: {exp1b_count} | Total: {len(free_text_data)}")
print(f"Total Questions (All Types):")
print(f"  Exp1a: {total_counts['exp1a']} | Exp1b: {total_counts['exp1b']} | Total: {sum(total_counts.values())}")
print(f"Free Text Percentages:")
if total_counts['exp1a'] > 0:
    print(f"  Exp1a: {100*exp1a_count/total_counts['exp1a']:.1f}%")
if total_counts['exp1b'] > 0:
    print(f"  Exp1b: {100*exp1b_count/total_counts['exp1b']:.1f}%")
if sum(total_counts.values()) > 0:
    print(f"  Overall: {100*len(free_text_data)/sum(total_counts.values()):.1f}%")

print(f"\n" + "=" * 80)
print("INDIVIDUAL FREE TEXT QUESTIONS:")
print("=" * 80)

for i, item in enumerate(sorted(free_text_data, key=lambda x: (x['experiment'], x['path'])), 1):
    print(f"\n{i}. {item['experiment']} - {item['input_source']} | Layer {item['layer']} | {item['llm']} | {item['prompt_type']}")
    print(f"   Path: {item['path'].replace(BASE_PROJECT_PATH, '...')}")
    if item['cosine_similarity'] is not None and item['adherence_score'] is not None:
        print(f"   Scores: Cosine={item['cosine_similarity']:.3f}, Adherence={item['adherence_score']:.3f}")
    else:
        print(f"   Scores: Not found")

valid_data = free_text_df.dropna(subset=['cosine_similarity', 'adherence_score'])

if not valid_data.empty:
    summary_stats = valid_data.groupby('experiment')[['cosine_similarity', 'adherence_score']].agg(['mean', 'std', 'count']).round(4)
    simple_summary = valid_data.groupby('experiment')[['cosine_similarity', 'adherence_score']].mean().round(4)
    simple_summary['n_questions'] = valid_data.groupby('experiment').size()
    
    print(f"\nDetailed Statistics:")
    display(summary_stats)

    overall_stats = {
        'Mean Cosine Similarity': valid_data['cosine_similarity'].mean(),
        'Mean Adherence Score': valid_data['adherence_score'].mean(),
        'Total Free Text Questions': len(valid_data)
    }
    
    print(f"\nOverall Statistics:")
    for key, value in overall_stats.items():
        print(f"  {key}: {value:.4f}" if isinstance(value, float) else f"  {key}: {value}")
    
    tables["free_text_summary_by_experiment"] = simple_summary
    tables["free_text_detailed_stats"] = summary_stats
else:
    print("No valid free text questions with scores found!")


# ## 1.5: LLM vs Input Source Analysis

# In[ ]:


llm_vs_input_source_cos_sim_1a = pd.pivot_table(
    exp1a_df,
    values="cosine_similarity",
    index="llm",
    columns="input_source",
    aggfunc=["mean", "std"],
)
tables["exp1a_cosine_sim_llm_vs_input_source"] = llm_vs_input_source_cos_sim_1a
display(llm_vs_input_source_cos_sim_1a)


# In[ ]:


adherence_pivot = pd.pivot_table(exp1a_df, values="adherence_score", index="llm", 
                                columns="input_source", aggfunc=["mean", "std"])

fig = create_dual_heatmap(llm_vs_input_source_cos_sim_1a, adherence_pivot, 
                         "LLM vs Input Source", "Exp 1a")
plots['exp1a_combined_llm_vs_input_source'] = fig


# ## 1.6: LLM vs Prompt Type Analysis

# In[ ]:


llm_vs_prompt_type_cos_sim_1a = pd.pivot_table(
    exp1a_df,
    values="cosine_similarity",
    index="llm",
    columns="prompt_type",
    aggfunc=["mean", "std"],
)
tables["exp1a_cosine_sim_llm_vs_prompt_type"] = llm_vs_prompt_type_cos_sim_1a
display(llm_vs_prompt_type_cos_sim_1a)


# In[ ]:


adherence_pivot_prompt = pd.pivot_table(exp1a_df, values="adherence_score", index="llm", 
                                       columns="prompt_type", aggfunc=["mean", "std"])

fig = create_dual_heatmap(llm_vs_prompt_type_cos_sim_1a, adherence_pivot_prompt, 
                         "LLM vs Prompt Type", "Exp 1a")
plots['exp1a_combined_llm_vs_prompt_type'] = fig


# ## 1.7: Distribution Plots

# In[ ]:


fig, ax = plt.subplots(1, 2, figsize=(15, 7))
plots['exp1a_dist_by_llm'] = fig

create_seaborn_boxplot(exp1a_df, 'llm', 'cosine_similarity', ax[0], 
                      'Cosine Similarity (-1 to 1) Distribution by LLM (Exp 1a)',
                      'Cosine Similarity', 'LLM')

create_seaborn_boxplot(exp1a_df, 'llm', 'adherence_score', ax[1],
                      'Adherence Score (0 to 1) Distribution by LLM (Exp 1a)', 
                      'Adherence Score', 'LLM')

plt.tight_layout()
plt.show()


# In[ ]:


fig, ax = plt.subplots(1, 2, figsize=(15, 7))
plots['exp1a_dist_by_input_source'] = fig

create_seaborn_boxplot(exp1a_df, 'input_source', 'cosine_similarity', ax[0], 
                      'Cosine Similarity (-1 to 1) Distribution by Input Source (Exp 1a)',
                      'Cosine Similarity', 'Input Source')

create_seaborn_boxplot(exp1a_df, 'input_source', 'adherence_score', ax[1],
                      'Adherence Score (0 to 1) Distribution by Input Source (Exp 1a)', 
                      'Adherence Score', 'Input Source')

plt.tight_layout()
plt.show()


# # Experiment 1b - Error Analysis

# ## 2.1: Metrics by LLM

# In[ ]:


llm_metrics_1b = exp1b_df.groupby("llm")[["cosine_similarity", "adherence_score"]].agg(
    ["mean", "std"]
)
tables["exp1b_metrics_by_llm"] = llm_metrics_1b
display(llm_metrics_1b)


# ## 2.2: LLM vs Prompt Type Analysis

# In[ ]:


llm_vs_prompt_type_cos_sim_1b = pd.pivot_table(
    exp1b_df,
    values="cosine_similarity",
    index="llm",
    columns="prompt_type",
    aggfunc=["mean", "std"],
)
tables["exp1b_cosine_sim_llm_vs_prompt_type"] = llm_vs_prompt_type_cos_sim_1b
display(llm_vs_prompt_type_cos_sim_1b)


# In[ ]:


adherence_pivot_1b = pd.pivot_table(exp1b_df, values="adherence_score", index="llm", 
                                   columns="prompt_type", aggfunc=["mean", "std"])

fig = create_dual_heatmap(llm_vs_prompt_type_cos_sim_1b, adherence_pivot_1b, 
                         "LLM vs Prompt Type", "Exp 1b")
plots['exp1b_combined_llm_vs_prompt_type'] = fig


# ## 2.3: Distribution Plots

# In[ ]:


fig, ax = plt.subplots(1, 2, figsize=(15, 7))
plots['exp1b_dist_by_llm'] = fig

create_seaborn_boxplot(exp1b_df, 'llm', 'cosine_similarity', ax[0], 
                      'Cosine Similarity (-1 to 1) Distribution by LLM (Exp 1b)',
                      'Cosine Similarity', 'LLM')

create_seaborn_boxplot(exp1b_df, 'llm', 'adherence_score', ax[1],
                      'Adherence Score (0 to 1) Distribution by LLM (Exp 1b)', 
                      'Adherence Score', 'LLM')

plt.tight_layout()
plt.show()


# # Experiment 1a - Source vs No Source Comparison

# ## 3.1: No Source Individual Analysis

# In[ ]:


if exp1a_no_source_df is not None:
    print("Creating plots for exp1a_no_source data...")
    
    has_comparison_source = 'comparison_source' in exp1a_no_source_df.columns
    
    if has_comparison_source:
        print(f"Data shape: {exp1a_no_source_df.shape}")
        print(f"Comparison sources: {exp1a_no_source_df['comparison_source'].unique()}")
        
        fig, ax = plt.subplots(1, 2, figsize=(15, 7))
        plots['exp1a_no_source_dist_by_llm'] = fig

        create_seaborn_boxplot(exp1a_no_source_df, 'llm', 'cosine_similarity', ax[0], 
                              'Cosine Similarity (-1 to 1) Distribution by LLM (Exp 1a No Source)',
                              'Cosine Similarity', 'LLM')

        create_seaborn_boxplot(exp1a_no_source_df, 'llm', 'adherence_score', ax[1],
                              'Adherence Score (0 to 1) Distribution by LLM (Exp 1a No Source)', 
                              'Adherence Score', 'LLM')

        plt.tight_layout()
        plt.show()

        
        fig, ax = plt.subplots(1, 2, figsize=(15, 7))
        plots['exp1a_no_source_dist_by_comparison_source'] = fig

        create_seaborn_boxplot(exp1a_no_source_df, 'comparison_source', 'cosine_similarity', ax[0], 
                              'Cosine Similarity (-1 to 1) by Comparison Source (Exp 1a No Source)',
                              'Cosine Similarity', 'Comparison Source')

        create_seaborn_boxplot(exp1a_no_source_df, 'comparison_source', 'adherence_score', ax[1],
                              'Adherence Score (0 to 1) by Comparison Source (Exp 1a No Source)', 
                              'Adherence Score', 'Comparison Source')

        plt.tight_layout()
        plt.show()
        
    print("exp1a_no_source plots created successfully!")
else:
    print("Skipping exp1a_no_source plots - data not available.")


# ## 3.2: Input Source vs No Source Comparison

# In[ ]:


# Combined Input Source vs No Source Comparison
if exp1a_no_source_df is not None:
    print("Creating combined Input Source vs No Source comparison plot...")
    
    exp1a_regular = exp1a_df.copy()
    exp1a_no_source_agg = exp1a_no_source_df.copy()
    exp1a_no_source_agg['input_source'] = 'no_source'
    
    comparison_df = pd.concat([exp1a_regular, exp1a_no_source_agg], ignore_index=True)
    
    fig, ax = plt.subplots(1, 2, figsize=(16, 7))
    plots['exp1a_input_source_vs_no_source_comparison'] = fig
    
    comparison_means = comparison_df.groupby('input_source')[['cosine_similarity', 'adherence_score']].mean()
    
    create_seaborn_boxplot(comparison_df, 'input_source', 'cosine_similarity', ax[0], 
                          'Cosine Similarity: Input Sources vs No Source (Exp 1a)', 
                          'Cosine Similarity', 'Input Source',
                          custom_means=comparison_means['cosine_similarity'])
    
    create_seaborn_boxplot(comparison_df, 'input_source', 'adherence_score', ax[1],
                          'Adherence Score: Input Sources vs No Source (Exp 1a)', 
                          'Adherence Score', 'Input Source',
                          custom_means=comparison_means['adherence_score'])
    
    plt.tight_layout()
    plt.show()
    
    comparison_summary = comparison_df.groupby('input_source')[['cosine_similarity', 'adherence_score']].agg(['mean', 'std', 'count'])
    tables['exp1a_input_source_vs_no_source_summary'] = comparison_summary
    
    print("\nSummary Statistics:")
    display(comparison_summary)
    
    print("\nInput Source vs No Source comparison created successfully!")
else:
    print("Skipping Input Source vs No Source comparison - exp1a_no_source data not available.")


# # Save Results

# In[ ]:


def save_all_tables_and_plots():
    for name, df in tables.items():
        if name.startswith("exp1a_no_source"):
            output_dir = output_dir_exp1a_no_source
            table_name = name.replace("exp1a_no_source_", "")
        elif name.startswith("exp1a"):
            output_dir = output_dir_exp1a
            table_name = name.replace("exp1a_", "")
        elif name.startswith("exp1b"):
            output_dir = output_dir_exp1b
            table_name = name.replace("exp1b_", "")
        else:
            if "exp1" in name:
                base_filename = os.path.join(output_dir_exp1a, name)
                csv_path = f"{base_filename}.csv"
                df.to_csv(csv_path)
                print(f"Saved {csv_path}")
            continue

        base_filename = os.path.join(output_dir, table_name)
        
        csv_path = f"{base_filename}.csv"
        df.to_csv(csv_path)
        print(f"Saved {csv_path}")

    for name, fig in plots.items():
        if name.startswith("exp1a_no_source") or "no_source" in name:
            output_dir = output_plot_dir_exp1a_no_source
            plot_name = name.replace("exp1a_no_source_", "").replace("exp1a_", "")
        elif name.startswith("exp1a"):
            output_dir = output_plot_dir_exp1a
            plot_name = name.replace("exp1a_", "")
        elif name.startswith("exp1b"):
            output_dir = output_plot_dir_exp1b
            plot_name = name.replace("exp1b_", "")
        else:
            if "exp1" in name:
                base_filename = os.path.join(output_plot_dir_exp1a, name)
                png_path = f"{base_filename}.png"
                fig.savefig(png_path, bbox_inches='tight')
                print(f"Saved {png_path}")
            continue
        
        base_filename = os.path.join(output_dir, plot_name)
        
        png_path = f"{base_filename}.png"
        fig.savefig(png_path, bbox_inches='tight')
        print(f"Saved {png_path}")

save_all_tables_and_plots()

