#!/usr/bin/env python
# coding: utf-8

# # Notebook: Qualitative Evaluation (Experts 3, 4 & 5) -- Experiment 1

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
    
    # Load all three experts data with proper CSV handling
    experts_data = {}
    for expert in [3, 4, 5]:
        expert_key = f'expert_{expert}'
        try:
            exp1a_path = os.path.join(expert_base_path, expert_key, "exp1a.csv")
            exp1b_path = os.path.join(expert_base_path, expert_key, "exp1b.csv")
            
            # Try different separators based on expert
            if expert == 4:
                # Expert 4 uses semicolons
                exp1a_data = pd.read_csv(exp1a_path, sep=';', quotechar='"')
                exp1b_data = pd.read_csv(exp1b_path, sep=';', quotechar='"')
            else:
                # Other experts use commas
                exp1a_data = pd.read_csv(exp1a_path, quotechar='"', escapechar='\\')
                exp1b_data = pd.read_csv(exp1b_path, quotechar='"', escapechar='\\')
            
            experts_data[expert_key] = {
                'exp1a': exp1a_data,
                'exp1b': exp1b_data
            }
            experts_data[expert_key]['exp1a']['expert'] = expert_key
            experts_data[expert_key]['exp1b']['expert'] = expert_key
            
            print(f"Loaded {expert_key}: Exp1a={len(experts_data[expert_key]['exp1a'])}, Exp1b={len(experts_data[expert_key]['exp1b'])}")
            
        except Exception as e:
            print(f"Error loading {expert_key}: {e}")
            continue
    
    if not experts_data:
        print("No expert data could be loaded!")
        return None, None, None, None, None
    
    # Combine all experts data
    exp1a_combined = pd.concat([data['exp1a'] for data in experts_data.values()], ignore_index=True)
    exp1b_combined = pd.concat([data['exp1b'] for data in experts_data.values()], ignore_index=True)
    
    # Add hint information - repeat hints for each expert
    hint_multiplier = len(experts_data)
    exp1a_hints_extended = pd.concat([hint_exp1a[['llm', 'prompt_type']]] * hint_multiplier, ignore_index=True)
    exp1b_hints_extended = pd.concat([hint_exp1b[['llm', 'prompt_type']]] * hint_multiplier, ignore_index=True)
    
    # Merge data carefully
    exp1a_df = exp1a_combined.copy()
    exp1b_df = exp1b_combined.copy()
    
    # Add missing columns from hints
    for col in ['llm', 'prompt_type']:
        if col not in exp1a_df.columns:
            exp1a_df[col] = exp1a_hints_extended[col].values
        if col not in exp1b_df.columns:
            exp1b_df[col] = exp1b_hints_extended[col].values
    
    numeric_cols_1a = ['relevance', 'clarity', 'answerability', 'challenging', 'value', 'language', 'correctness']
    numeric_cols_1b = ['relevance', 'clarity', 'answerability', 'challenging', 'value', 'language', 'manipulation_handling']
    
    # Clean and convert numeric columns to integers
    print("\nKonvertiere Bewertungen zu Integern...")
    for df, cols, exp_name in [(exp1a_df, numeric_cols_1a, "1a"), (exp1b_df, numeric_cols_1b, "1b")]:
        for col in cols:
            if col in df.columns:
                print(f"  Processing {exp_name}.{col}...")
                
                # Erstelle Debug-Info vor der Konvertierung
                non_numeric_before = df[col].apply(lambda x: not pd.isna(x) and not isinstance(x, (int, float))).sum()
                if non_numeric_before > 0:
                    print(f"    Found {non_numeric_before} non-numeric values before cleaning")
                
                # Bereinige ungültige Werte (aber behalte 0!)
                df[col] = df[col].replace(['??', '???', '', ' ', 'nan', 'NaN', 'NULL', 'null'], np.nan)
                
                # Konvertiere zu numeric (float first)
                df[col] = pd.to_numeric(df[col], errors='coerce')
                
                # Konvertiere zu Integer (behalte NaN bei)
                # Verwende 'Int64' dtype für nullable integers
                df[col] = df[col].astype('Int64')
                
                # Prüfe Wertebereich (0-10 für alle Kriterien)
                valid_data = df[col].dropna()
                if len(valid_data) > 0:
                    min_val = valid_data.min()
                    max_val = valid_data.max()
                    
                    # Prüfe erlaubten Bereich (0-10 für alle Kriterien)
                    valid_range = (0, 10)
                    
                    # Warnung bei Werten außerhalb des Bereichs
                    out_of_range = valid_data[(valid_data < valid_range[0]) | (valid_data > valid_range[1])]
                    if len(out_of_range) > 0:
                        print(f"    WARNING: {len(out_of_range)} values outside range {valid_range}")
                        # Entferne Werte außerhalb des gültigen Bereichs
                        df.loc[(df[col] < valid_range[0]) | (df[col] > valid_range[1]), col] = np.nan
                        df[col] = df[col].astype('Int64')
                    
                    print(f"    Range: {min_val}-{max_val}, Valid entries: {len(valid_data)}")
                else:
                    print(f"    No valid data found")
                
                # Debug: Prüfe finale Datentypen
                print(f"    Final dtype: {df[col].dtype}")
    
    exp1a_df['experiment'] = 'exp1a'
    exp1b_df['experiment'] = 'exp1b'
    
    # Handle input_source naming
    if 'input_source' in exp1b_df.columns:
        exp1b_df['input_source'] = exp1b_df['input_source'].replace('script', 'script_manipulated')
    
    # Calculate completion rates
    exp1a_filled = exp1a_df[numeric_cols_1a].notna().sum().sum()
    exp1a_total = len(exp1a_df) * len(numeric_cols_1a)
    exp1b_filled = exp1b_df[numeric_cols_1b].notna().sum().sum()
    exp1b_total = len(exp1b_df) * len(numeric_cols_1b)
    
    print(f"\nData loaded for {len(experts_data)} experts")
    print(f"Completion rates:")
    print(f"  Exp 1a: {exp1a_filled}/{exp1a_total} ({100*exp1a_filled/exp1a_total:.1f}%)")
    print(f"  Exp 1b: {exp1b_filled}/{exp1b_total} ({100*exp1b_filled/exp1b_total:.1f}%)")
    
    # Berechne total_score (verwende fillvalue=0 für Integer summation)
    exp1a_df['total_score'] = exp1a_df[numeric_cols_1a].sum(axis=1, skipna=True)
    exp1b_df['total_score'] = exp1b_df[numeric_cols_1b].sum(axis=1, skipna=True)
    
    # Zusätzliche Datentyp-Validierung für experts_data
    print(f"\nValidiere Datentypen in experts_data...")
    for expert_key in experts_data:
        for exp_type in ['exp1a', 'exp1b']:
            cols = numeric_cols_1a if exp_type == 'exp1a' else numeric_cols_1b
            for col in cols:
                if col in experts_data[expert_key][exp_type].columns:
                    # Bereinige auch die einzelnen Expert-DataFrames
                    experts_data[expert_key][exp_type][col] = experts_data[expert_key][exp_type][col].replace(['??', '???', '', ' ', 'nan', 'NaN', 'NULL', 'null'], np.nan)
                    experts_data[expert_key][exp_type][col] = pd.to_numeric(experts_data[expert_key][exp_type][col], errors='coerce')
                    
                    # Behalte 0-Werte für alle Kriterien!
                    experts_data[expert_key][exp_type][col] = experts_data[expert_key][exp_type][col].astype('Int64')
    
    print(f"Datentyp-Konvertierung abgeschlossen!")
    
    return exp1a_df, exp1b_df, numeric_cols_1a, numeric_cols_1b, experts_data

# Load data
result = load_and_prepare_data()
if result[0] is not None:
    exp1a_df, exp1b_df, numeric_cols_1a, numeric_cols_1b, experts_data = result
    
    print("\n" + "="*50)
    print("DATA OVERVIEW")
    print("="*50)
    
    for exp_name, exp_df in [("1a", exp1a_df), ("1b", exp1b_df)]:
        print(f"\nExperiment {exp_name}:")
        print(f"  Total samples: {len(exp_df)}")
        if 'expert' in exp_df.columns:
            print(f"  Experts: {dict(exp_df['expert'].value_counts())}")
        if 'llm' in exp_df.columns:
            print(f"  LLMs: {list(exp_df['llm'].unique())}")
        if 'prompt_type' in exp_df.columns:
            print(f"  Prompt Types: {list(exp_df['prompt_type'].unique())}")
        if 'input_source' in exp_df.columns:
            print(f"  Input Sources: {list(exp_df['input_source'].unique())}")
            
    # Zeige Datentypen für Überprüfung
    print(f"\n" + "="*50)
    print("DATENTYP ÜBERPRÜFUNG")
    print("="*50)
    
    print(f"\nExperiment 1a Datentypen:")
    for col in numeric_cols_1a:
        if col in exp1a_df.columns:
            print(f"  {col}: {exp1a_df[col].dtype}")
    
    print(f"\nExperiment 1b Datentypen:")
    for col in numeric_cols_1b:
        if col in exp1b_df.columns:
            print(f"  {col}: {exp1b_df[col].dtype}")
            
else:
    print("Failed to load data!")


# # Experiment 1a: Original Content Analysis
# 
# Analysis of LLM question generation quality using original source materials (script, transcript, tanenbaum textbook).

# ## 1a.1: Descriptive Statistics

# In[ ]:


# print("EXPERIMENT 1A - DATENVALIDIERUNG UND DESCRIPTIVE STATISTICS")
# print("="*60)

# # Zusätzliche Datenvalidierung vor der Analyse
# print("\nDATENVALIDIERUNG:")
# print("="*30)

# for exp_name, exp_df, cols in [("1a", exp1a_df, numeric_cols_1a), ("1b", exp1b_df, numeric_cols_1b)]:
#     print(f"\nExperiment {exp_name}:")
#     for col in cols:
#         if col in exp_df.columns:
#             # Prüfe Datentyp
#             dtype = exp_df[col].dtype
#             print(f"  {col}: {dtype}")
            
#             # Prüfe auf ungültige Werte
#             valid_data = exp_df[col].dropna()
#             if len(valid_data) > 0:
#                 # Prüfe Wertebereich
#                 min_val = valid_data.min()
#                 max_val = valid_data.max()
                
#                 # Erwarteter Bereich: 0-10 für alle Kriterien
#                 expected_min = 0
#                 expected_max = 10
                
#                 if min_val < expected_min or max_val > expected_max:
#                     print(f"    WARNING: Werte außerhalb Bereich [{expected_min}-{expected_max}]: {min_val}-{max_val}")
#                 else:
#                     print(f"    ✓ Wertebereich korrekt: {min_val}-{max_val}")
                
#                 # Prüfe auf Nicht-Integer-Werte
#                 non_integer = valid_data[valid_data % 1 != 0]
#                 if len(non_integer) > 0:
#                     print(f"    WARNING: {len(non_integer)} Nicht-Integer-Werte gefunden")
#                     print(f"      Beispiele: {non_integer.head().tolist()}")
#                 else:
#                     print(f"    ✓ Alle Werte sind Integer")
                    
#                 # Zeige Verteilung der Werte
#                 value_counts = valid_data.value_counts().sort_index()
#                 print(f"    Werteverteilung: {dict(value_counts.head(11))}")  # Zeige 0-10
#             else:
#                 print(f"    Keine gültigen Daten")

# print("\n" + "="*60)
# print("DESCRIPTIVE STATISTICS")
# print("="*60)

# exp1a_stats = exp1a_df[numeric_cols_1a].describe().round(2)
# tables['exp1a_overall_stats'] = exp1a_stats
# print("\nOverall Statistics (all criteria):")
# display(exp1a_stats)

# exp1a_llm_stats = exp1a_df.groupby('llm')[numeric_cols_1a].agg(['mean', 'std', 'count']).round(2)
# tables['exp1a_llm_stats'] = exp1a_llm_stats
# print("\nStatistics by LLM:")
# display(exp1a_llm_stats)

# exp1a_source_stats = exp1a_df.groupby('input_source')[numeric_cols_1a].agg(['mean', 'std', 'count']).round(2)
# tables['exp1a_source_stats'] = exp1a_source_stats
# print("\nStatistics by Input Source:")
# display(exp1a_source_stats)

# exp1a_prompt_stats = exp1a_df.groupby('prompt_type')[numeric_cols_1a].agg(['mean', 'std', 'count']).round(2)
# tables['exp1a_prompt_stats'] = exp1a_prompt_stats
# print("\nStatistics by Prompt Type:")
# display(exp1a_prompt_stats)


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

# Konvertiere zu float für seaborn-Kompatibilität
heatmap_mean = heatmap_mean.astype(float)
heatmap_std = heatmap_std.astype(float)

# Erstelle String-Matrix für Annotationen
annot_matrix = pd.DataFrame(index=heatmap_mean.index, columns=heatmap_mean.columns, dtype=str)
for i in range(len(heatmap_mean.index)):
    for j in range(len(heatmap_mean.columns)):
        mean_val = heatmap_mean.iloc[i, j]
        std_val = heatmap_std.iloc[i, j]
        if pd.notna(mean_val) and pd.notna(std_val):
            annot_matrix.iloc[i, j] = f"{mean_val:.1f}\n({std_val:.1f})"
        elif pd.notna(mean_val):
            annot_matrix.iloc[i, j] = f"{mean_val:.1f}"
        else:
            annot_matrix.iloc[i, j] = ""

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

# Konvertiere zu float für seaborn-Kompatibilität
heatmap_mean_prompt = heatmap_mean_prompt.astype(float)
heatmap_std_prompt = heatmap_std_prompt.astype(float)

# Erstelle String-Matrix für Annotationen
annot_matrix_prompt = pd.DataFrame(index=heatmap_mean_prompt.index, columns=heatmap_mean_prompt.columns, dtype=str)
for i in range(len(heatmap_mean_prompt.index)):
    for j in range(len(heatmap_mean_prompt.columns)):
        mean_val = heatmap_mean_prompt.iloc[i, j]
        std_val = heatmap_std_prompt.iloc[i, j]
        if pd.notna(mean_val) and pd.notna(std_val):
            annot_matrix_prompt.iloc[i, j] = f"{mean_val:.1f}\n({std_val:.1f})"
        elif pd.notna(mean_val):
            annot_matrix_prompt.iloc[i, j] = f"{mean_val:.1f}"
        else:
            annot_matrix_prompt.iloc[i, j] = ""

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

# Konvertiere zu float für seaborn-Kompatibilität
correctness_heatmap_mean = correctness_heatmap_mean.astype(float)
correctness_heatmap_std = correctness_heatmap_std.astype(float)

# Erstelle String-Matrix für Annotationen
correctness_annot_matrix = pd.DataFrame(index=correctness_heatmap_mean.index, columns=correctness_heatmap_mean.columns, dtype=str)
for i in range(len(correctness_heatmap_mean.index)):
    for j in range(len(correctness_heatmap_mean.columns)):
        mean_val = correctness_heatmap_mean.iloc[i, j]
        std_val = correctness_heatmap_std.iloc[i, j]
        if pd.notna(mean_val) and pd.notna(std_val):
            correctness_annot_matrix.iloc[i, j] = f"{mean_val:.1f}\n({std_val:.1f})"
        elif pd.notna(mean_val):
            correctness_annot_matrix.iloc[i, j] = f"{mean_val:.1f}"
        else:
            correctness_annot_matrix.iloc[i, j] = ""

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

# Konvertiere zu float für seaborn-Kompatibilität
correctness_prompt_heatmap_mean = correctness_prompt_heatmap_mean.astype(float)
correctness_prompt_heatmap_std = correctness_prompt_heatmap_std.astype(float)

# Erstelle String-Matrix für Annotationen
correctness_prompt_annot_matrix = pd.DataFrame(index=correctness_prompt_heatmap_mean.index, columns=correctness_prompt_heatmap_mean.columns, dtype=str)
for i in range(len(correctness_prompt_heatmap_mean.index)):
    for j in range(len(correctness_prompt_heatmap_mean.columns)):
        mean_val = correctness_prompt_heatmap_mean.iloc[i, j]
        std_val = correctness_prompt_heatmap_std.iloc[i, j]
        if pd.notna(mean_val) and pd.notna(std_val):
            correctness_prompt_annot_matrix.iloc[i, j] = f"{mean_val:.1f}\n({std_val:.1f})"
        elif pd.notna(mean_val):
            correctness_prompt_annot_matrix.iloc[i, j] = f"{mean_val:.1f}"
        else:
            correctness_prompt_annot_matrix.iloc[i, j] = ""

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
    fig, axes = plt.subplots(4, 2, figsize=(14, 20))
    axes = axes.flatten()
    plots['exp1b_llm_analysis'] = fig
    
    criteria_1b = ['relevance', 'clarity', 'answerability', 'challenging', 'value', 'language', 'manipulation_handling']
    
    for i, criterion in enumerate(criteria_1b):
        # Spezielle Formatierung für manipulation_handling
        if criterion == 'manipulation_handling':
            display_title = 'Manipulation Handling'
            ylabel = 'Manipulation Handling'
        else:
            display_title = criterion.title()
            ylabel = criterion.title()
            
        create_seaborn_boxplot(exp1b_df, 'llm', criterion, axes[i], 
                              display_title, ylabel, 'LLM', scale_range=(0, 10))
    
    create_seaborn_boxplot(exp1b_df, 'llm', 'total_score', axes[7], 
                          'Total Score', 'Total Score', 'LLM', scale_range=(0, 70))
    
    plt.suptitle('Experiment 1b: LLM Performance across all Criteria', fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.subplots_adjust(top=0.95)
    plt.show()
    
    print("\n" + "="*80)
    print("DETAILED STATISTICS - LLM PERFORMANCE (EXPERIMENT 1B)")
    print("="*80)
    
    all_criteria_1b_with_total = criteria_1b + ['total_score']
    exp1b_llm_detailed_stats = exp1b_df.groupby('llm')[all_criteria_1b_with_total].agg(['mean', 'std', 'median', 'min', 'max', 'count']).round(2)
    tables['exp1b_llm_detailed_stats'] = exp1b_llm_detailed_stats
    print("\nDetailed Statistics by LLM (Experiment 1b):")
    display(exp1b_llm_detailed_stats)
    
    # Kombinierte Tabelle: LLM x Prompt Type mit Fokus auf Manipulation Handling
    print("\n" + "="*80)
    print("MANIPULATION HANDLING ANALYSIS - LLM x PROMPT TYPE COMBINATIONS")
    print("="*80)
    
    exp1b_llm_prompt_manipulation = exp1b_df.groupby(['llm', 'prompt_type']).agg({
        'manipulation_handling': ['mean', 'std', 'median', 'count'],
    }).round(2)
    
    # Flatten column names für bessere Lesbarkeit
    exp1b_llm_prompt_manipulation.columns = [
        'Manipulation Handling Mean', 'Std', 'Median', 'Count',
    ]
    
    tables['exp1b_llm_prompt_manipulation_focus'] = exp1b_llm_prompt_manipulation
    print("\nManipulation Handling Performance by LLM and Prompt Type:")
    display(exp1b_llm_prompt_manipulation)
    
    # Zusätzliche Analyse: Beste Kombinationen für Manipulation Handling
    # manipulation_ranking = exp1b_llm_prompt_manipulation.sort_values('Manipulation_Handling_Mean', ascending=False)
    # print("\nRanking der LLM-Prompt Kombinationen nach Manipulation Handling:")
    # display(manipulation_ranking[['Manipulation_Handling_Mean', 'Manipulation_Handling_Count']])
    
    fig, axes = plt.subplots(4, 2, figsize=(14, 20))
    axes = axes.flatten()
    plots['exp1b_prompt_analysis'] = fig
    
    for i, criterion in enumerate(criteria_1b):
        if criterion == 'manipulation_handling':
            display_title = 'Manipulation Handling'
            ylabel = 'Manipulation Handling'
        else:
            display_title = criterion.title()
            ylabel = criterion.title()
            
        create_seaborn_boxplot(exp1b_df, 'prompt_type', criterion, axes[i], 
                              display_title, ylabel, 'Prompt Type', scale_range=(0, 10))
    
    create_seaborn_boxplot(exp1b_df, 'prompt_type', 'total_score', axes[7], 
                          'Total Score', 'Total Score', 'Prompt Type', scale_range=(0, 70))
    
    plt.suptitle('Experiment 1b: Performance by Prompt Type', fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.subplots_adjust(top=0.95)
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


# In[ ]:


if analyze_exp1b:
    print("\n" + "="*80)
    print("COMPREHENSIVE LLM STATISTICS - ALL CRITERIA (EXPERIMENT 1B)")
    print("="*80)
    
    # Erstelle umfassende Statistiken für alle Kriterien pro LLM
    exp1b_llm_comprehensive = exp1b_df.groupby('llm')[numeric_cols_1b + ['total_score']].agg(['mean', 'std', 'median']).round(2)
    tables['exp1b_llm_comprehensive_stats'] = exp1b_llm_comprehensive
    print("\nComprehensive Statistics by LLM (Mean, Std, Median) - Experiment 1b:")
    display(exp1b_llm_comprehensive)
    
    # Zusätzlich: Ranking der LLMs basierend auf verschiedenen Metriken
    print("\n" + "="*60)
    print("LLM RANKINGS BY DIFFERENT METRICS (EXPERIMENT 1B)")
    print("="*60)
    
    # Ranking nach Total Score
    total_score_ranking = exp1b_df.groupby('llm')['total_score'].mean().sort_values(ascending=False)
    print("\nLLM Ranking by Total Score (Mean):")
    for i, (llm, score) in enumerate(total_score_ranking.items(), 1):
        print(f"{i}. {llm.title()}: {score:.2f}/70")
    
    # Ranking nach Manipulation Handling (spezifisch für Exp1b)
    manipulation_ranking = exp1b_df.groupby('llm')['manipulation_handling'].mean().sort_values(ascending=False)
    print("\nLLM Ranking by Manipulation Handling (Mean):")
    for i, (llm, score) in enumerate(manipulation_ranking.items(), 1):
        print(f"{i}. {llm.title()}: {score:.2f}/10")
    
    # Zeige auch Count pro LLM
    exp1b_llm_counts = exp1b_df.groupby('llm').size()
    print("\nSample Counts by LLM:")
    for llm, count in exp1b_llm_counts.items():
        print(f"  {llm.title()}: {count} samples")
    
else:
    print("Comprehensive LLM statistics section ready for Experiment 1b data")
    print("Will include: Mean/Std/Median for all criteria, LLM rankings, and sample counts")


# # Summary and Key Insights
# 
# This section provides a comprehensive summary of findings from the qualitative analysis of Experiment 1.

# ## Inter-Rater Agreement Analysis

# In[ ]:


# Vereinfachte Fleiss Kappa Berechnung für Experten 3, 4, 5
from statsmodels.stats.inter_rater import fleiss_kappa
import numpy as np
import pandas as pd

def simple_fleiss_kappa(expert3_df, expert4_df, expert5_df, criteria_cols):
    """Fleiss Kappa Berechnung für 3 Experten mit korrekter 0-10 Skala"""
    results = []
    
    # Finde gemeinsame sample_ids
    ids3 = set(expert3_df['sample_id'].astype(int))
    ids4 = set(expert4_df['sample_id'].astype(int)) 
    ids5 = set(expert5_df['sample_id'].astype(int))
    common_ids = sorted(list(ids3 & ids4 & ids5))
    
    print(f"Gemeinsame Items: {len(common_ids)}")
    
    for criterion in criteria_cols:
        print(f"\nKriterium: {criterion}")
        
        # Sammle Ratings für gemeinsame Items
        ratings = []
        for sample_id in common_ids:
            # Hole Rating von jedem Experten
            r3 = expert3_df[expert3_df['sample_id'] == sample_id][criterion].iloc[0]
            r4 = expert4_df[expert4_df['sample_id'] == sample_id][criterion].iloc[0] 
            r5 = expert5_df[expert5_df['sample_id'] == sample_id][criterion].iloc[0]
            
            # Konvertiere nullable integers zu standard python ints/floats für Vergleich
            def safe_convert(val):
                if pd.isna(val):
                    return np.nan
                return float(val)
            
            r3_val = safe_convert(r3)
            r4_val = safe_convert(r4)
            r5_val = safe_convert(r5)
            
            # Prüfe ob alle Ratings gültig sind (0-10 für alle Kriterien)
            if all(not pd.isna(r) and 0 <= r <= 10 for r in [r3_val, r4_val, r5_val]):
                # Verwende die ursprünglichen Werte (0-10) ohne Verschiebung
                ratings.append([int(r3_val), int(r4_val), int(r5_val)])
        
        print(f"  Gültige Items: {len(ratings)}")
        
        if len(ratings) < 2:
            print(f"  Zu wenig Daten!")
            continue
            
        # Zeige erste paar Ratings (ursprüngliche 0-10 Skala)
        print(f"  Beispiel Ratings (0-10 Skala): {ratings[:3]}")
        
        # Erstelle Fleiss Tabelle (Items x Kategorien)
        # Für 0-10 Skala brauchen wir 11 Kategorien (0, 1, 2, ..., 10)
        ratings_array = np.array(ratings)
        n_items = len(ratings)
        fleiss_table = np.zeros((n_items, 11))  # 11 Kategorien (0-10)
        
        for i, item_ratings in enumerate(ratings):
            for rating in item_ratings:
                fleiss_table[i, int(rating)] += 1  # Rating 0-10 -> Index 0-10
        
        # Berechne Kappa
        try:
            kappa = fleiss_kappa(fleiss_table)
            
            # Interpretation
            if kappa < 0.2:
                level = "Slight"
            elif kappa < 0.4:
                level = "Fair"
            elif kappa < 0.6:
                level = "Moderate" 
            elif kappa < 0.8:
                level = "Substantial"
            else:
                level = "Almost Perfect"
            
            # Statistiken basieren auf ursprünglichen 0-10 Werten
            results.append({
                'Criterion': criterion,
                'Fleiss_Kappa': round(kappa, 3),
                'Agreement_Level': level,
                'N_Items': len(ratings),
                'Mean_Rating': round(np.mean(ratings_array), 2),
                'Std_Rating': round(np.std(ratings_array), 2)
            })
            
            print(f"  Kappa: {kappa:.3f} ({level})")
            print(f"  Mittlere Bewertung: {np.mean(ratings_array):.2f} (0-10 Skala)")
            
        except Exception as e:
            print(f"  Fehler: {e}")
    
    return pd.DataFrame(results)

# Führe Berechnung aus
print("FLEISS KAPPA für Experten 3, 4, 5 - Experiment 1a")
print("="*50)

kappa_results = simple_fleiss_kappa(
    experts_data['expert_3']['exp1a'],
    experts_data['expert_4']['exp1a'], 
    experts_data['expert_5']['exp1a'],
    numeric_cols_1a
)

print("\nErgebnisse:")
display(kappa_results)


# In[ ]:


print("EXPERIMENT 1A - INTER-RATER AGREEMENT (Fleiss' Kappa für Experten 3-5)")
print("="*70)

# Verwende die bereits definierte simple_fleiss_kappa Funktion
if 'kappa_results' in locals() and not kappa_results.empty:
    agreement_exp1a = kappa_results.copy()
    tables['agreement_exp1a_real_fleiss'] = agreement_exp1a

    print("\nFleiss' Kappa Agreement Statistiken (basierend auf realen Expert-Bewertungen):")
    display(agreement_exp1a.round(3))

    # Summary statistics
    print("\n" + "="*50)
    print("AGREEMENT SUMMARY - EXPERIMENT 1A (REAL DATA)")
    print("="*50)

    valid_kappas = agreement_exp1a['Fleiss_Kappa'].dropna()
    if len(valid_kappas) > 0:
        avg_kappa = valid_kappas.mean()
        
        # Definiere kappa_level Funktion lokal
        def kappa_level(kappa):
            if kappa < 0.2:
                return "Slight"
            elif kappa < 0.4:
                return "Fair" 
            elif kappa < 0.6:
                return "Moderate"
            elif kappa < 0.8:
                return "Substantial"
            else:
                return "Almost Perfect"
        
        print(f"\nOVERALL AGREEMENT STATISTICS:")
        print(f"  Average Fleiss' Kappa: {avg_kappa:.3f}")
        print(f"  Agreement Level: {kappa_level(avg_kappa)}")

        # Best and worst agreement by criterion
        valid_rows = agreement_exp1a.dropna(subset=['Fleiss_Kappa'])
        if len(valid_rows) > 0:
            best_criterion = valid_rows.loc[valid_rows['Fleiss_Kappa'].idxmax()]
            worst_criterion = valid_rows.loc[valid_rows['Fleiss_Kappa'].idxmin()]

            print(f"\nBest agreement: {best_criterion['Criterion']} (κ = {best_criterion['Fleiss_Kappa']:.3f}, {best_criterion['Agreement_Level']})")
            print(f"Worst agreement: {worst_criterion['Criterion']} (κ = {worst_criterion['Fleiss_Kappa']:.3f}, {worst_criterion['Agreement_Level']})")

        # Distribution of agreement levels
        print(f"\nAgreement Level Distribution:")
        level_counts = agreement_exp1a['Agreement_Level'].value_counts()
        for level, count in level_counts.items():
            print(f"  {level}: {count} criteria")
            
        # Details über die Anzahl bewerteter Items
        print(f"\nAnzahl bewerteter Items pro Kriterium:")
        for _, row in agreement_exp1a.iterrows():
            print(f"  {row['Criterion']}: {row['N_Items']} Items")
    else:
        print("Keine gültigen Kappa-Werte berechnet")
else:
    print("Keine Kappa-Ergebnisse verfügbar. Führen Sie zuerst die vorherige Zelle aus.")


# In[ ]:


# Check data availability for Experiment 1b
exp1b_has_data = False
total_filled = 0

for expert_key in ['expert_3', 'expert_4', 'expert_5']:
    if expert_key in experts_data:
        expert_filled = experts_data[expert_key]['exp1b'][numeric_cols_1b].notna().sum().sum()
        total_filled += expert_filled

if total_filled > 50:  # Threshold for meaningful analysis
    exp1b_has_data = True

if exp1b_has_data:
    print("EXPERIMENT 1B - INTER-RATER AGREEMENT (Fleiss' Kappa für Experten 3-5)")
    print("="*70)
    
    # Calculate Fleiss' kappa for experiment 1b using simple_fleiss_kappa
    agreement_exp1b = simple_fleiss_kappa(
        experts_data['expert_3']['exp1b'],
        experts_data['expert_4']['exp1b'], 
        experts_data['expert_5']['exp1b'],
        numeric_cols_1b
    )
    tables['agreement_exp1b_real_fleiss'] = agreement_exp1b
    
    print("\nFleiss' Kappa Agreement Statistiken (basierend auf realen Expert-Bewertungen):")
    display(agreement_exp1b.round(3))
    
    # Summary statistics
    print("\n" + "="*50)
    print("AGREEMENT SUMMARY - EXPERIMENT 1B (REAL DATA)")
    print("="*50)
    
    valid_kappas_1b = agreement_exp1b['Fleiss_Kappa'].dropna()
    if len(valid_kappas_1b) > 0:
        avg_kappa_1b = valid_kappas_1b.mean()
        
        # Definiere kappa_level Funktion lokal für 1b
        def kappa_level(kappa):
            if kappa < 0.2:
                return "Slight"
            elif kappa < 0.4:
                return "Fair" 
            elif kappa < 0.6:
                return "Moderate"
            elif kappa < 0.8:
                return "Substantial"
            else:
                return "Almost Perfect"
        
        print(f"\nOVERALL AGREEMENT STATISTICS (EXP 1B):")
        print(f"  Average Fleiss' Kappa: {avg_kappa_1b:.3f}")
        print(f"  Agreement Level: {kappa_level(avg_kappa_1b)}")
        
        # Details über die Anzahl bewerteter Items
        print(f"\nAnzahl bewerteter Items pro Kriterium (Exp1b):")
        for _, row in agreement_exp1b.iterrows():
            print(f"  {row['Criterion']}: {row['N_Items']} Items")
    else:
        print("Keine gültigen Kappa-Werte für Experiment 1b berechnet")
    
else:
    print("EXPERIMENT 1B - INTER-RATER AGREEMENT (INSUFFICIENT DATA)")
    print("="*70)
    print("Not enough completed evaluations for meaningful agreement analysis.")
    print("Agreement analysis will be available once experts complete more evaluations.")


# In[ ]:


print("\n" + "="*80)
print("DETAILED EXPERT COMPARISON (EXPERTS 3-5)")
print("="*80)

print("\nEXPERT RATING PATTERNS - EXPERIMENT 1A")
print("-" * 50)

# Calculate mean ratings by expert for Experiment 1a (experts 3-5 only)
expert_means_1a = {}
expert_stds_1a = {}

for expert_key in ['expert_3', 'expert_4', 'expert_5']:
    if expert_key in experts_data:
        expert_means_1a[expert_key] = experts_data[expert_key]['exp1a'][numeric_cols_1a].mean()
        expert_stds_1a[expert_key] = experts_data[expert_key]['exp1a'][numeric_cols_1a].std()

# Create comparison dataframe
if expert_means_1a:
    comparison_df_1a = pd.DataFrame(expert_means_1a).T
    comparison_df_1a['Overall_Mean'] = comparison_df_1a.mean(axis=1)
    comparison_df_1a = comparison_df_1a.round(3)

    tables['expert_comparison_exp1a_experts35'] = comparison_df_1a

    print("Mean Ratings by Expert (Experiment 1a, Experts 3-5):")
    display(comparison_df_1a)

    # Expert ranking by overall performance
    expert_ranking = comparison_df_1a['Overall_Mean'].sort_values(ascending=False)
    print(f"\nExpert Ranking by Overall Performance:")
    for i, (expert, score) in enumerate(expert_ranking.items(), 1):
        print(f"{i}. {expert}: {score:.3f}")

    # Standard deviations comparison
    std_comparison = pd.DataFrame(expert_stds_1a).T.round(3)
    tables['expert_std_comparison_exp1a_experts35'] = std_comparison

    print("\nRating Consistency (Standard Deviations):")
    display(std_comparison)

    # Most lenient/strict expert
    most_lenient = expert_ranking.index[0]
    most_strict = expert_ranking.index[-1]
    print(f"\nMost lenient expert: {most_lenient}")
    print(f"Most strict expert: {most_strict}")

# Check if Experiment 1b has enough data
exp1b_has_enough_data = False
if len(exp1b_df) > 0:
    total_filled = 0
    for expert_key in ['expert_3', 'expert_4', 'expert_5']:
        if expert_key in experts_data:
            total_filled += experts_data[expert_key]['exp1b'][numeric_cols_1b].notna().sum().sum()
    if total_filled > 50:  # Threshold for meaningful analysis
        exp1b_has_enough_data = True

if exp1b_has_enough_data:
    print("\n" + "-" * 50)
    print("EXPERT RATING PATTERNS - EXPERIMENT 1B")
    
    expert_means_1b = {}
    for expert_key in ['expert_3', 'expert_4', 'expert_5']:
        if expert_key in experts_data:
            expert_means_1b[expert_key] = experts_data[expert_key]['exp1b'][numeric_cols_1b].mean()
    
    comparison_df_1b = pd.DataFrame(expert_means_1b).T
    comparison_df_1b['Overall_Mean'] = comparison_df_1b.mean(axis=1)
    comparison_df_1b = comparison_df_1b.round(3)
    
    tables['expert_comparison_exp1b_experts35'] = comparison_df_1b
    
    print("Mean Ratings by Expert (Experiment 1b, Experts 3-5):")
    display(comparison_df_1b)
else:
    print("\nExperiment 1b comparison will be available once experts complete more evaluations.")


# ## Data Export
# 
# Save all tables and plots for use in thesis and presentations.

# In[ ]:


def save_all_results():
    print("Saving results...")
    
    tables_saved = 0
    for table_name, table_data in tables.items():
        try:
            csv_path = os.path.join(output_tables_path, f"{table_name}_staff.csv")
            table_data.to_csv(csv_path)
            tables_saved += 1
            print(f"Saved table: {table_name}_staff.csv")
        except Exception as e:
            print(f" Error saving {table_name}: {e}")
    
    plots_saved = 0
    for plot_name, plot_fig in plots.items():
        try:
            png_path = os.path.join(output_plots_path, f"{plot_name}_staff.png")
            plot_fig.savefig(png_path, dpi=300, bbox_inches='tight')
            plots_saved += 1
            print(f"Saved plot: {plot_name}_staff.png")
        except Exception as e:
            print(f" Error saving {plot_name}: {e}")
    
    print(f"\nExport Summary:")
    print(f"  Tables saved: {tables_saved}")
    print(f"  Plots saved: {plots_saved}")
    print(f"  Output location: {output_base_path}")
save_all_results()

