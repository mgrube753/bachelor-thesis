#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt
import os
import warnings
from IPython.display import display

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


# In[ ]:


# === METRICS & LABELS ===
metrics = [
    'relevance',
    'clarity',
    'answerability',
    'challenging',
    'value',
    'language',
    'bloom_rating',
    "blooms_level_score"
 ]
metric_labels = {
    'relevance': 'Relevance',
    'clarity': 'Clarity',
    'answerability': 'Answerability',
    'challenging': 'Challenging',
    'value': 'Value',
    'language': 'Language',
    'bloom_rating': "Bloom's Level (Student)",
    'blooms_level_score': "Bloom's Level (Score)"
}


# In[ ]:


base_path = Path("../60_analyses/csv/qualitative/exp2/students")

BASE_PROJECT_PATH = os.path.abspath(os.path.join(os.getcwd(), "..", ".."))
hint_base_path = os.path.join(BASE_PROJECT_PATH, "20_experiments/60_analyses/csv/qualitative/exp2/hints")
output_base_path = os.path.join(BASE_PROJECT_PATH, "40_evaluation/exp2/qualitative")
output_tables_path = os.path.join(output_base_path, "tables")
output_plots_path = os.path.join(output_base_path, "plots")

for path in [output_tables_path, output_plots_path]:
    os.makedirs(path, exist_ok=True)

tables = {}
plots = {}


# In[ ]:


def load_student_data(student_id):
    student_path = base_path / f"student_{student_id}"
    data = {}
    
    for exp in ["exp2a", "exp2b", "exp2c"]:
        csv_path = student_path / f"{exp}.csv"
        if csv_path.exists():
            # Try multiple encodings to handle German characters
            df = None
            for encoding in ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']:
                try:
                    df = pd.read_csv(csv_path, encoding=encoding)
                    break
                except UnicodeDecodeError:
                    continue
            
            if df is None:
                print(f"Error: Could not read {csv_path} with any encoding")
                continue
            
            if 'comments' in df.columns:
                df = df.drop('comments', axis=1)

            if 'answer_problems' in df.columns:
                df = df.drop('answer_problems', axis=1)
            
            df['sample_id'] = df['sample_id'].astype(str)
            if 'question_num' not in df.columns:
                df['question_num'] = df['sample_id'].str.extract('(\\d+)').astype(int).iloc[:, 0]
            
            df['student'] = student_id
            df['experiment'] = exp
            data[exp] = df
            print(f"Loaded {exp} for student_{student_id}: {len(df)} questions")
    
    return data


def load_hint_data():
    hint_data = {}
    for exp in ["exp2a", "exp2b", "exp2c"]:
        hint_path = os.path.join(hint_base_path, f"{exp}_hints.csv")
        if os.path.exists(hint_path):
            hint_df = None
            for encoding in ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']:
                try:
                    hint_df = pd.read_csv(hint_path, encoding=encoding)
                    break
                except UnicodeDecodeError:
                    continue
            if hint_df is None:
                print(f"Error: Could not read {hint_path} with any encoding")
                continue
            if exp == 'exp2a':
                if 'question_id' not in hint_df.columns:
                    print(f"Warning: No question_id column found in {exp}_hints.csv")
                    continue
                hint_df['question_id'] = hint_df['question_id'].astype(str)
                print(f"Loaded {exp}_hints.csv: {len(hint_df)} rows")
                hint_data[exp] = hint_df
            elif exp in ['exp2b', 'exp2c'] and 'bloom_original' in hint_df.columns:
                hint_df = hint_df.copy()
                hint_df['bloom_original'] = hint_df['bloom_original'].astype(str)
                # DO NOT set question_id = index!
                print(f"Loaded {exp}_hints.csv: {len(hint_df)} rows (no question_id, using row order)")
                hint_data[exp] = hint_df
            else:
                print(f"Warning: No suitable columns found in {exp}_hints.csv")
    return hint_data

all_data = {}
for i in range(1, 4):
    all_data[f"student_{i}"] = load_student_data(i)

hint_data = load_hint_data()


# In[ ]:


def combine_data():
    combined = []
    print("\n--- Combining all available student data (no overlap filtering) ---")
    for student, experiments in all_data.items():
        print(f"\n{student}:")
        for exp, df in experiments.items():
            if not df.empty:
                if exp in hint_data:
                    hint_df = hint_data[exp]
                    # Always use row-wise assignment if lengths match
                    if len(df) == len(hint_df):
                        df_merged = df.copy()
                        for col in hint_df.columns:
                            if col not in df_merged.columns:
                                df_merged[col] = hint_df[col].values
                        print(f"  {exp}: {len(df_merged)} evaluations (row-wise assignment: {list(hint_df.columns)})")
                    else:
                        print(f"  {exp}: Could not row-wise assign hint data (len(df)={len(df)}, len(hint_df)={len(hint_df)})")
                        df_merged = df
                    combined.append(df_merged)
                else:
                    print(f"  {exp}: {len(df)} evaluations (no hint data available)")
                    combined.append(df)
    if combined:
        return pd.concat(combined, ignore_index=True)
    return pd.DataFrame()

df_combined = combine_data()
print(f"\n=== FINAL SUMMARY ===")
print(f"Total evaluations: {len(df_combined)}")

if len(df_combined) > 0:
    print(f"\nBreakdown by student:")
    for student_id in sorted(df_combined['student'].unique()):
        student_data = df_combined[df_combined['student'] == student_id]
        print(f"  Student {student_id}: {len(student_data)} evaluations")
        for exp in ["exp2a", "exp2b", "exp2c"]:
            exp_data = student_data[student_data['experiment'] == exp]
            if len(exp_data) > 0:
                questions = sorted(exp_data['question_num'].unique())
                print(f"    {exp}: {len(exp_data)} evaluations, Questions: {questions}")
else:
    print("No data loaded. Check if CSV files exist and contain data.")


# # Experiment 2: Descriptive Statistics
# 
# Analysis of prompt engineering approaches for question generation.

# In[ ]:


def convert_bloom_rating_simple(value, experiment, given_level=None):

    bloom_map = {
        6: 10,
        5: 8.5,
        4: 7,
        3: 4.5,
        2: 3,
        1: 1.5
    }
    import re
    def extract_levels(val):
        if isinstance(val, str):
            nums = re.findall(r'\d+', val)
            return [int(n) for n in nums] if nums else []
        elif isinstance(val, (int, float)) and not pd.isnull(val):
            return [int(val)]
        return []

    if experiment == 'exp2a':
        levels = extract_levels(value)
        if levels:
            max_level = max(levels)
            return bloom_map.get(max_level, np.nan)
        return np.nan
    elif experiment in ['exp2b', 'exp2c']:
        rater_levels = extract_levels(value)
        given_levels = extract_levels(given_level) if given_level is not None else []
        if not rater_levels or not given_levels:
            return np.nan
        best_score = 0
        for r in rater_levels:
            for g in given_levels:
                if r == g:
                    best_score = max(best_score, 10)
                elif abs(r - g) == 1:
                    best_score = max(best_score, 5)
        if best_score == 0:
            return 0
        return best_score
    else:
        return np.nan


# In[ ]:


# --- DESCRIPTIVE STATISTICS & PLOTS: ALL RATINGS (NO OVERLAP FILTERING) ---

print("EXPERIMENT 2 - DESCRIPTIVE STATISTICS (ALL RATINGS)")
print("="*70)
print(f"Number of ratings in df_combined: {len(df_combined)}")

# Create consistent numeric dataset for all ratings
df_numeric = df_combined.copy()

print("Converting metrics to numeric (all ratings)...")
for metric in metrics:
    if metric == 'bloom_rating':
        # bloom_rating bleibt das Rating der Studierenden
        df_numeric[metric] = df_combined[metric]
    elif metric == 'blooms_level_score':
        def bloom_score_apply(row):
            if row['experiment'] in ['exp2b', 'exp2c'] and 'bloom_original' in row and not pd.isnull(row['bloom_original']):
                return convert_bloom_rating_simple(row['bloom_rating'], row['experiment'], row['bloom_original'])
            else:
                return convert_bloom_rating_simple(row['bloom_rating'], row['experiment'])
        df_numeric[metric] = df_combined.apply(bloom_score_apply, axis=1)
    else:
        df_numeric[metric] = pd.to_numeric(df_combined[metric], errors='coerce')

display(df_numeric)

# Nur numerische Spalten für Statistik und Plots verwenden
numeric_metrics = [m for m in metrics if pd.api.types.is_numeric_dtype(df_numeric[m])]

# Basic statistics - ALL ratings
if len(df_numeric) > 0 and numeric_metrics:
    print("\nOverall Statistics (all metrics on 0-10 scale):")
    overall_stats = df_numeric[numeric_metrics].describe().round(2)
    display(overall_stats)

    print("\nStatistics by Experiment:")
    exp_stats = df_numeric.groupby('experiment')[numeric_metrics].agg(['mean', 'std', 'median', 'count']).round(2)
    display(exp_stats)
    
    print(f"\nQuestions per Experiment:")
    for exp in ["exp2a", "exp2b", "exp2c"]:
        exp_data = df_numeric[df_numeric['experiment'] == exp]
        if len(exp_data) > 0:
            questions = sorted(exp_data['question_num'].unique())
            print(f"  {exp}: Questions {questions} ({len(exp_data)} ratings)")
        else:
            print(f"  {exp}: No questions")
else:
    print("\nNo ratings available for statistics.")
    overall_stats = pd.DataFrame()
    exp_stats = pd.DataFrame()

# --- TOTAL SCORE ---
main_score_metrics = ['relevance', 'clarity', 'answerability', 'challenging', 'value', 'language', 'blooms_level_score']
existing_score_metrics = [m for m in main_score_metrics if m in df_numeric.columns]
df_numeric['total_score'] = df_numeric[existing_score_metrics].sum(axis=1)
metric_labels['total_score'] = 'Total Score'
if 'total_score' not in metrics:
    metrics.append('total_score')
if 'total_score' not in numeric_metrics:
    numeric_metrics.append('total_score')

# --- PLOTS: ALL RATINGS ---
print("\n=== VISUALIZATION: PERFORMANCE BY EXPERIMENT ===")

if len(df_numeric) > 0 and numeric_metrics:
    fig, axes = plt.subplots(4, 2, figsize=(14, 20))
    axes = axes.flatten()

    for i, metric in enumerate(numeric_metrics):
        df_plot = df_numeric[[metric, 'experiment']].dropna()
        if len(df_plot) > 0:
            metric_display = metric_labels[metric]
            colors = ['#66c2a5', '#fc8d62', '#8da0cb']
            sns.boxplot(data=df_plot, x='experiment', y=metric, ax=axes[i], palette=colors,
                        medianprops={'color': 'black', 'linewidth': 2.5, 'linestyle': ':'})
            # Always plot means for all metrics, including total_score
            for j, exp in enumerate(['exp2a', 'exp2b', 'exp2c']):
                exp_data = df_plot[df_plot['experiment'] == exp][metric]
                if len(exp_data) > 0:
                    mean_val = exp_data.mean()
                    axes[i].scatter(j, mean_val, color='red', marker='D', s=50, zorder=3, edgecolor='darkred', linewidth=1)
            if metric == 'total_score' or i == 7:
                axes[i].set_ylim(0, 70)
            else:
                axes[i].set_ylim(0, 10)
            axes[i].set_title(f'{metric_display}', fontsize=12, fontweight='bold')
            axes[i].set_xlabel('Experiment')
            axes[i].set_ylabel(metric_display)
            axes[i].grid(True, alpha=0.3)
            axes[i].set_xticklabels(['Type Only', 'Bloom Only', 'Type + Bloom'])
        else:
            axes[i].set_title(f'{metric_labels[metric]} - No Data')
            axes[i].text(0.5, 0.5, 'No Data', ha='center', va='center', transform=axes[i].transAxes)
    for j in range(len(numeric_metrics), len(axes)):
        axes[j].set_visible(False)
    plt.suptitle('Experiment 2: Performance across Prompt Engineering Approaches', fontsize=16, fontweight='bold', y=0.995)
    plt.subplots_adjust(top=0.92)
    plt.tight_layout()
    # Save the entire figure as one PNG
    if 'output_plots_path' in locals():
        figpath = os.path.join(output_plots_path, "exp2_boxplots_all_metrics_by_experiment.png")
        fig.savefig(figpath)
        print(f"Saved collective experiment boxplot: {figpath}")
    plt.show()
    print("Visualization complete.")
    print(f"Note: This visualization includes all {len(df_numeric)} ratings.")
else:
    print("No data available for visualization.")


# # Metric Analysis by LLM
# 
# The following section provides boxplots and summary tables for all metrics, grouped by LLM (language model).

# In[ ]:


# --- BOXPLOTS & TABLES: METRICS BY LLM ---

print("\n=== METRIC ANALYSIS BY LLM ===")

if 'df_numeric' in locals() and 'llm' in df_numeric.columns and len(df_numeric) > 0 and numeric_metrics:
    fig, axes = plt.subplots(4, 2, figsize=(14, 20))
    axes = axes.flatten()

    for i, metric in enumerate(numeric_metrics):
        df_plot = df_numeric[[metric, 'llm']].dropna()
        if len(df_plot) > 0:
            metric_display = metric_labels.get(metric, metric)
            colors = sns.color_palette("Set2", n_colors=df_plot['llm'].nunique())
            sns.boxplot(data=df_plot, x='llm', y=metric, ax=axes[i], palette=colors,
                        medianprops={'color': 'black', 'linewidth': 2.5, 'linestyle': ':'})
            for j, llm_name in enumerate(sorted(df_plot['llm'].unique())):
                llm_data = df_plot[df_plot['llm'] == llm_name][metric]
                if len(llm_data) > 0:
                    mean_val = llm_data.mean()
                    axes[i].scatter(j, mean_val, color='red', marker='D', s=50, zorder=3, edgecolor='darkred', linewidth=1)
            if metric == 'total_score' or i == 7:
                axes[i].set_ylim(0, 70)
            else:
                axes[i].set_ylim(0, 10)
            axes[i].set_title(f'{metric_display} by LLM', fontsize=12, fontweight='bold')
            axes[i].set_xlabel('LLM')
            axes[i].set_ylabel(metric_display)
            axes[i].grid(True, alpha=0.3)
            axes[i].set_xticklabels(sorted(df_plot['llm'].unique()), rotation=20)
        else:
            axes[i].set_title(f'{metric_labels[metric]} - No Data')
            axes[i].text(0.5, 0.5, 'No Data', ha='center', va='center', transform=axes[i].transAxes)
    for j in range(len(numeric_metrics), len(axes)):
        axes[j].set_visible(False)
    plt.suptitle('Experiment 2: Metrics by LLM', fontsize=16, fontweight='bold', y=0.995)
    plt.subplots_adjust(top=0.92)
    plt.tight_layout()
    
    if 'output_plots_path' in locals():
        figpath = os.path.join(output_plots_path, "exp2_boxplots_all_metrics_by_llm.png")
        fig.savefig(figpath)
        print(f"Saved collective LLM boxplot: {figpath}")
    plt.show()
    print("Visualization by LLM complete.")
    print(f"Note: This visualization includes all {len(df_numeric)} ratings.")

    # --- TABLES: METRICS BY LLM ---
    print("\nSummary Table: Metrics by LLM (mean, std, count)")
    llm_stats = df_numeric.groupby('llm')[numeric_metrics].agg(['mean', 'std', 'median', 'count']).round(2)
    display(llm_stats)
    if 'output_tables_path' in locals():
        llm_stats.to_csv(os.path.join(output_tables_path, "exp2_metrics_by_llm.csv"))
        print(f"Saved metrics by LLM table to {output_tables_path}")

else:
    print("No data available for LLM-based analysis.")


# In[ ]:


# --- TABLE: LLM vs. Prompt Type (Experiment) for Bloom's Level Scoring ---

print("\n=== TABLE: LLM vs. Prompt Type (Experiment) for Bloom's Level Scoring ===")

if 'df_numeric' in locals() and 'llm' in df_numeric.columns and 'experiment' in df_numeric.columns and 'blooms_level_score' in df_numeric.columns:
    llm_prompt_bloom = df_numeric.pivot_table(index='llm', columns='experiment', values='blooms_level_score', aggfunc=['mean', 'std', 'median']).round(2)
    display(llm_prompt_bloom)
    if 'output_tables_path' in locals():
        llm_prompt_bloom.to_csv(os.path.join(output_tables_path, "exp2_llm_vs_prompttype_bloomslevel.csv"))
        print(f"Saved LLM vs. Prompt Type Bloom's Level table to {output_tables_path}")

else:
    print("Not enough data for LLM vs. Prompt Type Bloom's Level table.")


# In[ ]:


# --- TABLE: Question Type vs. Subexperiment for Bloom's Level Scoring ---
print("\n=== TABLE: Question Type vs. Subexperiment for Bloom's Level Scoring ===")

if (
    'df_numeric' in locals() and 
    'experiment' in df_numeric.columns and 
    'question_type' in df_numeric.columns and 
    'blooms_level_score' in df_numeric.columns
):
    qt_exp_bloom = df_numeric.pivot_table(
        index='question_type',
        columns='experiment',
        values='blooms_level_score',
        aggfunc=['mean', 'std', 'median', 'count']
    ).round(2)
    display(qt_exp_bloom)
    if 'output_tables_path' in locals():
        qt_exp_bloom.to_csv(os.path.join(output_tables_path, "exp2_questiontype_vs_experiment_bloomslevel.csv"))
        print(f"Saved Question Type vs. Subexperiment Bloom's Level table to {output_tables_path}")
else:
    print("Not enough data for Question Type vs. Subexperiment Bloom's Level table.")


# # Inter-Student Reliability Analysis
# 
# Analysis of agreement between student evaluators on overlapping questions.

# In[ ]:


print("\n" + "="*60)
print("FLEISS' KAPPA INTER-RATER RELIABILITY ANALYSIS")
print("="*60)

from statsmodels.stats.inter_rater import fleiss_kappa

def make_global_question_id(row):
    if row['experiment'] == 'exp2a':
        return f"{row['experiment']}|{row['llm']}|{row['question_id']}|{row['question_type']}"
    elif row['experiment'] == 'exp2b':
        return f"{row['experiment']}|{row['llm']}|{row['bloom_original']}"
    elif row['experiment'] == 'exp2c':
        return f"{row['experiment']}|{row['llm']}|{row['bloom_original']}|{row['question_type']}"
    else:
        return None

df_numeric['global_question_id'] = df_numeric.apply(make_global_question_id, axis=1)

def kappa_level(k):
    if k < 0:
        return "Invalid"
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

def calculate_fleiss_kappa_all_questions(df, metrics, experiment_col='experiment'):
    results = []
    for exp in sorted(df[experiment_col].unique()):
        exp_df = df[df[experiment_col] == exp]
        for metric in metrics:
            pivot = exp_df.pivot_table(index='global_question_id', columns='student', values=metric)
            ratings_matrix = pivot.applymap(lambda x: max(1, min(10, int(round(x)))) if pd.notnull(x) else np.nan).values
            fleiss_table = np.zeros((ratings_matrix.shape[0], 10))
            for i, row in enumerate(ratings_matrix):
                for r in row:
                    if not np.isnan(r) and 1 <= r <= 10:
                        fleiss_table[i, int(r)-1] += 1
            all_identical = np.all((fleiss_table == np.max(fleiss_table, axis=1, keepdims=True)) | (fleiss_table == 0), axis=1)
            try:
                if np.all(all_identical):
                    kappa = 1.0
                else:
                    kappa = fleiss_kappa(fleiss_table)
            except Exception:
                kappa = np.nan
            results.append({
                'Experiment': exp,
                'Metric': metric_labels.get(metric, metric),
                'Fleiss_Kappa': kappa,
                'Agreement_Level': kappa_level(kappa) if not np.isnan(kappa) else 'No data',
                'N_Questions': ratings_matrix.shape[0]
            })
    return pd.DataFrame(results)

def calculate_fleiss_kappa_compact(df, metrics):
    results = []
    for metric in metrics:
        pivot = df.pivot_table(index='global_question_id', columns='student', values=metric)
        ratings_matrix = pivot.applymap(lambda x: max(1, min(10, int(round(x)))) if pd.notnull(x) else np.nan).values
        fleiss_table = np.zeros((ratings_matrix.shape[0], 10))
        for i, row in enumerate(ratings_matrix):
            for r in row:
                if not np.isnan(r) and 1 <= r <= 10:
                    fleiss_table[i, int(r)-1] += 1
        all_identical = np.all((fleiss_table == np.max(fleiss_table, axis=1, keepdims=True)) | (fleiss_table == 0), axis=1)
        try:
            if np.all(all_identical):
                kappa = 1.0
            else:
                kappa = fleiss_kappa(fleiss_table)
        except Exception:
            kappa = np.nan
        results.append({
            'Metric': metric_labels.get(metric, metric),
            'Fleiss_Kappa': kappa,
            'Agreement_Level': kappa_level(kappa) if not np.isnan(kappa) else 'No data',
            'N_Questions': ratings_matrix.shape[0]
        })
    return pd.DataFrame(results)

kappa_all_df = calculate_fleiss_kappa_all_questions(df_numeric, numeric_metrics)
print("\nFleiss' Kappa Calculation:")
display(kappa_all_df.round(4))
if 'output_tables_path' in locals():
    kappa_all_df.to_csv(os.path.join(output_tables_path, "exp2_fleiss_kappa_all_questions.csv"), index=False)
    print(f"Saved full Fleiss' Kappa table to {output_tables_path}")

kappa_compact_df = calculate_fleiss_kappa_compact(df_numeric, numeric_metrics)
print("\nFleiss' Kappa Calculation (ALL QUESTIONS, ALL EXPERIMENTS):")
display(kappa_compact_df.round(4))
if 'output_tables_path' in locals():
    kappa_compact_df.to_csv(os.path.join(output_tables_path, "exp2_fleiss_kappa_all_questions_compact.csv"), index=False)
    print(f"Saved compact Fleiss' Kappa table to {output_tables_path}")


# In[ ]:


#TODO add fleiss kappa between student pairs


# In[ ]:


def save_results():
    print("Saving key results (based on all ratings)...")
    
    if 'overall_stats' in locals() and not overall_stats.empty:
        overall_stats.to_csv(os.path.join(output_tables_path, "exp2_overall_statistics_all.csv"))
        print("Saved overall statistics (all ratings)")
    
    if 'exp_stats' in locals() and not exp_stats.empty:
        exp_stats.to_csv(os.path.join(output_tables_path, "exp2_experiment_statistics_all.csv"))
        print("Saved experiment statistics (all ratings)")
    
    if 'kappa_all_df' in locals() and not kappa_all_df.empty:
        kappa_all_df.to_csv(os.path.join(output_tables_path, "exp2_fleiss_kappa_all.csv"), index=False)
        print("Saved Fleiss' Kappa results (all ratings)")
    
    if 'kappa_compact_df' in locals() and not kappa_compact_df.empty:
        kappa_compact_df.to_csv(os.path.join(output_tables_path, "exp2_fleiss_kappa_all_compact.csv"), index=False)
        print("Saved compact Fleiss' Kappa results (all ratings)")
    
    print(f"\nResults saved to: {output_tables_path}")

# Execute save
save_results()

print(f"\n" + "="*60)
print("ANALYSIS COMPLETE - ALL RATINGS")
print("="*60)
print(f"Data loaded: {len(df_combined)} total evaluations")
print(f"Metrics analyzed: {len(metrics)}")
print(f"Students: {sorted(df_combined['student'].unique())}")
print(f"Experiments: {sorted(df_combined['experiment'].unique())}")

