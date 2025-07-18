#!/usr/bin/env python
# coding: utf-8

# # Notebook: Qualitative Evaluation (Supervisor vs. Staff Members) -- Experiment 1

# ## Initial Setup

# In[ ]:


import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display
import warnings
from statsmodels.stats.inter_rater import fleiss_kappa

warnings.filterwarnings('ignore')

# Plot configuration
plt.style.use('default')
sns.set_palette("Set2")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

# Display configuration
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 100)
pd.set_option('display.notebook_repr_html', True)

# Path configuration
BASE_PROJECT_PATH = os.path.abspath(os.path.join(os.getcwd(), "..", ".."))
expert_base_path = os.path.join(BASE_PROJECT_PATH, "20_experiments/60_analyses/csv/qualitative/exp1/experts")
hint_base_path = os.path.join(BASE_PROJECT_PATH, "20_experiments/60_analyses/csv/qualitative/exp1/hints")
output_base_path = os.path.join(BASE_PROJECT_PATH, "40_evaluation/exp1/qualitative")
output_tables_path = os.path.join(output_base_path, "tables")
output_plots_path = os.path.join(output_base_path, "plots")

for path in [output_tables_path, output_plots_path]:
    os.makedirs(path, exist_ok=True)

# Storage for results
tables = {}
plots = {}

print("Setup completed successfully")
print(f"Output tables: {output_tables_path}")
print(f"Output plots: {output_plots_path}")


# In[ ]:


# Utility Functions

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
        'anthropic': 'Anthropic', 'openai': 'OpenAI', 'google': 'Google', 'deepseek': 'DeepSeek',
        'common': 'Common', 'complex': 'Complex', 'script': 'Script', 'transcript': 'Transcript', 
        'tanenbaum': 'Tanenbaum', 'script_manipulated': 'Script (Manipulated)'
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

def load_supervisor_data():
    hint_exp1a = pd.read_csv(os.path.join(hint_base_path, "exp1a_hints.csv"))
    hint_exp1b = pd.read_csv(os.path.join(hint_base_path, "exp1b_hints.csv"))
    
    expert1_exp1a = pd.read_csv(os.path.join(expert_base_path, "expert_1", "exp1a.csv"))
    expert1_exp1b = pd.read_csv(os.path.join(expert_base_path, "expert_1", "exp1b.csv"))
    
    # Apply preliminary cleaning to Expert 1 data to handle special characters
    numeric_cols_1a_temp = ['relevance', 'clarity', 'answerability', 'challenging', 'value', 'language', 'correctness']
    numeric_cols_1b_temp = ['relevance', 'clarity', 'answerability', 'challenging', 'value', 'language', 'manipulation_handling']
    
    # Clean Expert 1 data before concatenation
    for col in numeric_cols_1a_temp:
        if col in expert1_exp1a.columns:
            expert1_exp1a[col] = expert1_exp1a[col].astype(str)
            invalid_values = ['??', '???', '?', '', ' ', 'nan', 'NaN', 'NULL', 'null', 
                             'None', 'NONE', 'n/a', 'N/A', '#N/A', '#NULL!', 
                             'undefined', 'UNDEFINED', '-', '--', '---']
            expert1_exp1a[col] = expert1_exp1a[col].replace(invalid_values, np.nan)
            expert1_exp1a[col] = expert1_exp1a[col].replace(r'^\s*[\?\-\#]*\s*$', np.nan, regex=True)
    
    for col in numeric_cols_1b_temp:
        if col in expert1_exp1b.columns:
            expert1_exp1b[col] = expert1_exp1b[col].astype(str)
            invalid_values = ['??', '???', '?', '', ' ', 'nan', 'NaN', 'NULL', 'null', 
                             'None', 'NONE', 'n/a', 'N/A', '#N/A', '#NULL!', 
                             'undefined', 'UNDEFINED', '-', '--', '---']
            expert1_exp1b[col] = expert1_exp1b[col].replace(invalid_values, np.nan)
            expert1_exp1b[col] = expert1_exp1b[col].replace(r'^\s*[\?\-\#]*\s*$', np.nan, regex=True)
    
    exp1a_df = pd.concat([expert1_exp1a, hint_exp1a[['llm', 'prompt_type']]], axis=1)
    exp1b_df = pd.concat([expert1_exp1b, hint_exp1b[['llm', 'prompt_type']]], axis=1)
    
    exp1a_df['experiment'] = 'exp1a'
    exp1b_df['experiment'] = 'exp1b'
    exp1b_df['input_source'] = exp1b_df['input_source'].replace('script', 'script_manipulated')
    
    return exp1a_df, exp1b_df

def load_staff_data():
    hint_exp1a = pd.read_csv(os.path.join(hint_base_path, "exp1a_hints.csv"))
    hint_exp1b = pd.read_csv(os.path.join(hint_base_path, "exp1b_hints.csv"))
    
    experts_data = {}
    for expert in [2, 3, 4, 5]:
        expert_key = f'expert_{expert}'
        
        exp1a_path = os.path.join(expert_base_path, expert_key, "exp1a.csv")
        exp1b_path = os.path.join(expert_base_path, expert_key, "exp1b.csv")
        
        if expert == 4 or expert == 2:
            exp1a_data = pd.read_csv(exp1a_path, sep=';', quotechar='"')
            exp1b_data = pd.read_csv(exp1b_path, sep=';', quotechar='"')
        else:
            exp1a_data = pd.read_csv(exp1a_path, quotechar='"', escapechar='\\')
            exp1b_data = pd.read_csv(exp1b_path, quotechar='"', escapechar='\\')
        
        experts_data[expert_key] = {'exp1a': exp1a_data, 'exp1b': exp1b_data}
        experts_data[expert_key]['exp1a']['expert'] = expert_key
        experts_data[expert_key]['exp1b']['expert'] = expert_key
    
    exp1a_combined = pd.concat([data['exp1a'] for data in experts_data.values()], ignore_index=True)
    exp1b_combined = pd.concat([data['exp1b'] for data in experts_data.values()], ignore_index=True)
    
    hint_multiplier = len(experts_data)
    exp1a_hints_extended = pd.concat([hint_exp1a[['llm', 'prompt_type']]] * hint_multiplier, ignore_index=True)
    exp1b_hints_extended = pd.concat([hint_exp1b[['llm', 'prompt_type']]] * hint_multiplier, ignore_index=True)
    
    exp1a_df = exp1a_combined.copy()
    exp1b_df = exp1b_combined.copy()
    
    for col in ['llm', 'prompt_type']:
        if col not in exp1a_df.columns:
            exp1a_df[col] = exp1a_hints_extended[col].values
        if col not in exp1b_df.columns:
            exp1b_df[col] = exp1b_hints_extended[col].values
    
    return exp1a_df, exp1b_df, experts_data

def clean_numeric_data(df, numeric_cols):
    for col in numeric_cols:
        if col in df.columns:
            # Convert to string first to handle all possible invalid values
            df[col] = df[col].astype(str)
            
            # Replace various invalid values with NaN
            invalid_values = ['??', '???', '?', '', ' ', 'nan', 'NaN', 'NULL', 'null', 
                             'None', 'NONE', 'n/a', 'N/A', '#N/A', '#NULL!', 
                             'undefined', 'UNDEFINED', '-', '--', '---']
            df[col] = df[col].replace(invalid_values, np.nan)
            
            # Also replace any string that contains only special characters or whitespace
            df[col] = df[col].replace(r'^\s*[\?\-\#]*\s*$', np.nan, regex=True)
            
            # Convert to numeric, any remaining non-numeric values become NaN
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Validate range (0-10 for rating scales)
            valid_data = df[col].dropna()
            if len(valid_data) > 0:
                out_of_range = valid_data[(valid_data < 0) | (valid_data > 10)]
                if len(out_of_range) > 0:
                    df.loc[(df[col] < 0) | (df[col] > 10), col] = np.nan
    return df

def calculate_fleiss_kappa(expert2_df, expert3_df, expert4_df, expert5_df, criteria_cols):
    results = []
    
    ids2 = set(expert2_df['sample_id'].astype(int))
    ids3 = set(expert3_df['sample_id'].astype(int))
    ids4 = set(expert4_df['sample_id'].astype(int)) 
    ids5 = set(expert5_df['sample_id'].astype(int))
    common_ids = sorted(list(ids2 & ids3 & ids4 & ids5))
    
    for criterion in criteria_cols:
        ratings = []
        for sample_id in common_ids:
            r2 = expert2_df[expert2_df['sample_id'] == sample_id][criterion].iloc[0]
            r3 = expert3_df[expert3_df['sample_id'] == sample_id][criterion].iloc[0]
            r4 = expert4_df[expert4_df['sample_id'] == sample_id][criterion].iloc[0] 
            r5 = expert5_df[expert5_df['sample_id'] == sample_id][criterion].iloc[0]
            
            def safe_convert(val):
                return np.nan if pd.isna(val) else float(val)
            
            r2_val, r3_val, r4_val, r5_val = map(safe_convert, [r2, r3, r4, r5])
            
            if all(not pd.isna(r) and 0 <= r <= 10 for r in [r2_val, r3_val, r4_val, r5_val]):
                ratings.append([int(r2_val), int(r3_val), int(r4_val), int(r5_val)])
        
        if len(ratings) >= 2:
            ratings_array = np.array(ratings)
            fleiss_table = np.zeros((len(ratings), 11))
            
            for i, item_ratings in enumerate(ratings):
                for rating in item_ratings:
                    fleiss_table[i, int(rating)] += 1
            
            kappa = fleiss_kappa(fleiss_table)
            
            level = ("Slight" if kappa < 0.2 else 
                    "Fair" if kappa < 0.4 else 
                    "Moderate" if kappa < 0.6 else 
                    "Substantial" if kappa < 0.8 else 
                    "Almost Perfect")
            
            results.append({
                'Criterion': criterion,
                'Fleiss_Kappa': round(kappa, 3),
                'Agreement_Level': level,
                'N_Items': len(ratings),
                'Mean_Rating': round(np.mean(ratings_array), 2),
                'Std_Rating': round(np.std(ratings_array), 2)
            })
    
    return pd.DataFrame(results)

print("Utility functions loaded successfully")


# ## Data Loading and Configuration

# In[ ]:


# Data Selection Configuration
USE_SUPERVISOR_DATA = True  # Set to False to use staff data (Experts 2-5)

# Load data based on configuration
if USE_SUPERVISOR_DATA:
    print("Loading SUPERVISOR data (Expert 1 - single rater)")
    exp1a_df, exp1b_df = load_supervisor_data()
    analysis_suffix = "supervisor"
    agreement_available = False
else:
    print("Loading STAFF data (Experts 2-5 - multiple raters with agreement analysis)")
    exp1a_df, exp1b_df, experts_data = load_staff_data()
    analysis_suffix = "staff" 
    agreement_available = True

# Define criteria columns
numeric_cols_1a = ['relevance', 'clarity', 'answerability', 'challenging', 'value', 'language', 'correctness']
numeric_cols_1b = ['relevance', 'clarity', 'answerability', 'challenging', 'value', 'language', 'manipulation_handling']

# Clean and prepare data
exp1a_df = clean_numeric_data(exp1a_df, numeric_cols_1a)
exp1b_df = clean_numeric_data(exp1b_df, numeric_cols_1b)

# Calculate total scores
exp1a_df['total_score'] = exp1a_df[numeric_cols_1a].sum(axis=1)
exp1b_df['total_score'] = exp1b_df[numeric_cols_1b].sum(axis=1)

# Data availability check
exp1a_filled = exp1a_df[numeric_cols_1a].notna().sum().sum()
exp1a_total = len(exp1a_df) * len(numeric_cols_1a)
exp1b_filled = exp1b_df[numeric_cols_1b].notna().sum().sum()
exp1b_total = len(exp1b_df) * len(numeric_cols_1b)

analyze_exp1b = exp1b_filled > 0

print(f"\nData loaded successfully!")
print(f"Experiment 1a: {len(exp1a_df)} samples, {100*exp1a_filled/exp1a_total:.1f}% completion")
print(f"Experiment 1b: {len(exp1b_df)} samples, {100*exp1b_filled/exp1b_total:.1f}% completion")
print(f"Analysis suffix: {analysis_suffix}")

print(f"\nDistribution:")
print(f"  LLMs: {list(exp1a_df['llm'].unique())}")
print(f"  Prompt Types: {list(exp1a_df['prompt_type'].unique())}")
print(f"  Input Sources (1a): {list(exp1a_df['input_source'].unique())}")
if analyze_exp1b:
    print(f"  Input Sources (1b): {list(exp1b_df['input_source'].unique())}")


# # Experiment 1a: Original Content Analysis
# 
# Analysis of LLM question generation quality using original source materials.

# In[ ]:


print("EXPERIMENT 1A - DESCRIPTIVE STATISTICS")
print("="*60)

criteria = numeric_cols_1a + ['total_score']

# Overall statistics
exp1a_stats = exp1a_df[numeric_cols_1a].describe().round(2)
tables[f'exp1a_overall_stats_{analysis_suffix}'] = exp1a_stats
print("\nOverall Statistics:")
display(exp1a_stats)

# Statistics by LLM
exp1a_llm_stats = exp1a_df.groupby('llm')[criteria].agg(['mean', 'std', 'median', 'count']).round(2)
tables[f'exp1a_llm_stats_{analysis_suffix}'] = exp1a_llm_stats
print("\nStatistics by LLM:")
display(exp1a_llm_stats)

# LLM ranking
exp1a_llm_means = exp1a_df.groupby('llm')[numeric_cols_1a].mean().round(2)
exp1a_llm_overall = exp1a_llm_means.mean(axis=1).sort_values(ascending=False)
tables[f'exp1a_llm_ranking_{analysis_suffix}'] = exp1a_llm_overall

print("\nOverall LLM Ranking:")
for i, (llm, score) in enumerate(exp1a_llm_overall.items(), 1):
    print(f"{i}. {llm.title()}: {score:.2f}")

# Statistics by Input Source
exp1a_source_stats = exp1a_df.groupby('input_source')[criteria].agg(['mean', 'std', 'median', 'count']).round(2)
tables[f'exp1a_source_stats_{analysis_suffix}'] = exp1a_source_stats
print("\nStatistics by Input Source:")
display(exp1a_source_stats)

# Statistics by Prompt Type
exp1a_prompt_stats = exp1a_df.groupby('prompt_type')[criteria].agg(['mean', 'std', 'median', 'count']).round(2)
tables[f'exp1a_prompt_stats_{analysis_suffix}'] = exp1a_prompt_stats
print("\nStatistics by Prompt Type:")
display(exp1a_prompt_stats)


# In[ ]:


# LLM Performance Visualization
fig, axes = plt.subplots(4, 2, figsize=(14, 20))
axes = axes.flatten()
plots[f'exp1a_llm_analysis_{analysis_suffix}'] = fig

for i, criterion in enumerate(numeric_cols_1a):
    create_seaborn_boxplot(exp1a_df, 'llm', criterion, axes[i], 
                          f'{criterion.title()}', criterion.title(), 'LLM', scale_range=(0, 10))

create_seaborn_boxplot(exp1a_df, 'llm', 'total_score', axes[7], 
                      'Total Score', 'Total Score', 'LLM', scale_range=(0, 70))

plt.suptitle('Experiment 1a: LLM Performance across all Criteria', fontsize=16, fontweight='bold', y=0.98)
plt.tight_layout()
plt.subplots_adjust(top=0.95)
plt.show()


# In[ ]:


# Input Source Analysis
fig, axes = plt.subplots(4, 2, figsize=(14, 20))
axes = axes.flatten()
plots[f'exp1a_source_analysis_{analysis_suffix}'] = fig

for i, criterion in enumerate(numeric_cols_1a):
    create_seaborn_boxplot(exp1a_df, 'input_source', criterion, axes[i], 
                          f'{criterion.title()}', criterion.title(), 'Input Source', scale_range=(0, 10))

create_seaborn_boxplot(exp1a_df, 'input_source', 'total_score', axes[7], 
                      'Total Score', 'Total Score', 'Input Source', scale_range=(0, 70))

plt.suptitle('Experiment 1a: Performance by Input Source', fontsize=16, fontweight='bold', y=0.98)
plt.tight_layout()
plt.subplots_adjust(top=0.95)
plt.show()

# Prompt Type Analysis
fig, axes = plt.subplots(2, 4, figsize=(20, 10))
axes = axes.flatten()
plots[f'exp1a_prompt_analysis_{analysis_suffix}'] = fig

for i, criterion in enumerate(numeric_cols_1a):
    create_seaborn_boxplot(exp1a_df, 'prompt_type', criterion, axes[i], 
                          f'{criterion.title()}', criterion.title(), 'Prompt Type', scale_range=(0, 10))

create_seaborn_boxplot(exp1a_df, 'prompt_type', 'total_score', axes[7], 
                      'Total Score', 'Total Score', 'Prompt Type', scale_range=(0, 70))

plt.suptitle('Experiment 1a: Performance by Prompt Type', fontsize=16, fontweight='bold', y=0.98)
plt.tight_layout()
plt.subplots_adjust(top=0.92)
plt.show()

# Prompt Type Comparison
exp1a_prompt_means = exp1a_df.groupby('prompt_type')[numeric_cols_1a].mean().round(2)
tables[f'exp1a_prompt_means_{analysis_suffix}'] = exp1a_prompt_means

if 'complex' in exp1a_prompt_means.index and 'common' in exp1a_prompt_means.index:
    prompt_diff = exp1a_prompt_means.loc['complex'] - exp1a_prompt_means.loc['common']
    print("\nComplex vs Common Prompt Difference:")
    for criterion, diff in prompt_diff.items():
        direction = "higher" if diff > 0 else "lower"
        print(f"  {criterion.title()}: {diff:+.2f} ({direction} for complex)")


# In[ ]:


# Total Score Heatmaps
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
plots[f'exp1a_total_score_heatmaps_{analysis_suffix}'] = fig

# Heatmap 1: Total Score by LLM vs Input Source
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

sns.heatmap(heatmap_mean, annot=annot_matrix, fmt='', cmap='RdYlBu_r',
            center=heatmap_mean.mean().mean(), square=True, linewidths=0.5,
            cbar_kws={'shrink': 0.8, 'label': 'Total Score'}, annot_kws={'size': 10, 'weight': 'bold'},
            xticklabels=source_labels, yticklabels=llm_labels, ax=ax1)

ax1.set_title('Total Score (LLM vs Input Source)\nValues: Mean (Std) | Scale: 0-70 points', 
             fontsize=14, fontweight='bold', pad=20)
ax1.set_xlabel('Input Source', fontsize=12, fontweight='bold')
ax1.set_ylabel('LLM', fontsize=12, fontweight='bold')

# Heatmap 2: Total Score by LLM vs Prompt Type
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

sns.heatmap(heatmap_mean_prompt, annot=annot_matrix_prompt, fmt='', cmap='RdYlBu_r',
            center=heatmap_mean_prompt.mean().mean(), square=True, linewidths=0.5,
            cbar_kws={'shrink': 0.8, 'label': 'Total Score'}, annot_kws={'size': 10, 'weight': 'bold'},
            xticklabels=prompt_labels, yticklabels=llm_labels, ax=ax2)

ax2.set_title('Total Score (LLM vs Prompt Type)\nValues: Mean (Std) | Scale: 0-70 points', 
             fontsize=14, fontweight='bold', pad=20)
ax2.set_xlabel('Prompt Type', fontsize=12, fontweight='bold')
ax2.set_ylabel('LLM', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.show()

# Correctness Heatmaps
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
plots[f'exp1a_correctness_heatmaps_{analysis_suffix}'] = fig

# Correctness by LLM vs Input Source
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

sns.heatmap(correctness_heatmap_mean, annot=correctness_annot_matrix, fmt='', cmap='RdYlBu_r',
            center=correctness_heatmap_mean.mean().mean(), square=True, linewidths=0.5,
            cbar_kws={'shrink': 0.8, 'label': 'Correctness Score'}, annot_kws={'size': 10, 'weight': 'bold'},
            xticklabels=[l.title() for l in correctness_heatmap_mean.columns], 
            yticklabels=[l.title() for l in correctness_heatmap_mean.index], ax=ax1)

ax1.set_title('Correctness Score (LLM vs Input Source)\nValues: Mean (Std) | Scale: 0-10 points', 
             fontsize=14, fontweight='bold', pad=20)
ax1.set_xlabel('Input Source', fontsize=12, fontweight='bold')
ax1.set_ylabel('LLM', fontsize=12, fontweight='bold')

# Correctness by LLM vs Prompt Type
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

sns.heatmap(correctness_prompt_heatmap_mean, annot=correctness_prompt_annot_matrix, fmt='', cmap='RdYlBu_r',
            center=correctness_prompt_heatmap_mean.mean().mean(), square=True, linewidths=0.5,
            cbar_kws={'shrink': 0.8, 'label': 'Correctness Score'}, annot_kws={'size': 10, 'weight': 'bold'},
            xticklabels=[l.title() for l in correctness_prompt_heatmap_mean.columns], 
            yticklabels=[l.title() for l in correctness_prompt_heatmap_mean.index], ax=ax2)

ax2.set_title('Correctness Score (LLM vs Prompt Type)\nValues: Mean (Std) | Scale: 0-10 points', 
             fontsize=14, fontweight='bold', pad=20)
ax2.set_xlabel('Prompt Type', fontsize=12, fontweight='bold')
ax2.set_ylabel('LLM', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.show()

# Store detailed statistics tables
exp1a_llm_source_combinations = exp1a_df.groupby(['llm', 'input_source'])['total_score'].agg(['mean', 'std', 'median', 'min', 'max', 'count']).round(2)
tables[f'exp1a_llm_source_combinations_{analysis_suffix}'] = exp1a_llm_source_combinations

exp1a_llm_prompt_combinations = exp1a_df.groupby(['llm', 'prompt_type'])['total_score'].agg(['mean', 'std', 'median', 'min', 'max', 'count']).round(2)
tables[f'exp1a_llm_prompt_combinations_{analysis_suffix}'] = exp1a_llm_prompt_combinations

correctness_llm_source_stats = exp1a_df.groupby(['llm', 'input_source'])['correctness'].agg(['mean', 'std', 'median', 'min', 'max', 'count']).round(2)
tables[f'exp1a_correctness_llm_source_stats_{analysis_suffix}'] = correctness_llm_source_stats

correctness_llm_prompt_stats = exp1a_df.groupby(['llm', 'prompt_type'])['correctness'].agg(['mean', 'std', 'median', 'min', 'max', 'count']).round(2)
tables[f'exp1a_correctness_llm_prompt_stats_{analysis_suffix}'] = correctness_llm_prompt_stats


# # Experiment 1b: Manipulated Content Analysis
# 
# Analysis of LLM robustness to content manipulation.

# In[ ]:


if analyze_exp1b:
    print("EXPERIMENT 1B - DESCRIPTIVE STATISTICS")
    print("="*60)
    
    criteria_1b = numeric_cols_1b + ['total_score']
    
    # Overall statistics
    exp1b_stats = exp1b_df[numeric_cols_1b].describe().round(2)
    tables[f'exp1b_overall_stats_{analysis_suffix}'] = exp1b_stats
    print("\nOverall Statistics:")
    display(exp1b_stats)
    
    # Statistics by LLM
    exp1b_llm_stats = exp1b_df.groupby('llm')[criteria_1b].agg(['mean', 'std', 'median', 'count']).round(2)
    tables[f'exp1b_llm_stats_{analysis_suffix}'] = exp1b_llm_stats
    print("\nStatistics by LLM:")
    display(exp1b_llm_stats)
    
    # LLM Performance Visualization
    fig, axes = plt.subplots(4, 2, figsize=(14, 20))
    axes = axes.flatten()
    plots[f'exp1b_llm_analysis_{analysis_suffix}'] = fig
    
    for i, criterion in enumerate(numeric_cols_1b):
        display_title = 'Manipulation Handling' if criterion == 'manipulation_handling' else criterion.title()
        create_seaborn_boxplot(exp1b_df, 'llm', criterion, axes[i], 
                              display_title, display_title, 'LLM', scale_range=(0, 10))
    
    create_seaborn_boxplot(exp1b_df, 'llm', 'total_score', axes[7], 
                          'Total Score', 'Total Score', 'LLM', scale_range=(0, 70))
    
    plt.suptitle('Experiment 1b: LLM Performance (Manipulation Handling)', fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.subplots_adjust(top=0.95)
    plt.show()
    
    # Prompt Type Analysis
    fig, axes = plt.subplots(4, 2, figsize=(14, 20))
    axes = axes.flatten()
    plots[f'exp1b_prompt_analysis_{analysis_suffix}'] = fig
    
    for i, criterion in enumerate(numeric_cols_1b):
        display_title = 'Manipulation Handling' if criterion == 'manipulation_handling' else criterion.title()
        create_seaborn_boxplot(exp1b_df, 'prompt_type', criterion, axes[i], 
                              display_title, display_title, 'Prompt Type', scale_range=(0, 10))
    
    create_seaborn_boxplot(exp1b_df, 'prompt_type', 'total_score', axes[7], 
                          'Total Score', 'Total Score', 'Prompt Type', scale_range=(0, 70))
    
    plt.suptitle('Experiment 1b: Performance by Prompt Type', fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.subplots_adjust(top=0.95)
    plt.show()
    
    # LLM Rankings
    exp1b_llm_means = exp1b_df.groupby('llm')[numeric_cols_1b].mean().round(2)
    tables[f'exp1b_llm_means_{analysis_suffix}'] = exp1b_llm_means
    
    total_score_ranking = exp1b_df.groupby('llm')['total_score'].mean().sort_values(ascending=False)
    manipulation_ranking = exp1b_df.groupby('llm')['manipulation_handling'].mean().sort_values(ascending=False)
    
    print("\nLLM Rankings (Experiment 1b):")
    print("\nBy Total Score:")
    for i, (llm, score) in enumerate(total_score_ranking.items(), 1):
        print(f"{i}. {llm.title()}: {score:.2f}/70")
    
    print("\nBy Manipulation Handling:")
    for i, (llm, score) in enumerate(manipulation_ranking.items(), 1):
        print(f"{i}. {llm.title()}: {score:.2f}/10")
    
    # Store additional statistics
    exp1b_prompt_stats = exp1b_df.groupby('prompt_type')[criteria_1b].agg(['mean', 'std', 'median', 'count']).round(2)
    tables[f'exp1b_prompt_stats_{analysis_suffix}'] = exp1b_prompt_stats
    
    exp1b_llm_detailed_stats = exp1b_df.groupby('llm')[criteria_1b].agg(['mean', 'std', 'median', 'min', 'max', 'count']).round(2)
    tables[f'exp1b_llm_detailed_stats_{analysis_suffix}'] = exp1b_llm_detailed_stats
    
else:
    print("EXPERIMENT 1B - DATA NOT AVAILABLE")
    print("="*60)
    print(f"Experiment 1b analysis will be available once expert evaluations are completed.")
    print(f"Current completion: {100*exp1b_filled/exp1b_total:.1f}%")
    print(f"Structure: {len(exp1b_df)} samples ready for analysis")


# # Inter-Rater Agreement Analysis
# 
# **Note:** Agreement analysis is only available for staff data (Experts 2-5).

# In[ ]:


if agreement_available:
    print("INTER-RATER AGREEMENT ANALYSIS (Fleiss' Kappa)")
    print("="*60)
    
    # Experiment 1a Agreement
    print("\nExperiment 1a Agreement (Experts 2, 3, 4, 5):")
    agreement_exp1a = calculate_fleiss_kappa(
        experts_data['expert_2']['exp1a'],
        experts_data['expert_3']['exp1a'],
        experts_data['expert_4']['exp1a'], 
        experts_data['expert_5']['exp1a'],
        numeric_cols_1a
    )
    tables[f'agreement_exp1a_{analysis_suffix}'] = agreement_exp1a
    display(agreement_exp1a.round(3))
    
    if not agreement_exp1a.empty:
        valid_kappas = agreement_exp1a['Fleiss_Kappa'].dropna()
        if len(valid_kappas) > 0:
            avg_kappa = valid_kappas.mean()
            
            level = ("Slight" if avg_kappa < 0.2 else 
                    "Fair" if avg_kappa < 0.4 else 
                    "Moderate" if avg_kappa < 0.6 else 
                    "Substantial" if avg_kappa < 0.8 else 
                    "Almost Perfect")
            
            print(f"\nOverall Agreement: K = {avg_kappa:.3f} ({level})")
            
            best_criterion = agreement_exp1a.loc[agreement_exp1a['Fleiss_Kappa'].idxmax()]
            worst_criterion = agreement_exp1a.loc[agreement_exp1a['Fleiss_Kappa'].idxmin()]
            
            print(f"Best agreement: {best_criterion['Criterion']} (K = {best_criterion['Fleiss_Kappa']:.3f})")
            print(f"Worst agreement: {worst_criterion['Criterion']} (K = {worst_criterion['Fleiss_Kappa']:.3f})")
    
    # Check if Experiment 1b has sufficient data for agreement analysis
    # exp1b_has_enough_data = False
    # if 'experts_data' in locals():
    #     total_filled = 0
    #     for expert_key in ['expert_2', 'expert_3', 'expert_4', 'expert_5']:
    #         if expert_key in experts_data:
    #             total_filled += experts_data[expert_key]['exp1b'][numeric_cols_1b].notna().sum().sum()
    #     exp1b_has_enough_data = total_filled > 50
    
    # if exp1b_has_enough_data:
    #     print("\n" + "-"*40)
    #     print("Experiment 1b Agreement (Experts 2, 3, 4, 5):")
    #     agreement_exp1b = calculate_fleiss_kappa(
    #         experts_data['expert_2']['exp1b'],
    #         experts_data['expert_3']['exp1b'],
    #         experts_data['expert_4']['exp1b'], 
    #         experts_data['expert_5']['exp1b'],
    #         numeric_cols_1b
    #     )
    #     tables[f'agreement_exp1b_{analysis_suffix}'] = agreement_exp1b
    #     display(agreement_exp1b.round(3))
        
    #     if not agreement_exp1b.empty:
    #         valid_kappas_1b = agreement_exp1b['Fleiss_Kappa'].dropna()
    #         if len(valid_kappas_1b) > 0:
    #             avg_kappa_1b = valid_kappas_1b.mean()
    #             level_1b = ("Slight" if avg_kappa_1b < 0.2 else 
    #                        "Fair" if avg_kappa_1b < 0.4 else 
    #                        "Moderate" if avg_kappa_1b < 0.6 else 
    #                        "Substantial" if avg_kappa_1b < 0.8 else 
    #                        "Almost Perfect")
    #             print(f"\nOverall Agreement (1b): K = {avg_kappa_1b:.3f} ({level_1b})")
    # else:
    #     print("\n" + "-"*40)
    #     print("Experiment 1b Agreement: Insufficient data for analysis")
    
    # Expert Comparison
    print("\n" + "="*60)
    print("EXPERT COMPARISON")
    print("="*60)
    
    expert_means_1a = {}
    for expert_key in ['expert_2', 'expert_3', 'expert_4', 'expert_5']:
        if expert_key in experts_data:
            expert_means_1a[expert_key] = experts_data[expert_key]['exp1a'][numeric_cols_1a].mean()
    
    if expert_means_1a:
        comparison_df_1a = pd.DataFrame(expert_means_1a).T
        comparison_df_1a['Overall_Mean'] = comparison_df_1a.mean(axis=1)
        comparison_df_1a = comparison_df_1a.round(3)
        tables[f'expert_comparison_exp1a_{analysis_suffix}'] = comparison_df_1a
        
        print("\nMean Ratings by Expert (Experiment 1a):")
        display(comparison_df_1a)
        
        expert_ranking = comparison_df_1a['Overall_Mean'].sort_values(ascending=False)
        print(f"\nExpert Ranking:")
        for i, (expert, score) in enumerate(expert_ranking.items(), 1):
            print(f"{i}. {expert}: {score:.3f}")

else:
    print("INTER-RATER AGREEMENT ANALYSIS")
    print("="*60)
    print("Agreement analysis not available for supervisor data.")
    print("Switch to staff data (USE_SUPERVISOR_DATA = False) to enable agreement analysis.")


# In[ ]:


if agreement_available:
    print("COMPREHENSIVE INTER-RATER AGREEMENT ANALYSIS")
    print("="*70)
    
    # Function to calculate agreement between all available experts
    def calculate_comprehensive_fleiss_kappa(experts_data, experiment, criteria_cols):
        results = []
        
        # Get all available expert dataframes for the experiment
        expert_dfs = {}
        for expert_key in ['expert_1', 'expert_2', 'expert_3', 'expert_4', 'expert_5']:
            if expert_key in experts_data and experiment in experts_data[expert_key]:
                expert_dfs[expert_key] = experts_data[expert_key][experiment]
        
        # Add supervisor data if we're in staff mode
        if experiment == 'exp1a':
            supervisor_exp1a, _ = load_supervisor_data()
            expert_dfs['expert_1'] = supervisor_exp1a
        elif experiment == 'exp1b':
            _, supervisor_exp1b = load_supervisor_data()
            expert_dfs['expert_1'] = supervisor_exp1b
        
        # Find common sample IDs across all experts
        if len(expert_dfs) < 2:
            return pd.DataFrame()
        
        common_ids = None
        for expert_key, df in expert_dfs.items():
            if 'sample_id' in df.columns:
                ids = set(df['sample_id'].astype(int))
                if common_ids is None:
                    common_ids = ids
                else:
                    common_ids = common_ids & ids
        
        if not common_ids:
            return pd.DataFrame()
        
        common_ids = sorted(list(common_ids))
        expert_names = sorted(expert_dfs.keys())
        
        print(f"\nAnalyzing {experiment.upper()} with experts: {expert_names}")
        print(f"Common samples: {len(common_ids)}")
        
        for criterion in criteria_cols:
            ratings = []
            for sample_id in common_ids:
                sample_ratings = []
                valid_sample = True
                
                for expert_key in expert_names:
                    df = expert_dfs[expert_key]
                    if sample_id in df['sample_id'].values:
                        rating = df[df['sample_id'] == sample_id][criterion].iloc[0]
                        rating_val = np.nan if pd.isna(rating) else float(rating)
                        
                        if pd.isna(rating_val) or rating_val < 0 or rating_val > 10:
                            valid_sample = False
                            break
                        sample_ratings.append(int(rating_val))
                    else:
                        valid_sample = False
                        break
                
                if valid_sample and len(sample_ratings) == len(expert_names):
                    ratings.append(sample_ratings)
            
            if len(ratings) >= 2:
                ratings_array = np.array(ratings)
                n_raters = len(expert_names)
                fleiss_table = np.zeros((len(ratings), 11))
                
                for i, item_ratings in enumerate(ratings):
                    for rating in item_ratings:
                        fleiss_table[i, int(rating)] += 1
                
                kappa = fleiss_kappa(fleiss_table)
                
                level = ("Slight" if kappa < 0.2 else 
                        "Fair" if kappa < 0.4 else 
                        "Moderate" if kappa < 0.6 else 
                        "Substantial" if kappa < 0.8 else 
                        "Almost Perfect")
                
                results.append({
                    'Criterion': criterion,
                    'Fleiss_Kappa': round(kappa, 3),
                    'Agreement_Level': level,
                    'N_Items': len(ratings),
                    'N_Raters': n_raters,
                    'Mean_Rating': round(np.mean(ratings_array), 2),
                    'Std_Rating': round(np.std(ratings_array), 2),
                    'Experts': ', '.join(expert_names)
                })
        
        return pd.DataFrame(results)
    
    # Calculate comprehensive agreement for Experiment 1a
    print("\n" + "="*70)
    print("ALL EXPERTS AGREEMENT ANALYSIS (Including Supervisor)")
    print("="*70)
    
    comprehensive_agreement_exp1a = calculate_comprehensive_fleiss_kappa(experts_data, 'exp1a', numeric_cols_1a)
    
    if not comprehensive_agreement_exp1a.empty:
        tables[f'comprehensive_agreement_exp1a_{analysis_suffix}'] = comprehensive_agreement_exp1a
        print("\nExperiment 1a - All Available Experts Agreement:")
        display(comprehensive_agreement_exp1a[['Criterion', 'Fleiss_Kappa', 'Agreement_Level', 'N_Items', 'N_Raters']].round(3))
        
        # Summary statistics for comprehensive agreement
        valid_kappas_comp = comprehensive_agreement_exp1a['Fleiss_Kappa'].dropna()
        if len(valid_kappas_comp) > 0:
            avg_kappa_comp = valid_kappas_comp.mean()
            level_comp = ("Slight" if avg_kappa_comp < 0.2 else 
                         "Fair" if avg_kappa_comp < 0.4 else 
                         "Moderate" if avg_kappa_comp < 0.6 else 
                         "Substantial" if avg_kappa_comp < 0.8 else 
                         "Almost Perfect")
            
            print(f"\nComprehensive Agreement Summary (All Experts):")
            print(f"  Average K: {avg_kappa_comp:.3f} ({level_comp})")
            print(f"  Experts included: {comprehensive_agreement_exp1a['Experts'].iloc[0]}")
            print(f"  Number of raters: {comprehensive_agreement_exp1a['N_Raters'].iloc[0]}")
            
            # Compare with staff-only agreement
            if 'agreement_exp1a' in locals() and not agreement_exp1a.empty:
                staff_avg_kappa = agreement_exp1a['Fleiss_Kappa'].dropna().mean()
                kappa_diff = avg_kappa_comp - staff_avg_kappa
                print(f"\nAgreement Comparison:")
                print(f"  Staff only (Experts 2-5): K = {staff_avg_kappa:.3f}")
                print(f"  All experts (1-5): K = {avg_kappa_comp:.3f}")
                print(f"  Difference: {kappa_diff:+.3f} ({'Higher' if kappa_diff > 0 else 'Lower'} with all experts)")
    
    # Check for Experiment 1b comprehensive agreement
    if analyze_exp1b:
        comprehensive_agreement_exp1b = calculate_comprehensive_fleiss_kappa(experts_data, 'exp1b', numeric_cols_1b)
        
        if not comprehensive_agreement_exp1b.empty:
            tables[f'comprehensive_agreement_exp1b_{analysis_suffix}'] = comprehensive_agreement_exp1b
            print("\n" + "-"*50)
            print("Experiment 1b - All Available Experts Agreement:")
            display(comprehensive_agreement_exp1b[['Criterion', 'Fleiss_Kappa', 'Agreement_Level', 'N_Items', 'N_Raters']].round(3))
            
            valid_kappas_comp_1b = comprehensive_agreement_exp1b['Fleiss_Kappa'].dropna()
            if len(valid_kappas_comp_1b) > 0:
                avg_kappa_comp_1b = valid_kappas_comp_1b.mean()
                level_comp_1b = ("Slight" if avg_kappa_comp_1b < 0.2 else 
                               "Fair" if avg_kappa_comp_1b < 0.4 else 
                               "Moderate" if avg_kappa_comp_1b < 0.6 else 
                               "Substantial" if avg_kappa_comp_1b < 0.8 else 
                               "Almost Perfect")
                
                print(f"\nComprehensive Agreement Summary (Exp 1b - All Experts):")
                print(f"  Average K: {avg_kappa_comp_1b:.3f} ({level_comp_1b})")
                print(f"  Experts included: {comprehensive_agreement_exp1b['Experts'].iloc[0]}")
        else:
            print("\n" + "-"*50)
            print("Experiment 1b - Insufficient data for comprehensive agreement analysis")
    
    print("\n" + "="*70)
    print("STAFF-ONLY AGREEMENT ANALYSIS (Experts 2-5)")
    print("="*70)


# # Key Insights and Summary

# In[ ]:


print("EXPERIMENT 1 - COMPREHENSIVE INSIGHTS")
print("="*60)

print(f"\nData Source: {analysis_suffix.title()}")
print(f"Analysis Type: {'With inter-rater agreement' if agreement_available else 'Single rater evaluation'}")

print("\nEXPERIMENT 1A INSIGHTS:")
print("-" * 30)

# Best performing elements
if 'exp1a_llm_overall' in locals():
    best_llm = exp1a_llm_overall.index[0]
    best_llm_score = exp1a_llm_overall.iloc[0]
    print(f"Best LLM: {best_llm.title()} (avg score: {best_llm_score:.2f})")

# Source performance
exp1a_source_overall = exp1a_df.groupby('input_source')['total_score'].mean().sort_values(ascending=False)
if len(exp1a_source_overall) > 0:
    best_source = exp1a_source_overall.index[0]
    best_source_score = exp1a_source_overall.iloc[0]
    print(f"Best Input Source: {best_source.title()} (avg score: {best_source_score:.2f})")

# Prompt comparison
if 'exp1a_prompt_means' in locals() and len(exp1a_prompt_means) >= 2:
    prompt_avg_scores = exp1a_prompt_means.mean(axis=1)
    if 'complex' in prompt_avg_scores.index and 'common' in prompt_avg_scores.index:
        complex_avg = prompt_avg_scores['complex']
        common_avg = prompt_avg_scores['common']
        prompt_winner = "Complex" if complex_avg > common_avg else "Common"
        print(f"Better Prompt Type: {prompt_winner} ({complex_avg:.2f} vs {common_avg:.2f})")

# Criteria performance
criteria_avg = exp1a_df[numeric_cols_1a].mean().sort_values(ascending=False)
print(f"\nCriteria Performance (Exp 1a):")
for criterion, score in criteria_avg.items():
    print(f"  {criterion.title()}: {score:.2f}")

# Areas for improvement
low_performance = criteria_avg[criteria_avg < 7.0]
if len(low_performance) > 0:
    print(f"\nAreas needing improvement (< 7.0):")
    for criterion, score in low_performance.items():
        print(f"  {criterion.title()}: {score:.2f}")

# Correctness insights
correctness_by_llm = exp1a_df.groupby('llm')['correctness'].mean().sort_values(ascending=False)
correctness_by_source = exp1a_df.groupby('input_source')['correctness'].mean().sort_values(ascending=False)

print(f"\nCorrectness Insights:")
if len(correctness_by_llm) > 0:
    print(f"  Best LLM for correctness: {correctness_by_llm.index[0].title()} ({correctness_by_llm.iloc[0]:.2f})")
if len(correctness_by_source) > 0:
    print(f"  Best source for correctness: {correctness_by_source.index[0].title()} ({correctness_by_source.iloc[0]:.2f})")

# Best combinations
if len(exp1a_df) > 0:
    best_llm_source_combo = exp1a_df.groupby(['llm', 'input_source'])['correctness'].mean()
    if len(best_llm_source_combo) > 0:
        best_combo = best_llm_source_combo.idxmax()
        best_combo_score = best_llm_source_combo.max()
        print(f"  Best LLM-Source combo: {best_combo[0].title()} + {best_combo[1].title()} ({best_combo_score:.2f})")

if analyze_exp1b:
    print(f"\nEXPERIMENT 1B INSIGHTS:")
    print("-" * 30)
    
    exp1b_llm_overall = exp1b_df.groupby('llm')[numeric_cols_1b].mean().mean(axis=1).sort_values(ascending=False)
    if len(exp1b_llm_overall) > 0:
        best_llm_1b = exp1b_llm_overall.index[0]
        best_score_1b = exp1b_llm_overall.iloc[0]
        print(f"Best LLM for manipulation: {best_llm_1b.title()} (avg score: {best_score_1b:.2f})")
    
    manip_scores = exp1b_df.groupby('llm')['manipulation_handling'].mean().sort_values(ascending=False)
    if len(manip_scores) > 0:
        print(f"Manipulation handling leader: {manip_scores.index[0].title()} ({manip_scores.iloc[0]:.2f})")
    
    # Robustness analysis
    criteria_avg_1b = exp1b_df[numeric_cols_1b].mean().sort_values(ascending=False)
    print(f"\nCriteria Performance (Exp 1b):")
    for criterion, score in criteria_avg_1b.items():
        display_name = 'Manipulation Handling' if criterion == 'manipulation_handling' else criterion.title()
        print(f"  {display_name}: {score:.2f}")
else:
    print(f"\nEXPERIMENT 1B: Awaiting expert evaluations")
    print("   Will analyze manipulation handling capabilities")

if agreement_available and 'agreement_exp1a' in locals() and not agreement_exp1a.empty:
    print(f"\nINTER-RATER AGREEMENT:")
    print("-" * 30)
    valid_kappas = agreement_exp1a['Fleiss_Kappa'].dropna()
    if len(valid_kappas) > 0:
        avg_kappa = valid_kappas.mean()
        level = ("Slight" if avg_kappa < 0.2 else 
                "Fair" if avg_kappa < 0.4 else 
                "Moderate" if avg_kappa < 0.6 else 
                "Substantial" if avg_kappa < 0.8 else 
                "Almost Perfect")
        print(f"Average agreement: K = {avg_kappa:.3f} ({level})")

print(f"\nOVERALL RECOMMENDATIONS:")
print("-" * 30)
if 'best_llm' in locals():
    print(f"• Focus on {best_llm.title()} for best overall performance")
if 'best_source' in locals():
    print(f"• {best_source.title()} source material produces highest quality questions")
if 'prompt_winner' in locals():
    print(f"• {prompt_winner} prompts show better results")
if len(low_performance) > 0:
    print(f"• Improve {', '.join(low_performance.index)} criteria")
if analyze_exp1b:
    print(f"• Monitor manipulation handling capabilities in ongoing evaluations")
else:
    print(f"• Continue with Experiment 1b evaluations for robustness analysis")


# ## Data Export
# 
# Save all tables and plots for thesis and presentations.

# In[ ]:


def save_all_results():
    print("Saving results...")
    
    # Determine prefix based on data source
    prefix = "supervisor_" if USE_SUPERVISOR_DATA else "staff_"
    
    tables_saved = 0
    for table_name, table_data in tables.items():
        # Remove suffix from table_name if it exists
        clean_name = table_name.replace(f"_{analysis_suffix}", "")
        csv_path = os.path.join(output_tables_path, f"{prefix}{table_name}.csv")
        table_data.to_csv(csv_path)
        tables_saved += 1
        print(f"Saved table: {prefix}{clean_name}.csv")
    
    plots_saved = 0
    for plot_name, plot_fig in plots.items():
        # Remove suffix from plot_name if it exists
        clean_name = plot_name.replace(f"_{analysis_suffix}", "")
        png_path = os.path.join(output_plots_path, f"{prefix}{clean_name}.png")
        plot_fig.savefig(png_path, dpi=300, bbox_inches='tight')
        plots_saved += 1
        print(f"Saved plot: {prefix}{clean_name}.png")
    
    print(f"\nExport Summary:")
    print(f"  Tables saved: {tables_saved}")
    print(f"  Plots saved: {plots_saved}")
    print(f"  Output location: {output_base_path}")
    print(f"  Analysis type: {analysis_suffix}")
    print(f"  File prefix: {prefix}")

save_all_results()

