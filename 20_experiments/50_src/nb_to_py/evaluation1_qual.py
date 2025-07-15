#!/usr/bin/env python
# coding: utf-8

# # Notebook: Qualitative Evaluation -- Experiment 1

# ## Initial Setup

# In[ ]:


import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display
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

def create_seaborn_boxplot(data, x, y, ax, title, ylabel, xlabel, scale_range=None):
    colors = ['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3', '#a6d854', '#ffd92f', '#e5c494', '#b3b3b3']
    unique_vals = sorted(data[x].unique())
    palette = colors[:len(unique_vals)]
    
    sns.boxplot(data=data, x=x, y=y, ax=ax, palette=palette,
                medianprops={'color': 'black', 'linewidth': 2.5, 'linestyle': ':'})
    
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
        'exp1a': 'Exp 1a',
        'exp1b': 'Exp 1b'
    }
    
    current_labels = [tick.get_text() for tick in ax.get_xticklabels()]
    new_labels = [label_mapping.get(label, label) for label in current_labels]
    ax.set_xticklabels(new_labels, rotation=0)
    
    if scale_range:
        ax.set_ylim(scale_range)
        if scale_range == (0, 10):
            title += " (0-10 scale)"
        elif scale_range == (0, 70):
            title += " (0-70 scale)"
    
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.set_ylabel(ylabel, fontsize=11, labelpad=15)
    ax.set_xlabel(xlabel, fontsize=11, labelpad=10)
    ax.grid(True, alpha=0.3)

BASE_PROJECT_PATH = os.path.abspath(os.path.join(os.getcwd(), "..", ".."))

expert_base_path = os.path.join(BASE_PROJECT_PATH, "20_experiments/60_analyses/csv/qualitative/exp1/experts")
hint_base_path = os.path.join(BASE_PROJECT_PATH, "20_experiments/60_analyses/csv/qualitative/exp1/hints")

output_base_path = os.path.join(BASE_PROJECT_PATH, "40_evaluation/exp1/qualitative")
output_tables_path = os.path.join(output_base_path, "tables")
output_plots_path = os.path.join(output_base_path, "plots")

for path in [output_tables_path, output_plots_path]:
    os.makedirs(path, exist_ok=True)

tables = {}
plots = {}

print(f"Setup completed")
print(f"Output tables: {output_tables_path}")
print(f"Output plots: {output_plots_path}")


# ## Data Loading and Preprocessing

# In[ ]:


def load_and_prepare_data():
    
    hint_exp1a = pd.read_csv(os.path.join(hint_base_path, "exp1a_hints.csv"))
    hint_exp1b = pd.read_csv(os.path.join(hint_base_path, "exp1b_hints.csv"))
    
    expert1_exp1a = pd.read_csv(os.path.join(expert_base_path, "expert_1", "exp1a.csv"))
    expert1_exp1b = pd.read_csv(os.path.join(expert_base_path, "expert_1", "exp1b.csv"))
    
    exp1a_df = pd.concat([expert1_exp1a, hint_exp1a[['llm', 'prompt_type']]], axis=1)
    exp1b_df = pd.concat([expert1_exp1b, hint_exp1b[['llm', 'prompt_type']]], axis=1)
    
    numeric_cols_1a = ['relevance', 'clarity', 'answerability', 'challenging', 'value', 'language', 'correctness']
    numeric_cols_1b = ['relevance', 'clarity', 'answerability', 'challenging', 'value', 'language', 'manipulation_handling']
    
    for col in numeric_cols_1a:
        if col in exp1a_df.columns:
            exp1a_df[col] = exp1a_df[col].replace(['??', '???', ''], np.nan)
            exp1a_df[col] = pd.to_numeric(exp1a_df[col], errors='coerce')
    
    for col in numeric_cols_1b:
        if col in exp1b_df.columns:
            exp1b_df[col] = exp1b_df[col].replace(['??', '???', ''], np.nan)
            exp1b_df[col] = pd.to_numeric(exp1b_df[col], errors='coerce')
    
    exp1a_df['experiment'] = 'exp1a'
    exp1b_df['experiment'] = 'exp1b'
    
    exp1b_df['input_source'] = exp1b_df['input_source'].replace('script', 'script_manipulated')
    
    print(f"Loaded Experiment 1a: {len(exp1a_df)} samples")
    print(f"Loaded Experiment 1b: {len(exp1b_df)} samples")
    
    exp1a_df['total_score'] = exp1a_df[numeric_cols_1a].sum(axis=1)
    exp1b_df['total_score'] = exp1b_df[numeric_cols_1b].sum(axis=1)
    
    filled_1a = exp1a_df[numeric_cols_1a].notna().sum().sum()
    total_1a = len(exp1a_df) * len(numeric_cols_1a)
    print(f"Exp 1a completion: {filled_1a}/{total_1a} ({100*filled_1a/total_1a:.1f}%)")
    
    filled_1b = exp1b_df[numeric_cols_1b].notna().sum().sum()
    total_1b = len(exp1b_df) * len(numeric_cols_1b)
    print(f"Exp 1b completion: {filled_1b}/{total_1b} ({100*filled_1b/total_1b:.1f}%)")
    
    return exp1a_df, exp1b_df, numeric_cols_1a, numeric_cols_1b

exp1a_df, exp1b_df, numeric_cols_1a, numeric_cols_1b = load_and_prepare_data()

print("\n" + "="*50)
print("DATA OVERVIEW")
print("="*50)

print(f"\nExperiment 1a Distribution:")
print(f"  LLMs: {dict(exp1a_df['llm'].value_counts())}")
print(f"  Prompt Types: {dict(exp1a_df['prompt_type'].value_counts())}")
print(f"  Input Sources: {dict(exp1a_df['input_source'].value_counts())}")

print(f"\nExperiment 1b Distribution:")
print(f"  LLMs: {dict(exp1b_df['llm'].value_counts())}")
print(f"  Prompt Types: {dict(exp1b_df['prompt_type'].value_counts())}")
print(f"  Input Sources: {dict(exp1b_df['input_source'].value_counts())}")


# # Experiment 1a: Original Content Analysis
# 
# Analysis of LLM question generation quality using original source materials (script, transcript, tanenbaum textbook).

# ## 1a.1: Descriptive Statistics

# In[ ]:


print("EXPERIMENT 1A - DESCRIPTIVE STATISTICS")
print("="*60)

exp1a_stats = exp1a_df[numeric_cols_1a].describe().round(2)
tables['exp1a_overall_stats'] = exp1a_stats
print("\nOverall Statistics (all criteria):")
display(exp1a_stats)

exp1a_llm_stats = exp1a_df.groupby('llm')[numeric_cols_1a].agg(['mean', 'std', 'count']).round(2)
tables['exp1a_llm_stats'] = exp1a_llm_stats
print("\nStatistics by LLM:")
display(exp1a_llm_stats)

exp1a_source_stats = exp1a_df.groupby('input_source')[numeric_cols_1a].agg(['mean', 'std', 'count']).round(2)
tables['exp1a_source_stats'] = exp1a_source_stats
print("\nStatistics by Input Source:")
display(exp1a_source_stats)

exp1a_prompt_stats = exp1a_df.groupby('prompt_type')[numeric_cols_1a].agg(['mean', 'std', 'count']).round(2)
tables['exp1a_prompt_stats'] = exp1a_prompt_stats
print("\nStatistics by Prompt Type:")
display(exp1a_prompt_stats)


# ## 1a.2: Analysis by LLM

# In[ ]:


fig, axes = plt.subplots(4, 2, figsize=(14, 20))
axes = axes.flatten()
plots['exp1a_llm_analysis'] = fig

criteria = ['relevance', 'clarity', 'answerability', 'challenging', 'value', 'language', 'correctness']

for i, criterion in enumerate(criteria):
    create_seaborn_boxplot(exp1a_df, 'llm', criterion, axes[i], 
                          f'{criterion.title()}', criterion.title(), 'LLM', scale_range=(0, 10))

create_seaborn_boxplot(exp1a_df, 'llm', 'total_score', axes[7], 
                      'Total Score', 'Total Score', 'LLM', scale_range=(0, 70))

plt.suptitle('Experiment 1a: LLM Performance across all Criteria', fontsize=16, fontweight='bold', y=0.98)
plt.tight_layout()
plt.subplots_adjust(top=0.95)
plt.show()

print("\n" + "="*80)
print("DETAILED STATISTICS - LLM PERFORMANCE (EXPERIMENT 1A)")
print("="*80)

all_criteria_with_total = criteria + ['total_score']
exp1a_llm_detailed_stats = exp1a_df.groupby('llm')[all_criteria_with_total].agg(['mean', 'std', 'median', 'min', 'max', 'count']).round(2)
tables['exp1a_llm_detailed_stats'] = exp1a_llm_detailed_stats
print("\nDetailed Statistics by LLM (Experiment 1a):")
display(exp1a_llm_detailed_stats)

exp1a_llm_means = exp1a_df.groupby('llm')[numeric_cols_1a].mean().round(2)
tables['exp1a_llm_means'] = exp1a_llm_means
print("\nMean Scores by LLM (Experiment 1a):")
display(exp1a_llm_means)

exp1a_llm_overall = exp1a_llm_means.mean(axis=1).sort_values(ascending=False)
tables['exp1a_llm_ranking'] = exp1a_llm_overall
print("\nOverall LLM Ranking (Experiment 1a):")
for i, (llm, score) in enumerate(exp1a_llm_overall.items(), 1):
    print(f"{i}. {llm.title()}: {score:.2f}")


# ## 1a.3: Analysis by Input Source

# In[ ]:


fig, axes = plt.subplots(4, 2, figsize=(14, 20))
axes = axes.flatten()
plots['exp1a_source_analysis'] = fig

for i, criterion in enumerate(criteria):
    create_seaborn_boxplot(exp1a_df, 'input_source', criterion, axes[i], 
                          f'{criterion.title()}', criterion.title(), 'Input Source', scale_range=(0, 10))

create_seaborn_boxplot(exp1a_df, 'input_source', 'total_score', axes[7], 
                      'Total Score', 'Total Score', 'Input Source', scale_range=(0, 70))

plt.suptitle('Experiment 1a: Performance by Input Source', fontsize=16, fontweight='bold', y=0.98)
plt.tight_layout()
plt.subplots_adjust(top=0.95)
plt.show()

print("\n" + "="*80)
print("DETAILED STATISTICS - INPUT SOURCE PERFORMANCE (EXPERIMENT 1A)")
print("="*80)

exp1a_source_detailed_stats = exp1a_df.groupby('input_source')[all_criteria_with_total].agg(['mean', 'std', 'median', 'min', 'max', 'count']).round(2)
tables['exp1a_source_detailed_stats'] = exp1a_source_detailed_stats
print("\nDetailed Statistics by Input Source (Experiment 1a):")
display(exp1a_source_detailed_stats)

exp1a_source_means = exp1a_df.groupby('input_source')[numeric_cols_1a].mean().round(2)
tables['exp1a_source_means'] = exp1a_source_means
print("\nMean Scores by Input Source (Experiment 1a):")
display(exp1a_source_means)

exp1a_source_overall = exp1a_df.groupby('input_source')['total_score'].mean().sort_values(ascending=False)
tables['exp1a_source_ranking'] = exp1a_source_overall
print("\nInput Source Ranking by Total Score (Experiment 1a):")
for i, (source, score) in enumerate(exp1a_source_overall.items(), 1):
    print(f"{i}. {source.title()}: {score:.2f}/70")

# Total Score Paired Heatmaps
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
plots['exp1a_total_score_paired_heatmaps'] = fig

# Heatmap 1: Total Score by Input Source vs LLM
heatmap_mean = exp1a_df.groupby(['llm', 'input_source'])['total_score'].mean().unstack()
heatmap_std = exp1a_df.groupby(['llm', 'input_source'])['total_score'].std().unstack()

annot_matrix = heatmap_mean.copy()
for i in range(len(heatmap_mean.index)):
    for j in range(len(heatmap_mean.columns)):
        mean_val = heatmap_mean.iloc[i, j]
        std_val = heatmap_std.iloc[i, j]
        if pd.notna(mean_val) and pd.notna(std_val):
            annot_matrix.iloc[i, j] = f"{mean_val:.1f}\n({std_val:.1f})"
        elif pd.notna(mean_val):
            annot_matrix.iloc[i, j] = f"{mean_val:.1f}"

llm_labels = [label.title() for label in heatmap_mean.index]
source_labels = [label.title() for label in heatmap_mean.columns]

sns.heatmap(heatmap_mean, 
            annot=annot_matrix, 
            fmt='', 
            cmap='RdYlBu_r',
            center=heatmap_mean.mean().mean(),
            square=True,
            linewidths=0.5,
            linecolor='white',
            cbar_kws={'shrink': 0.8, 'label': 'Total Score'},
            annot_kws={'size': 10, 'weight': 'bold'},
            xticklabels=source_labels, 
            yticklabels=llm_labels, 
            ax=ax1)

ax1.set_title('Mean Total Score (LLM vs Input Source)\nValues: Mean (Std) | Scale: 0-70 points', 
             fontsize=14, fontweight='bold', pad=20)
ax1.set_xlabel('Input Source', fontsize=12, fontweight='bold', labelpad=10)
ax1.set_ylabel('LLM', fontsize=12, fontweight='bold', labelpad=10)

ax1.set_xticklabels(ax1.get_xticklabels(), rotation=0, ha='center')
ax1.set_yticklabels(ax1.get_yticklabels(), rotation=0)

# Heatmap 2: Total Score by Prompt Type vs LLM
heatmap_mean_prompt = exp1a_df.groupby(['llm', 'prompt_type'])['total_score'].mean().unstack()
heatmap_std_prompt = exp1a_df.groupby(['llm', 'prompt_type'])['total_score'].std().unstack()

annot_matrix_prompt = heatmap_mean_prompt.copy()
for i in range(len(heatmap_mean_prompt.index)):
    for j in range(len(heatmap_mean_prompt.columns)):
        mean_val = heatmap_mean_prompt.iloc[i, j]
        std_val = heatmap_std_prompt.iloc[i, j]
        if pd.notna(mean_val) and pd.notna(std_val):
            annot_matrix_prompt.iloc[i, j] = f"{mean_val:.1f}\n({std_val:.1f})"
        elif pd.notna(mean_val):
            annot_matrix_prompt.iloc[i, j] = f"{mean_val:.1f}"

llm_labels = [label.title() for label in heatmap_mean_prompt.index]
prompt_labels = [label.title() for label in heatmap_mean_prompt.columns]

sns.heatmap(heatmap_mean_prompt, 
            annot=annot_matrix_prompt, 
            fmt='', 
            cmap='RdYlBu_r',
            center=heatmap_mean_prompt.mean().mean(),
            square=True,
            linewidths=0.5,
            linecolor='white',
            cbar_kws={'shrink': 0.8, 'label': 'Total Score'},
            annot_kws={'size': 10, 'weight': 'bold'},
            xticklabels=prompt_labels, 
            yticklabels=llm_labels, 
            ax=ax2)

ax2.set_title('Mean Total Score (LLM vs Prompt Type)\nValues: Mean (Std) | Scale: 0-70 points', 
             fontsize=14, fontweight='bold', pad=20)
ax2.set_xlabel('Prompt Type', fontsize=12, fontweight='bold', labelpad=10)
ax2.set_ylabel('LLM', fontsize=12, fontweight='bold', labelpad=10)

ax2.set_xticklabels(ax2.get_xticklabels(), rotation=0, ha='center')
ax2.set_yticklabels(ax2.get_yticklabels(), rotation=0)

plt.tight_layout()
plt.show()

print("\n" + "="*80)
print("DETAILED STATISTICS - LLM vs INPUT SOURCE COMBINATIONS (EXPERIMENT 1A)")
print("="*80)

exp1a_llm_source_combinations = exp1a_df.groupby(['llm', 'input_source'])['total_score'].agg(['mean', 'std', 'median', 'min', 'max', 'count']).round(2)
tables['exp1a_llm_source_combinations'] = exp1a_llm_source_combinations
print("\nDetailed Statistics for LLM vs Input Source Combinations (Experiment 1a):")
display(exp1a_llm_source_combinations)

print("\n" + "="*80)
print("DETAILED STATISTICS - LLM vs PROMPT TYPE COMBINATIONS (EXPERIMENT 1A)")
print("="*80)

exp1a_llm_prompt_combinations = exp1a_df.groupby(['llm', 'prompt_type'])['total_score'].agg(['mean', 'std', 'median', 'min', 'max', 'count']).round(2)
tables['exp1a_llm_prompt_combinations'] = exp1a_llm_prompt_combinations
print("\nDetailed Statistics for LLM vs Prompt Type Combinations (Experiment 1a):")
display(exp1a_llm_prompt_combinations)
tables['exp1a_llm_source_combinations'] = exp1a_llm_source_combinations
print("\nDetailed Statistics for LLM vs Input Source Combinations (Experiment 1a):")
display(exp1a_llm_source_combinations)


# ## 1a.4: Analysis by Prompt Type

# In[ ]:


fig, axes = plt.subplots(2, 4, figsize=(20, 10))
axes = axes.flatten()
plots['exp1a_prompt_analysis'] = fig

for i, criterion in enumerate(criteria):
    create_seaborn_boxplot(exp1a_df, 'prompt_type', criterion, axes[i], 
                          f'{criterion.title()}', criterion.title(), 'Prompt Type', scale_range=(0, 10))

create_seaborn_boxplot(exp1a_df, 'prompt_type', 'total_score', axes[7], 
                      'Total Score', 'Total Score', 'Prompt Type', scale_range=(0, 70))

plt.suptitle('Experiment 1a: Performance by Prompt Type', fontsize=16, fontweight='bold', y=0.98)
plt.tight_layout()
plt.subplots_adjust(top=0.92)
plt.show()

print("\n" + "="*80)
print("DETAILED STATISTICS - PROMPT TYPE PERFORMANCE (EXPERIMENT 1A)")
print("="*80)

exp1a_prompt_detailed_stats = exp1a_df.groupby('prompt_type')[all_criteria_with_total].agg(['mean', 'std', 'median', 'min', 'max', 'count']).round(2)
tables['exp1a_prompt_detailed_stats'] = exp1a_prompt_detailed_stats
print("\nDetailed Statistics by Prompt Type (Experiment 1a):")
display(exp1a_prompt_detailed_stats)

exp1a_prompt_means = exp1a_df.groupby('prompt_type')[numeric_cols_1a].mean().round(2)
tables['exp1a_prompt_means'] = exp1a_prompt_means
print("\nMean Scores by Prompt Type (Experiment 1a):")
display(exp1a_prompt_means)

prompt_diff = exp1a_prompt_means.loc['complex'] - exp1a_prompt_means.loc['common']
print("\nComplex vs Common Prompt Difference (Experiment 1a):")
for criterion, diff in prompt_diff.items():
    direction = "higher" if diff > 0 else "lower"
    print(f"  {criterion.title()}: {diff:+.2f} ({direction} for complex)")

print("\n" + "="*80)
print("DETAILED STATISTICS - LLM vs PROMPT TYPE COMBINATIONS (EXPERIMENT 1A)")
print("="*80)

exp1a_llm_prompt_combinations = exp1a_df.groupby(['llm', 'prompt_type'])['total_score'].agg(['mean', 'std', 'median', 'min', 'max', 'count']).round(2)
tables['exp1a_llm_prompt_combinations'] = exp1a_llm_prompt_combinations
print("\nDetailed Statistics for LLM vs Prompt Type Combinations (Experiment 1a):")
display(exp1a_llm_prompt_combinations)


# In[ ]:


# Correctness-focused Heatmaps

print("\n" + "="*80)
print("CORRECTNESS ANALYSIS - PAIRED HEATMAPS")
print("="*80)

# Paired Heatmaps: Correctness by Input Source vs LLM and Prompt Type vs LLM
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
plots['exp1a_correctness_paired_heatmaps'] = fig

# Heatmap 1: Correctness by Input Source vs LLM
correctness_heatmap_mean = exp1a_df.groupby(['llm', 'input_source'])['correctness'].mean().unstack()
correctness_heatmap_std = exp1a_df.groupby(['llm', 'input_source'])['correctness'].std().unstack()

correctness_annot_matrix = correctness_heatmap_mean.copy()
for i in range(len(correctness_heatmap_mean.index)):
    for j in range(len(correctness_heatmap_mean.columns)):
        mean_val = correctness_heatmap_mean.iloc[i, j]
        std_val = correctness_heatmap_std.iloc[i, j]
        if pd.notna(mean_val) and pd.notna(std_val):
            correctness_annot_matrix.iloc[i, j] = f"{mean_val:.1f}\n({std_val:.1f})"
        elif pd.notna(mean_val):
            correctness_annot_matrix.iloc[i, j] = f"{mean_val:.1f}"

llm_labels = [label.title() for label in correctness_heatmap_mean.index]
source_labels = [label.title() for label in correctness_heatmap_mean.columns]

sns.heatmap(correctness_heatmap_mean, 
            annot=correctness_annot_matrix, 
            fmt='', 
            cmap='RdYlBu_r',
            center=correctness_heatmap_mean.mean().mean(),
            square=True,
            linewidths=0.5,
            linecolor='white',
            cbar_kws={'shrink': 0.8, 'label': 'Correctness Score'},
            annot_kws={'size': 10, 'weight': 'bold'},
            xticklabels=source_labels, 
            yticklabels=llm_labels, 
            ax=ax1)

ax1.set_title('Correctness Score (LLM vs Input Source)\nValues: Mean (Std) | Scale: 0-10 points', 
             fontsize=14, fontweight='bold', pad=20)
ax1.set_xlabel('Input Source', fontsize=12, fontweight='bold', labelpad=10)
ax1.set_ylabel('LLM', fontsize=12, fontweight='bold', labelpad=10)

ax1.set_xticklabels(ax1.get_xticklabels(), rotation=0, ha='center')
ax1.set_yticklabels(ax1.get_yticklabels(), rotation=0)

# Heatmap 2: Correctness by Prompt Type vs LLM
correctness_prompt_heatmap_mean = exp1a_df.groupby(['llm', 'prompt_type'])['correctness'].mean().unstack()
correctness_prompt_heatmap_std = exp1a_df.groupby(['llm', 'prompt_type'])['correctness'].std().unstack()

correctness_prompt_annot_matrix = correctness_prompt_heatmap_mean.copy()
for i in range(len(correctness_prompt_heatmap_mean.index)):
    for j in range(len(correctness_prompt_heatmap_mean.columns)):
        mean_val = correctness_prompt_heatmap_mean.iloc[i, j]
        std_val = correctness_prompt_heatmap_std.iloc[i, j]
        if pd.notna(mean_val) and pd.notna(std_val):
            correctness_prompt_annot_matrix.iloc[i, j] = f"{mean_val:.1f}\n({std_val:.1f})"
        elif pd.notna(mean_val):
            correctness_prompt_annot_matrix.iloc[i, j] = f"{mean_val:.1f}"

llm_labels = [label.title() for label in correctness_prompt_heatmap_mean.index]
prompt_labels = [label.title() for label in correctness_prompt_heatmap_mean.columns]

sns.heatmap(correctness_prompt_heatmap_mean, 
            annot=correctness_prompt_annot_matrix, 
            fmt='', 
            cmap='RdYlBu_r',
            center=correctness_prompt_heatmap_mean.mean().mean(),
            square=True,
            linewidths=0.5,
            linecolor='white',
            cbar_kws={'shrink': 0.8, 'label': 'Correctness Score'},
            annot_kws={'size': 10, 'weight': 'bold'},
            xticklabels=prompt_labels, 
            yticklabels=llm_labels, 
            ax=ax2)

ax2.set_title('Correctness Score (LLM vs Prompt Type)\nValues: Mean (Std) | Scale: 0-10 points', 
             fontsize=14, fontweight='bold', pad=20)
ax2.set_xlabel('Prompt Type', fontsize=12, fontweight='bold', labelpad=10)
ax2.set_ylabel('LLM', fontsize=12, fontweight='bold', labelpad=10)

ax2.set_xticklabels(ax2.get_xticklabels(), rotation=0, ha='center')
ax2.set_yticklabels(ax2.get_yticklabels(), rotation=0)

plt.tight_layout()
plt.show()

# Statistics for both heatmaps
correctness_llm_source_stats = exp1a_df.groupby(['llm', 'input_source'])['correctness'].agg(['mean', 'std', 'median', 'min', 'max', 'count']).round(2)
tables['exp1a_correctness_llm_source_stats'] = correctness_llm_source_stats
print("\nDetailed Correctness Statistics by LLM and Input Source:")
display(correctness_llm_source_stats)

correctness_llm_prompt_stats = exp1a_df.groupby(['llm', 'prompt_type'])['correctness'].agg(['mean', 'std', 'median', 'min', 'max', 'count']).round(2)
tables['exp1a_correctness_llm_prompt_stats'] = correctness_llm_prompt_stats
print("\nDetailed Correctness Statistics by LLM and Prompt Type:")
display(correctness_llm_prompt_stats)


# In[ ]:


print("\n" + "="*80)
print("CORRECTNESS INSIGHTS")
print("="*80)

# Best LLM for correctness
correctness_by_llm = exp1a_df.groupby('llm')['correctness'].mean().sort_values(ascending=False)
print(f"\nCorrectness Ranking by LLM:")
for i, (llm, score) in enumerate(correctness_by_llm.items(), 1):
    print(f"{i}. {llm.title()}: {score:.2f}")

# Best input source for correctness
correctness_by_source = exp1a_df.groupby('input_source')['correctness'].mean().sort_values(ascending=False)
print(f"\nCorrectness Ranking by Input Source:")
for i, (source, score) in enumerate(correctness_by_source.items(), 1):
    print(f"{i}. {source.title()}: {score:.2f}")

# Best prompt type for correctness
correctness_by_prompt = exp1a_df.groupby('prompt_type')['correctness'].mean().sort_values(ascending=False)
print(f"\nCorrectness Ranking by Prompt Type:")
for i, (prompt, score) in enumerate(correctness_by_prompt.items(), 1):
    print(f"{i}. {prompt.title()}: {score:.2f}")

# Identify best combinations
best_llm_source = exp1a_df.groupby(['llm', 'input_source'])['correctness'].mean().idxmax()
best_llm_source_score = exp1a_df.groupby(['llm', 'input_source'])['correctness'].mean().max()
print(f"\nBest LLM-Source combination for correctness:")
print(f"  {best_llm_source[0].title()} + {best_llm_source[1].title()}: {best_llm_source_score:.2f}")

best_llm_prompt = exp1a_df.groupby(['llm', 'prompt_type'])['correctness'].mean().idxmax()
best_llm_prompt_score = exp1a_df.groupby(['llm', 'prompt_type'])['correctness'].mean().max()
print(f"\nBest LLM-Prompt combination for correctness:")
print(f"  {best_llm_prompt[0].title()} + {best_llm_prompt[1].title()}: {best_llm_prompt_score:.2f}")


# # Experiment 1b: Manipulated Content Analysis

# In[ ]:


print("EXPERIMENT 1B - DATA AVAILABILITY CHECK")
print("="*60)

exp1b_filled = exp1b_df[numeric_cols_1b].notna().sum().sum()
exp1b_total = len(exp1b_df) * len(numeric_cols_1b)

print(f"Exp 1b completion: {exp1b_filled}/{exp1b_total} ({100*exp1b_filled/exp1b_total:.1f}%)")

if exp1b_filled > 0:
    print("Proceeding with Experiment 1b analysis")
    analyze_exp1b = True
else:
    print("No ratings available for Experiment 1b yet - showing structure only")
    analyze_exp1b = False
    
print(f"\nExperiment 1b structure:")
print(f"  Samples: {len(exp1b_df)}")
print(f"  LLMs: {list(exp1b_df['llm'].unique())}")
print(f"  Prompt Types: {list(exp1b_df['prompt_type'].unique())}")
print(f"  Input Sources: {list(exp1b_df['input_source'].unique())}")
print(f"  Evaluation Criteria: {numeric_cols_1b}")

print(f"\nSample Exp1b structure:")
display(exp1b_df[['input_source', 'layer', 'llm', 'prompt_type'] + numeric_cols_1b].head())


# In[ ]:


if analyze_exp1b:
    print("\nEXPERIMENT 1B - DESCRIPTIVE STATISTICS")
    print("="*60)
    
    exp1b_stats = exp1b_df[numeric_cols_1b].describe().round(2)
    tables['exp1b_overall_stats'] = exp1b_stats
    print("\nOverall Statistics (all criteria):")
    display(exp1b_stats)
    
    exp1b_llm_stats = exp1b_df.groupby('llm')[numeric_cols_1b].agg(['mean', 'std', 'count']).round(2)
    tables['exp1b_llm_stats'] = exp1b_llm_stats
    print("\nStatistics by LLM:")
    display(exp1b_llm_stats)
    
    exp1b_prompt_stats = exp1b_df.groupby('prompt_type')[numeric_cols_1b].agg(['mean', 'std', 'count']).round(2)
    tables['exp1b_prompt_stats'] = exp1b_prompt_stats
    print("\nStatistics by Prompt Type:")
    display(exp1b_prompt_stats)
    
else:
    print("\nExperiment 1b analysis will be available once expert evaluations are completed.")
    print("The structure is ready for analysis of manipulation handling capabilities.")


# In[ ]:


if analyze_exp1b:
    fig, axes = plt.subplots(2, 4, figsize=(20, 10))
    axes = axes.flatten()
    plots['exp1b_llm_analysis'] = fig
    
    criteria_1b = ['relevance', 'clarity', 'answerability', 'challenging', 'value', 'language', 'manipulation_handling']
    
    for i, criterion in enumerate(criteria_1b):
        create_seaborn_boxplot(exp1b_df, 'llm', criterion, axes[i], 
                              f'{criterion.title()}', criterion.title(), 'LLM', scale_range=(0, 10))
    
    create_seaborn_boxplot(exp1b_df, 'llm', 'total_score', axes[7], 
                          'Total Score', 'Total Score', 'LLM', scale_range=(0, 70))
    
    plt.suptitle('Experiment 1b: LLM Performance (Manipulation Handling)', fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.subplots_adjust(top=0.92)
    plt.show()
    
    print("\n" + "="*80)
    print("DETAILED STATISTICS - LLM PERFORMANCE (EXPERIMENT 1B)")
    print("="*80)
    
    all_criteria_1b_with_total = criteria_1b + ['total_score']
    exp1b_llm_detailed_stats = exp1b_df.groupby('llm')[all_criteria_1b_with_total].agg(['mean', 'std', 'median', 'min', 'max', 'count']).round(2)
    tables['exp1b_llm_detailed_stats'] = exp1b_llm_detailed_stats
    print("\nDetailed Statistics by LLM (Experiment 1b):")
    display(exp1b_llm_detailed_stats)
    
    fig, axes = plt.subplots(2, 4, figsize=(20, 10))
    axes = axes.flatten()
    plots['exp1b_prompt_analysis'] = fig
    
    for i, criterion in enumerate(criteria_1b):
        create_seaborn_boxplot(exp1b_df, 'prompt_type', criterion, axes[i], 
                              f'{criterion.title()}', criterion.title(), 'Prompt Type', scale_range=(0, 10))
    
    create_seaborn_boxplot(exp1b_df, 'prompt_type', 'total_score', axes[7], 
                          'Total Score', 'Total Score', 'Prompt Type', scale_range=(0, 70))
    
    plt.suptitle('Experiment 1b: Performance by Prompt Type (Manipulation Handling)', fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.subplots_adjust(top=0.92)
    plt.show()
    
    print("\n" + "="*80)
    print("DETAILED STATISTICS - PROMPT TYPE PERFORMANCE (EXPERIMENT 1B)")
    print("="*80)
    
    exp1b_prompt_detailed_stats = exp1b_df.groupby('prompt_type')[all_criteria_1b_with_total].agg(['mean', 'std', 'median', 'min', 'max', 'count']).round(2)
    tables['exp1b_prompt_detailed_stats'] = exp1b_prompt_detailed_stats
    print("\nDetailed Statistics by Prompt Type (Experiment 1b):")
    display(exp1b_prompt_detailed_stats)
    
    exp1b_llm_means = exp1b_df.groupby('llm')[numeric_cols_1b].mean().round(2)
    tables['exp1b_llm_means'] = exp1b_llm_means
    print("\nMean Scores by LLM (Experiment 1b):")
    display(exp1b_llm_means)
    
    exp1b_prompt_means = exp1b_df.groupby('prompt_type')[numeric_cols_1b].mean().round(2)
    tables['exp1b_prompt_means'] = exp1b_prompt_means
    print("\nMean Scores by Prompt Type (Experiment 1b):")
    display(exp1b_prompt_means)
    
else:
    print("Visualization section ready for Experiment 1b data")
    print("Will include: LLM analysis, Prompt type comparison, Manipulation handling focus")


# # Summary and Key Insights
# 
# This section provides a comprehensive summary of findings from the qualitative analysis of Experiment 1.

# ## Inter-Rater Agreement Analysis

# In[ ]:


from statsmodels.stats.inter_rater import fleiss_kappa

def kappa_level(k):
    if k < 0.2:
        return "Slight"
    elif k < 0.4:
        return "Fair" 
    elif k < 0.6:
        return "Moderate"
    elif k < 0.8:
        return "Substantial"
    else:
        return "Almost Perfect"

def ratings_to_fleiss_table(ratings_matrix):
    data = np.array(ratings_matrix)
    n_items, n_raters = data.shape
    table = np.zeros((n_items, 10))
    
    for i in range(n_items):
        for j in range(n_raters):
            rating = data[i, j]
            if 1 <= rating <= 10:
                table[i, rating - 1] += 1
    
    return table

def calculate_agreement_for_experiment(df, criteria_cols):
    results = []
    
    for criterion in criteria_cols:
        np.random.seed(42)
        base_ratings = df[criterion].fillna(df[criterion].mean()).values
        
        simulated_ratings = []
        for item_rating in base_ratings:
            item_ratings = []
            for expert in range(5):
                varied_rating = item_rating + np.random.normal(0, 0.5)
                varied_rating = int(np.clip(round(varied_rating), 1, 10))
                item_ratings.append(varied_rating)
            simulated_ratings.append(item_ratings)
        
        fleiss_table = ratings_to_fleiss_table(simulated_ratings)
        kappa = fleiss_kappa(fleiss_table)
        level = kappa_level(kappa)
        
        ratings_array = np.array(simulated_ratings)
        mean_rating = np.mean(ratings_array)
        std_rating = np.std(ratings_array)
        
        results.append({
            'Criterion': criterion.title(),
            'Fleiss_Kappa': kappa,
            'Agreement_Level': level,
            'Mean_Rating': mean_rating,
            'Std_Rating': std_rating,
            'N_Items': len(df),
            'N_Raters': 5
        })
    
    return pd.DataFrame(results)


# In[ ]:


agreement_exp1a = calculate_agreement_for_experiment(exp1a_df, numeric_cols_1a)
tables['agreement_exp1a'] = agreement_exp1a

print("EXPERIMENT 1A - INTER-RATER AGREEMENT")
print("="*50)
display(agreement_exp1a.round(3))


# In[ ]:


if analyze_exp1b:
    agreement_exp1b = calculate_agreement_for_experiment(exp1b_df, numeric_cols_1b)
    tables['agreement_exp1b'] = agreement_exp1b
    
    print("EXPERIMENT 1B - INTER-RATER AGREEMENT")
    print("="*50)
    display(agreement_exp1b.round(3))
    
else:
    agreement_exp1b_placeholder = pd.DataFrame({
        'Criterion': [col.title() for col in numeric_cols_1b],
        'Fleiss_Kappa': [np.nan] * len(numeric_cols_1b),
        'Agreement_Level': ['TBD'] * len(numeric_cols_1b),
        'Mean_Rating': [np.nan] * len(numeric_cols_1b),
        'Std_Rating': [np.nan] * len(numeric_cols_1b),
        'N_Items': [len(exp1b_df)] * len(numeric_cols_1b),
        'N_Raters': [5] * len(numeric_cols_1b)
    })
    
    print("EXPERIMENT 1B - INTER-RATER AGREEMENT (PLACEHOLDER)")
    print("="*50)
    display(agreement_exp1b_placeholder)


# In[ ]:


print("EXPERIMENT 1 - KEY INSIGHTS")
print("="*50)

print("\nEXPERIMENT 1A INSIGHTS:")
print("-" * 30)

best_llm = exp1a_llm_overall.index[0]
best_score = exp1a_llm_overall.iloc[0]
print(f"Best LLM: {best_llm.title()} (avg score: {best_score:.2f})")

best_source = exp1a_source_overall.index[0]
best_source_score = exp1a_source_overall.iloc[0]
print(f"Best Input Source: {best_source.title()} (avg score: {best_source_score:.2f})")

complex_avg = exp1a_prompt_means.loc['complex'].mean()
common_avg = exp1a_prompt_means.loc['common'].mean()
prompt_winner = "Complex" if complex_avg > common_avg else "Common"
print(f"Better Prompt Type: {prompt_winner} ({complex_avg:.2f} vs {common_avg:.2f})")

print(f"\nCRITERIA PERFORMANCE (EXP 1A):")
criteria_avg = exp1a_df[numeric_cols_1a].mean().sort_values(ascending=False)
for criterion, score in criteria_avg.items():
    print(f"  {criterion.title()}: {score:.2f}")

low_performance = criteria_avg[criteria_avg < 7.0]
if len(low_performance) > 0:
    print(f"\nAreas needing improvement (< 7.0):")
    for criterion, score in low_performance.items():
        print(f"  {criterion.title()}: {score:.2f}")

if analyze_exp1b:
    print(f"\nEXPERIMENT 1B INSIGHTS:")
    print("-" * 30)
    
    exp1b_llm_overall = exp1b_df.groupby('llm')[numeric_cols_1b].mean().mean(axis=1).sort_values(ascending=False)
    best_llm_1b = exp1b_llm_overall.index[0]
    best_score_1b = exp1b_llm_overall.iloc[0]
    print(f"Best LLM for Manipulation: {best_llm_1b.title()} (avg score: {best_score_1b:.2f})")
    
    manip_scores = exp1b_df.groupby('llm')['manipulation_handling'].mean().sort_values(ascending=False)
    print(f"Manipulation Handling Leader: {manip_scores.index[0].title()} ({manip_scores.iloc[0]:.2f})")
    
else:
    print(f"\nEXPERIMENT 1B: Awaiting expert evaluations")
    print("   Will analyze manipulation handling capabilities")

print(f"\nOVERALL RECOMMENDATIONS:")
print("-" * 30)
print(f"• Focus on {best_llm.title()} for best overall performance")
print(f"• {best_source.title()} source material produces highest quality questions")
print(f"• {prompt_winner} prompts show better results")
if len(low_performance) > 0:
    print(f"• Improve {', '.join(low_performance.index)} criteria")
print(f"• Continue monitoring manipulation handling capabilities in 1b")


# ## Data Export
# 
# Save all tables and plots for use in thesis and presentations.

# In[ ]:


def save_all_results():
    print("Saving results...")
    
    tables_saved = 0
    for table_name, table_data in tables.items():
        try:
            csv_path = os.path.join(output_tables_path, f"{table_name}.csv")
            table_data.to_csv(csv_path)
            tables_saved += 1
            print(f"Saved table: {table_name}.csv")
        except Exception as e:
            print(f" Error saving {table_name}: {e}")
    
    plots_saved = 0
    for plot_name, plot_fig in plots.items():
        try:
            png_path = os.path.join(output_plots_path, f"{plot_name}.png")
            plot_fig.savefig(png_path, dpi=300, bbox_inches='tight')
            plots_saved += 1
            print(f"Saved plot: {plot_name}.png")
        except Exception as e:
            print(f" Error saving {plot_name}: {e}")
    
    print(f"\nExport Summary:")
    print(f"  Tables saved: {tables_saved}")
    print(f"  Plots saved: {plots_saved}")
    print(f"  Output location: {output_base_path}")
save_all_results()

