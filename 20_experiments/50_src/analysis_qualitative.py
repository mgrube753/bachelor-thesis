"""
This is a discarded file which was used in 70_prior_exp_run/ to analyze (LLM-based) the quality of the questions in both experiments qualitatively.
It is not used anymore, as the qualitative analysis is now done by humans instead.
"""

import os
import pandas as pd
from constants import (
    PROMPT_TEMPLATES_PATH,
    INPUT_SOURCES_PATH,
    EXPERIMENTS_BASE_PATH,
    ANALYSES_PATH,
)
import concurrent.futures
from file_utils import load_txt
from api_calls import llm_generation
from api_config import init_clients
from tqdm import tqdm
import threading
from collections import defaultdict

evaluator_counters = defaultdict(int)
counter_lock = threading.Lock()


def inc_evaluator_count(evaluator_name):
    with counter_lock:
        evaluator_counters[evaluator_name] += 1


def reset_evaluator_count():
    with counter_lock:
        evaluator_counters.clear()
        for evaluator in ["openai", "anthropic"]:
            evaluator_counters[evaluator] = 0


def get_evaluator_progress():
    with counter_lock:
        if not evaluator_counters:
            return "Evaluation Progress"
        desc_parts = []
        for evaluator in sorted(evaluator_counters.keys()):
            count = evaluator_counters[evaluator]
            desc_parts.append(f"{evaluator}:{count}")
        return f"Evaluation [{' | '.join(desc_parts)}]"


def get_rubric(exp_name):
    rubric_file = (
        f"{exp_name}_rubric.md" if exp_name in ["exp1a", "exp1b"] else "exp2_rubric.md"
    )
    return load_txt(os.path.join(PROMPT_TEMPLATES_PATH, "evaluation", rubric_file))


def get_eval_prompt():
    return load_txt(os.path.join(PROMPT_TEMPLATES_PATH, "evaluation", "exp_eval.md"))


def get_source(source, layer, manipulated=False):
    source_dir = os.path.join(
        INPUT_SOURCES_PATH,
        source,
        "manipulated" if manipulated else ("common" if source == "script" else ""),
    )
    return load_txt(os.path.join(source_dir, f"layer{layer}.txt"))


def find_question(samples_path, pattern):
    for file in os.listdir(samples_path):
        if pattern in file and file.endswith(".txt"):
            return load_txt(os.path.join(samples_path, file))
    return None


def evaluate_single(clients, llm, question, context, rubric):
    prompt = (
        get_eval_prompt()
        .replace("{question_text}", question)
        .replace("{context_text}", context)
        .replace("{rubric_text}", rubric)
    )
    response = llm_generation(llm, clients, prompt, max_tokens=1200)
    result = [
        float(x.strip())
        for x in response.strip().split(",")
        if x.strip().replace(".", "").isdigit()
    ]
    inc_evaluator_count(llm)
    return result


def calculate_bloom_score(exp_name, bloom_rating, bloom_original=None):
    if exp_name == "exp2a":
        bloom_points = {1: 1.5, 2: 3.0, 3: 4.5, 4: 7.0, 5: 8.5, 6: 10.0}
        return bloom_points.get(int(bloom_rating), 0.0)

    elif exp_name in ["exp2b", "exp2c"]:
        if bloom_rating == bloom_original:
            return 10.0
        elif abs(bloom_rating - bloom_original) == 1:
            return 5.0
        else:
            return 0.0

    return 0.0


def process_exp1(exp_name, clients):
    print(f"\n[INFO] Processing {exp_name} with progress tracking")
    reset_evaluator_count()

    openai_csv_path = os.path.join(
        ANALYSES_PATH,
        "csv",
        "qualitative",
        "exp1",
        "experts",
        "expert_1",
        f"{exp_name}.csv",
    )
    anthropic_csv_path = os.path.join(
        ANALYSES_PATH,
        "csv",
        "qualitative",
        "exp1",
        "experts",
        "expert_2",
        f"{exp_name}.csv",
    )

    base_csv_path = os.path.join(
        ANALYSES_PATH, "csv", "initial", "exp1", f"{exp_name}.csv"
    )
    df_base = pd.read_csv(base_csv_path)

    samples_base = os.path.join(EXPERIMENTS_BASE_PATH, "70_samples", "exp1")
    run_folder = "run_a_content" if exp_name == "exp1a" else "run_b_error"
    rubric = get_rubric(exp_name)
    criteria = ["relevance", "clarity", "answerability", "challenging", "correctness"]

    def has_sample(row):
        samples_path = os.path.join(
            samples_base,
            run_folder,
            f"{row['prompt_type']}_prompt",
            row["llm"],
            row["input_source"].replace("_manipulated", ""),
        )
        return (
            os.path.exists(samples_path)
            and find_question(samples_path, f"layer{row['layer']}_question") is not None
        )

    df_filtered = df_base[df_base.apply(has_sample, axis=1)].copy()
    print(df_filtered)
    print(
        f"[INFO] {exp_name}: Processing {len(df_filtered)} sampled questions out of {len(df_base)} total"
    )

    def process_row(args):
        idx, row = args
        samples_path = os.path.join(
            samples_base,
            run_folder,
            f"{row['prompt_type']}_prompt",
            row["llm"],
            row["input_source"].replace("_manipulated", ""),
        )

        question = find_question(samples_path, f"layer{row['layer']}_question")
        context = get_source(
            row["input_source"].replace("_manipulated", ""),
            row["layer"],
            exp_name == "exp1b",
        )

        source_info = row["input_source"] + (
            "_manipulated"
            if exp_name == "exp1b" and not row["input_source"].endswith("_manipulated")
            else ""
        )
        print(
            f"[EVAL] {exp_name} - {row['llm']} - {source_info} layer{row['layer']} - {row['prompt_type']}_prompt"
        )

        openai_scores = evaluate_single(clients, "openai", question, context, rubric)
        anthropic_scores = evaluate_single(
            clients, "anthropic", question, context, rubric
        )

        return idx, openai_scores, anthropic_scores

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        futures = {
            executor.submit(process_row, row): row for row in df_filtered.iterrows()
        }

        with tqdm(
            total=len(df_filtered), desc=get_evaluator_progress(), unit="eval"
        ) as pbar:
            results = []
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                results.append(result)
                pbar.set_description(get_evaluator_progress())
                pbar.update(1)

    df_openai_filtered = df_filtered.copy()
    df_anthropic_filtered = df_filtered.copy()

    for criterion in criteria:
        df_openai_filtered[criterion] = None
        df_anthropic_filtered[criterion] = None

    for idx, openai_scores, anthropic_scores in results:
        if openai_scores and len(openai_scores) >= len(criteria):
            for i, criterion in enumerate(criteria[: len(openai_scores)]):
                df_openai_filtered.at[idx, criterion] = round(openai_scores[i], 1)

        if anthropic_scores and len(anthropic_scores) >= len(criteria):
            for i, criterion in enumerate(criteria[: len(anthropic_scores)]):
                df_anthropic_filtered.at[idx, criterion] = round(anthropic_scores[i], 1)

    os.makedirs(os.path.dirname(openai_csv_path), exist_ok=True)
    os.makedirs(os.path.dirname(anthropic_csv_path), exist_ok=True)

    df_openai_filtered.to_csv(openai_csv_path, index=False)
    df_anthropic_filtered.to_csv(anthropic_csv_path, index=False)


def process_exp2(exp_name, clients):
    print(f"\n[INFO] Processing {exp_name} with progress tracking")
    reset_evaluator_count()

    openai_csv_path = os.path.join(
        ANALYSES_PATH,
        "csv",
        "qualitative",
        "exp2",
        "students",
        "student_1",
        f"{exp_name}.csv",
    )
    anthropic_csv_path = os.path.join(
        ANALYSES_PATH,
        "csv",
        "qualitative",
        "exp2",
        "students",
        "student_2",
        f"{exp_name}.csv",
    )

    base_csv_path = os.path.join(
        ANALYSES_PATH, "csv", "initial", "exp2", f"{exp_name}.csv"
    )
    df_base = pd.read_csv(base_csv_path)

    samples_base = os.path.join(EXPERIMENTS_BASE_PATH, "70_samples", "exp2")
    run_folders = {"exp2a": "run_a_type", "exp2b": "run_b_bloom", "exp2c": "run_c_both"}
    rubric = get_rubric(exp_name)
    context = get_source("tanenbaum", 2)

    criteria = ["relevance", "clarity", "answerability", "challenging", "bloom_rating"]

    if exp_name == "exp2a" and "question_id" not in df_base.columns:
        df_base["question_id"] = (
            df_base.groupby(["llm", "question_type"]).cumcount() + 1
        )

    def has_sample(row):
        if exp_name == "exp2a":
            samples_path = os.path.join(
                samples_base,
                run_folders[exp_name],
                row["llm"],
                row["question_type"].lower().replace("-", "_"),
            )
            question_file = f"question_{row['question_id']}.txt"
            return os.path.exists(os.path.join(samples_path, question_file))
        elif exp_name == "exp2b":
            samples_path = os.path.join(samples_base, run_folders[exp_name], row["llm"])
            pattern = f"question_{row['bloom_original']}"
        else:
            samples_path = os.path.join(
                samples_base,
                run_folders[exp_name],
                row["llm"],
                row["question_type"].lower().replace("-", "_"),
            )
            pattern = f"question_{row['bloom_original']}"

        return (
            os.path.exists(samples_path)
            and find_question(samples_path, pattern) is not None
        )

    df_filtered = df_base[df_base.apply(has_sample, axis=1)].copy()
    print(df_filtered)
    print(
        f"[INFO] {exp_name}: Processing {len(df_filtered)} sampled questions out of {len(df_base)} total"
    )

    def process_row(args):
        idx, row = args

        if exp_name == "exp2a":
            samples_path = os.path.join(
                samples_base,
                run_folders[exp_name],
                row["llm"],
                row["question_type"].lower().replace("-", "_"),
            )
            pattern = f"question_{row['question_id']}"
        elif exp_name == "exp2b":
            samples_path = os.path.join(samples_base, run_folders[exp_name], row["llm"])
            pattern = f"question_{row['bloom_original']}"
        else:
            samples_path = os.path.join(
                samples_base,
                run_folders[exp_name],
                row["llm"],
                row["question_type"].lower().replace("-", "_"),
            )
            pattern = f"question_{row['bloom_original']}"

        question = find_question(samples_path, pattern)

        openai_scores = evaluate_single(clients, "openai", question, context, rubric)
        claude_scores = evaluate_single(clients, "anthropic", question, context, rubric)

        return idx, openai_scores, claude_scores

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        futures = {
            executor.submit(process_row, row): row for row in df_filtered.iterrows()
        }

        with tqdm(
            total=len(df_filtered), desc=get_evaluator_progress(), unit="eval"
        ) as pbar:
            results = []
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                results.append(result)
                pbar.set_description(get_evaluator_progress())
                pbar.update(1)

    df_openai_filtered = df_filtered.copy()
    df_anthropic_filtered = df_filtered.copy()

    for criterion in criteria:
        df_openai_filtered[criterion] = None
        df_anthropic_filtered[criterion] = None

    df_openai_filtered["bloom_score"] = None
    df_anthropic_filtered["bloom_score"] = None

    for idx, openai_scores, claude_scores in results:
        if openai_scores and len(openai_scores) >= len(criteria):
            for i, criterion in enumerate(criteria[: len(openai_scores)]):
                if criterion == "bloom_rating":
                    df_openai_filtered.at[idx, criterion] = int(openai_scores[i])
                else:
                    df_openai_filtered.at[idx, criterion] = round(openai_scores[i], 1)

            if len(openai_scores) >= 5:
                bloom_rating_openai = openai_scores[4]
                if exp_name == "exp2a":
                    bloom_score_openai = calculate_bloom_score(
                        exp_name, bloom_rating_openai
                    )
                else:
                    bloom_original = df_filtered.loc[idx].get("bloom_original")
                    bloom_score_openai = calculate_bloom_score(
                        exp_name, bloom_rating_openai, bloom_original
                    )
                df_openai_filtered.at[idx, "bloom_score"] = bloom_score_openai

        if claude_scores and len(claude_scores) >= len(criteria):
            for i, criterion in enumerate(criteria[: len(claude_scores)]):
                if criterion == "bloom_rating":
                    df_anthropic_filtered.at[idx, criterion] = int(claude_scores[i])
                else:
                    df_anthropic_filtered.at[idx, criterion] = round(
                        claude_scores[i], 1
                    )

            if len(claude_scores) >= 5:
                bloom_rating_claude = claude_scores[4]
                if exp_name == "exp2a":
                    bloom_score_claude = calculate_bloom_score(
                        exp_name, bloom_rating_claude
                    )
                else:
                    bloom_original = df_filtered.loc[idx].get("bloom_original")
                    bloom_score_claude = calculate_bloom_score(
                        exp_name, bloom_rating_claude, bloom_original
                    )
                df_anthropic_filtered.at[idx, "bloom_score"] = bloom_score_claude

    os.makedirs(os.path.dirname(openai_csv_path), exist_ok=True)
    os.makedirs(os.path.dirname(anthropic_csv_path), exist_ok=True)

    df_openai_filtered.to_csv(openai_csv_path, index=False)
    df_anthropic_filtered.to_csv(anthropic_csv_path, index=False)


def main():
    clients = init_clients()

    for exp in ["exp1a", "exp1b", "exp2a", "exp2b", "exp2c"]:
        print(f"[INFO] Processing {exp}")
        (process_exp1 if exp.startswith("exp1") else process_exp2)(exp, clients)


if __name__ == "__main__":
    main()
