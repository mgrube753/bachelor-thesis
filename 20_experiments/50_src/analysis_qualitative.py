import os
import pandas as pd
import constants
import concurrent.futures
from file_utils import load_txt
from api_calls import llm_generation
from api_config import init_clients


def get_rubric(exp_name):
    rubric_file = (
        f"{exp_name}_rubric.md" if exp_name in ["exp1a", "exp1b"] else "exp2_rubric.md"
    )
    return load_txt(
        os.path.join(constants.PROMPT_TEMPLATES_PATH, "evaluation", rubric_file)
    )


def get_eval_prompt():
    return load_txt(
        os.path.join(constants.PROMPT_TEMPLATES_PATH, "evaluation", "exp_eval.md")
    )


def get_source(source, layer, manipulated=False):
    source_dir = os.path.join(
        constants.INPUT_SOURCES_PATH,
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
    return [
        float(x.strip())
        for x in response.strip().split(",")
        if x.strip().replace(".", "").isdigit()
    ]


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
    csv_path = os.path.join(constants.EVAL_PATH, "csv_files", "auto", f"{exp_name}.csv")
    df = pd.read_csv(csv_path)
    samples_base = os.path.join(constants.EXPERIMENTS_BASE_PATH, "70_samples", "exp1")
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

    df_filtered = df[df.apply(has_sample, axis=1)].copy()
    print(df_filtered)
    print(
        f"[INFO] {exp_name}: Processing {len(df_filtered)} sampled questions out of {len(df)} total"
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

        scores = evaluate_single(clients, "anthropic", question, context, rubric)
        return idx, scores if len(scores) == 5 else None

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(process_row, df_filtered.iterrows()))

    for idx, scores in results:
        if scores:
            for i, criterion in enumerate(criteria):
                df.at[idx, criterion] = round(scores[i], 1)

    df.to_csv(csv_path, index=False)


def process_exp2(exp_name, clients):
    csv_path = os.path.join(constants.EVAL_PATH, "csv_files", "auto", f"{exp_name}.csv")
    df = pd.read_csv(csv_path)
    samples_base = os.path.join(constants.EXPERIMENTS_BASE_PATH, "70_samples", "exp2")
    run_folders = {"exp2a": "run_a_type", "exp2b": "run_b_bloom", "exp2c": "run_c_both"}
    rubric = get_rubric(exp_name)
    context = get_source("tanenbaum", 2)

    criteria = ["relevance", "clarity", "answerability", "challenging", "bloom_rating"]

    if exp_name == "exp2a" and "question_id" not in df.columns:
        df["question_id"] = df.groupby(["llm", "question_type"]).cumcount() + 1

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

    df_filtered = df[df.apply(has_sample, axis=1)].copy()
    print(df_filtered)
    print(
        f"[INFO] {exp_name}: Processing {len(df_filtered)} sampled questions out of {len(df)} total"
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
            print(
                f"[EVAL] {exp_name} - {row['llm']} - tanenbaum layer2 - {row['question_type']}"
            )
        elif exp_name == "exp2b":
            samples_path = os.path.join(samples_base, run_folders[exp_name], row["llm"])
            pattern = f"question_{row['bloom_original']}"
            bloom_level = (
                constants.BLOOM_LEVELS_ORDERED[row["bloom_original"] - 1]
                if row["bloom_original"] <= len(constants.BLOOM_LEVELS_ORDERED)
                else f"bloom_{row['bloom_original']}"
            )
            print(
                f"[EVAL] {exp_name} - {row['llm']} - tanenbaum layer2 - {bloom_level}"
            )
        else:
            samples_path = os.path.join(
                samples_base,
                run_folders[exp_name],
                row["llm"],
                row["question_type"].lower().replace("-", "_"),
            )
            pattern = f"question_{row['bloom_original']}"
            bloom_level = (
                constants.BLOOM_LEVELS_ORDERED[row["bloom_original"] - 1]
                if row["bloom_original"] <= len(constants.BLOOM_LEVELS_ORDERED)
                else f"bloom_{row['bloom_original']}"
            )
            print(
                f"[EVAL] {exp_name} - {row['llm']} - tanenbaum layer2 - {row['question_type']} - {bloom_level}"
            )

        question = find_question(samples_path, pattern)
        scores = evaluate_single(clients, "openai", question, context, rubric)
        return idx, scores if len(scores) >= len(criteria) else None

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(process_row, df_filtered.iterrows()))

    for idx, scores in results:
        if scores:
            row = df_filtered.loc[idx]

            for i, criterion in enumerate(criteria):
                if i < len(scores):
                    df.at[idx, criterion] = round(scores[i], 1)

            if len(scores) >= 5:
                bloom_rating = scores[4]

                if exp_name == "exp2a":
                    bloom_score = calculate_bloom_score(exp_name, bloom_rating)
                else:
                    bloom_original = row.get("bloom_original")
                    bloom_score = calculate_bloom_score(
                        exp_name, bloom_rating, bloom_original
                    )

                df.at[idx, "bloom_score"] = bloom_score

    df.to_csv(csv_path, index=False)


def main():
    clients = init_clients()

    for exp in ["exp1a", "exp1b", "exp2a", "exp2b", "exp2c"]:
        print(f"[INFO] Processing {exp}")
        (process_exp1 if exp.startswith("exp1") else process_exp2)(exp, clients)


if __name__ == "__main__":
    main()
