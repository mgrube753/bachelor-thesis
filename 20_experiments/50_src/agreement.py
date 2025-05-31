import numpy as np
import pandas as pd
from sklearn.metrics import cohen_kappa_score


def interpret_kappa(k):
    if k < 0:
        return "Poor"
    elif k < 0.20:
        return "Slight"
    elif k < 0.40:
        return "Fair"
    elif k < 0.60:
        return "Moderate"
    elif k < 0.80:
        return "Substantial"
    else:
        return "Almost Perfect"


def analyze_agreement(llm1, llm2, expert):
    llm1 = np.array(llm1)
    llm2 = np.array(llm2)
    expert = np.array(expert)

    llm_avg = np.round((llm1 + llm2) / 2, 1)
    llm_cat = (llm_avg * 10).astype(int)
    exp_cat = (expert * 10).astype(int)

    # using weighted cohen kappa
    kappa = cohen_kappa_score(exp_cat, llm_cat, weights="linear")

    return {
        "kappa": kappa,
        "interpretation": interpret_kappa(kappa),
        "llm_avg": llm_avg,
    }


def main():
    llm1 = np.array([8, 6, 9, 3, 7, 5, 9, 8, 2, 6])
    llm2 = np.array([7, 7, 8, 4, 6, 6, 8, 8, 3, 5])
    expert = np.array([8, 6, 9, 3, 7, 5, 9, 8, 3, 6])

    result = analyze_agreement(llm1, llm2, expert)

    df = pd.DataFrame(
        {
            "LLM1": llm1,
            "LLM2": llm2,
            "LLM_Avg": result["llm_avg"],
            "Expert": expert,
            "Diff": result["llm_avg"] - expert,
        }
    )

    print("=== LLM vs Expert Agreement ===\n")
    print("Ratings (0-10 scale):")
    print(df.to_string(index=False, float_format="%.1f"))
    print()
    print(f"Cohen's Kappa: {result['kappa']:.3f}")
    print(f"Interpretation: {result['interpretation']}")


if __name__ == "__main__":
    main()
