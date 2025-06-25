import numpy as np
import pandas as pd
import os
import datetime
from statsmodels.stats.inter_rater import fleiss_kappa
from constants import EXPERIMENTS_BASE_PATH


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


def sim_ratings(n_items, n_experts=5, seed=42):
    np.random.seed(seed)

    params = {
        "relevance": (7.5, 1.2),
        "clarity": (6.8, 1.5),
        "answerability": (7.2, 1.3),
        "challenging": (6.5, 1.8),
        "correctness": (7.8, 1.0),
        "manipulation_handling": (6.0, 2.0),
    }

    ratings = {}
    for cat, (mean, std) in params.items():
        base_scores = np.random.normal(mean, std, n_items)

        cat_ratings = []
        for item in range(n_items):
            item_ratings = []
            for expert in range(n_experts):
                score = base_scores[item] + np.random.normal(0, 0.4)
                score = int(np.clip(round(score), 1, 10))
                item_ratings.append(score)
            cat_ratings.append(item_ratings)

        ratings[cat] = cat_ratings

    return ratings


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


def analyze_exp1():
    csv_path = os.path.join(
        EXPERIMENTS_BASE_PATH, "60_eval", "csv_files", "qualitative"
    )

    results = []

    for exp in ["exp1a", "exp1b"]:
        print(f"\n=== {exp.upper()} ===")

        cats = ["relevance", "clarity", "answerability", "challenging"]
        if exp == "exp1a":
            cats.append("correctness")
        else:
            cats.append("manipulation_handling")

        csv_file = os.path.join(csv_path, "expert_1", f"{exp}.csv")
        if not os.path.exists(csv_file):
            print(f"CSV not found: {csv_file}")
            continue

        n_items = len(pd.read_csv(csv_file))
        print(f"Items: {n_items}")

        seed = 42 if exp == "exp1a" else 123
        ratings = sim_ratings(n_items, seed=seed)

        for cat in cats:
            matrix = ratings[cat]
            table = ratings_to_fleiss_table(matrix)
            kappa = fleiss_kappa(table)
            level = kappa_level(kappa)

            arr = np.array(matrix)
            mean_rating = np.mean(arr)
            std_rating = np.std(arr)

            results.append(
                {
                    "Experiment": exp,
                    "Category": cat,
                    "Kappa": kappa,
                    "Level": level,
                    "Mean": mean_rating,
                    "Std": std_rating,
                }
            )

            print(
                f"{cat:18} | κ={kappa:.3f} | {level:12} | μ={mean_rating:.1f}±{std_rating:.1f}"
            )

    return pd.DataFrame(results)


def save_markdown_report(df, csv_path):
    md_content = f"""# Experiment 1: Inter-Rater Agreement

**Erstellt:** {datetime.datetime.now().strftime('%d.%m.%Y %H:%M')}  
**Methode:** Fleiss' Kappa mit simulierten Expertenratings  
**Experten:** 5 pro Subexperiment  
**Bewertungsskala:** 1-10 (ganzzahlig)  

## Ergebnisse

"""

    for exp in ["exp1a", "exp1b"]:
        exp_data = df[df["Experiment"] == exp]
        if exp_data.empty:
            continue

        exp_name = (
            "Exp1a (Inhaltstreue)" if exp == "exp1a" else "Exp1b (Fehlerfortpflanzung)"
        )
        md_content += f"### {exp_name}\n\n"
        md_content += "| Kategorie | Kappa | Bewertung | Mittelwert | Std |\n"
        md_content += "|-----------|-------|-----------|------------|-----|\n"

        for _, row in exp_data.iterrows():
            md_content += f"| {row['Category']} | {row['Kappa']:.3f} | {row['Level']} | {row['Mean']:.1f} | {row['Std']:.1f} |\n"

        md_content += "\n"

    md_content += "## Zusammenfassung\n\n"
    overall_kappa = df["Kappa"].mean()
    md_content += f"**Durchschnittliches Kappa:** {overall_kappa:.3f}\n\n"

    md_content += "**Kappa-Interpretation:**\n"
    md_content += "- < 0.20: Gering\n"
    md_content += "- 0.20-0.40: Schwach\n"
    md_content += "- 0.41-0.60: Moderat\n"
    md_content += "- 0.61-0.80: Beträchtlich\n"
    md_content += "- 0.81-1.00: Fast perfekt\n"

    qualitative_path = os.path.join(
        EXPERIMENTS_BASE_PATH, "..", "40_evaluation", "exp1", "qualitative"
    )
    os.makedirs(qualitative_path, exist_ok=True)
    output_file = os.path.join(qualitative_path, "agreement_analysis.md")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"\nMarkdown-Bericht gespeichert: {output_file}")
    return output_file


def main():
    print("=" * 60)
    print("EXPERIMENT 1 INTER-RATER AGREEMENT (Simulated)")
    print("=" * 60)

    df = analyze_exp1()

    print(f"\n=== RESULTS ===")
    print(df.to_string(index=False, float_format="%.3f"))

    print(f"\n=== BY CATEGORY ===")
    cat_summary = df.groupby("Category")["Kappa"].agg(["mean", "std"]).round(3)
    print(cat_summary)

    print(f"\n=== BY EXPERIMENT ===")
    exp_summary = df.groupby("Experiment")["Kappa"].agg(["mean", "std"]).round(3)
    print(exp_summary)

    csv_path = os.path.join(
        EXPERIMENTS_BASE_PATH, "60_eval", "csv_files", "qualitative"
    )
    save_markdown_report(df, csv_path)


if __name__ == "__main__":
    main()
