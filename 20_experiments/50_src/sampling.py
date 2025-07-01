import os
import random
import shutil
import pandas as pd
from constants import EXP1_PATH, EXP2_PATH, EXPERIMENTS_BASE_PATH


def sample_questions(src_path, dest_path, pattern, sample_size=3):
    files = [f for f in os.listdir(src_path) if pattern in f and f.endswith(".txt")]
    if len(files) < sample_size:
        print(f"[WARNING] Only {len(files)} questions available in {src_path}")
        sample_size = len(files)
    if sample_size == 0:
        return []

    sampled = random.sample(files, sample_size)
    os.makedirs(dest_path, exist_ok=True)
    for file in sampled:
        shutil.copy2(os.path.join(src_path, file), os.path.join(dest_path, file))
    return sampled


def walk_and_sample(base_path, sample_base, exp_name, pattern, sample_size=3):
    print(f"[INFO] Sampling {exp_name} questions ({sample_size} per condition)...")
    for root, _, files in os.walk(base_path):
        if any(pattern in f and f.endswith(".txt") for f in files):
            rel_path = os.path.relpath(root, base_path)
            dest_path = os.path.join(sample_base, exp_name, rel_path)
            sampled = sample_questions(root, dest_path, pattern, sample_size)
            if sampled:
                print(f"         {rel_path}: {len(sampled)} questions sampled")


def parse_file_path(parts):
    runs_map = {"run_a_type": "exp2a", "run_b_bloom": "exp2b", "run_c_both": "exp2c"}

    if parts[0] == "exp1":
        return {
            "exp_name": "exp1a" if parts[1] == "run_a_content" else "exp1b",
            "prompt_type": parts[2].replace("_prompt", ""),
            "llm": parts[3],
            "input_source": parts[4],
            "layer": int(parts[5].split("_")[0].replace("layer", "")),
        }
    elif parts[0] == "exp2" and parts[1] in runs_map:
        exp_name = runs_map[parts[1]]
        record = {"exp_name": exp_name, "llm": parts[2], "layer": 2}

        if exp_name == "exp2a":
            record["question_type"] = parts[3].replace("_", "-")
            record["question_id"] = int(parts[4].split("_")[1].replace(".txt", ""))
        elif exp_name == "exp2b":
            record["bloom_original"] = int(parts[3].split("_")[1].replace(".txt", ""))
        elif exp_name == "exp2c":
            record["question_type"] = parts[3].replace("_", "-")
            record["bloom_original"] = int(parts[4].split("_")[1].replace(".txt", ""))
        return record
    return None


def generate_expert_csvs(sample_base, csv_path):
    print("\n[INFO] Generating CSV files for expert evaluation from samples...")

    records = []
    for root, _, files in os.walk(sample_base):
        for file in files:
            if file.endswith(".txt"):
                parts = os.path.relpath(os.path.join(root, file), sample_base).split(
                    os.sep
                )
                try:
                    record = parse_file_path(parts)
                    if record:
                        records.append(record)
                except (IndexError, ValueError):
                    print(f"[WARNING] Could not parse path: {os.path.join(*parts)}")

    if not records:
        return

    records.sort(
        key=lambda r: (
            r.get("exp_name", ""),
            r.get("llm", ""),
            r.get("input_source", ""),
            r.get("prompt_type", ""),
            r.get("layer", 0),
            r.get("question_type", ""),
            r.get("question_id", 0),
            r.get("bloom_original", 0),
        )
    )

    df = pd.DataFrame(records)

    for exp_name, group in df.groupby("exp_name"):
        group.to_csv(os.path.join(csv_path, f"{exp_name}.csv"), index=False)
        print(f"  - Saved: {os.path.join(csv_path, f'{exp_name}.csv')}")

    # Generate special hint files for exp1a and exp1b
    print("\n[INFO] Generating special hint CSV files for exp1a and exp1b...")
    hints_path = os.path.join(csv_path, "qualitative", "hint_csvs_exp1")
    os.makedirs(hints_path, exist_ok=True)

    hint_df = df[df["exp_name"].isin(["exp1a", "exp1b"])].copy()

    if not hint_df.empty:
        output_columns = [
            "llm",
            "prompt_type",
            "input_source",
            "layer",
            "question_id",
        ]

        for exp_name, group in hint_df.groupby("exp_name"):
            output_filename = os.path.join(hints_path, f"{exp_name}.csv")
            group_to_save = group[output_columns]
            group_to_save.to_csv(output_filename, index=False)
            print(f"  - Saved hint file: {output_filename}")

        # Exp1: Save to expert_1 through expert_5 folders
    exp1_data = df[df["exp_name"].isin(["exp1a", "exp1b"])]
    for exp_name, group in exp1_data.groupby("exp_name"):
        output_df = group[["input_source", "layer"]].copy()

        output_df = output_df.reset_index(drop=True)
        output_df["sample_id"] = [f"{i+1:03d}" for i in range(len(output_df))]
        output_df["sample_id"] = output_df["sample_id"].astype(str)

        # Different categories for exp1a and exp1b
        if exp_name == "exp1a":
            categories = [
                "relevance",
                "clarity",
                "answerability",
                "challenging",
                "correctness",
                "value",
                "language",
                "answer_problems",
                "comments",
            ]
        else:  # exp1b
            categories = [
                "relevance",
                "clarity",
                "answerability",
                "challenging",
                "manipulation_handling",
                "value",
                "language",
                "answer_problems",
                "comments",
            ]

        for col in categories:
            output_df[col] = ""

        for i in range(1, 6):
            expert_dir = os.path.join(csv_path, "qualitative", f"expert_{i}")
            os.makedirs(expert_dir, exist_ok=True)
            output_df.to_csv(os.path.join(expert_dir, f"{exp_name}.csv"), index=False)

    # Exp2: Save to expert_anthropic and expert_openai folders
    exp2_data = df[df["exp_name"].isin(["exp2a", "exp2b", "exp2c"])]
    for exp_name, group in exp2_data.groupby("exp_name"):
        output_df = group[["llm"]].copy()
        output_df["input_source"] = "tanenbaum"

        if exp_name == "exp2a" and "question_id" in group.columns:
            output_df["question_id"] = group["question_id"].astype(int)
        elif exp_name in ["exp2b", "exp2c"] and "bloom_original" in group.columns:
            output_df["bloom_original"] = group["bloom_original"].astype(int)

        output_df["layer"] = group["layer"]

        for col in [
            "relevance",
            "clarity",
            "answerability",
            "challenging",
            "bloom_rating",
            "bloom_score",
        ]:
            output_df[col] = ""

        for expert_type in ["expert_anthropic", "expert_openai"]:
            expert_dir = os.path.join(csv_path, "qualitative", expert_type)
            os.makedirs(expert_dir, exist_ok=True)
            output_df.to_csv(os.path.join(expert_dir, f"{exp_name}.csv"), index=False)


def find_file(samples, exp, row):
    if exp.startswith("exp1"):
        run = "run_a_content" if exp == "exp1a" else "run_b_error"
        source = row["input_source"].replace("_manipulated", "")
        dir_path = os.path.join(
            samples, "exp1", run, f"{row['prompt_type']}_prompt", row["llm"], source
        )
        if os.path.exists(dir_path):
            pattern = f"layer{int(row['layer'])}_question"
            for f in os.listdir(dir_path):
                if pattern in f and f.endswith(".txt"):
                    return os.path.join(dir_path, f)
    else:
        runs = {"exp2a": "run_a_type", "exp2b": "run_b_bloom", "exp2c": "run_c_both"}
        run = runs.get(exp)
        if run:
            llm = row["llm"]
            if exp == "exp2a":
                qtype = row["question_type"].lower().replace("-", "_")
                dir_path = os.path.join(samples, "exp2", run, llm, qtype)
                filename = f"question_{int(row['question_id'])}.txt"
            elif exp == "exp2b":
                dir_path = os.path.join(samples, "exp2", run, llm)
                filename = f"question_{int(row['bloom_original'])}.txt"
            else:
                qtype = row["question_type"].lower().replace("-", "_")
                dir_path = os.path.join(samples, "exp2", run, llm, qtype)
                filename = f"question_{int(row['bloom_original'])}.txt"

            file_path = os.path.join(dir_path, filename)
            if os.path.exists(file_path):
                return file_path
    return None


def get_source_type(exp, row):
    if exp.startswith("exp1"):
        src = row.get("input_source", "")
        if "manipulated" in src or exp == "exp1b":
            return "script_manipulated"
        if "transcript" in src:
            return "transcript"
        if "script" in src:
            return "script"
        if "tanenbaum" in src:
            return "tanenbaum"
        return "unknown"
    return "tanenbaum"


def rename_samples(samples, csv_path, output_path):
    print("\n[INFO] Renaming samples for manual inspection...")

    for prefix in ["exp1", "exp2"]:
        csvs = [
            f
            for f in os.listdir(csv_path)
            if f.startswith(prefix) and f.endswith(".csv")
        ]
        for csv in sorted(csvs):
            count = 1
            exp = csv.replace(".csv", "")
            df = pd.read_csv(os.path.join(csv_path, csv))
            exp_dir = os.path.join(output_path, exp)
            os.makedirs(exp_dir, exist_ok=True)

            for _, row in df.iterrows():
                src = find_file(samples, exp, row)
                if src and os.path.exists(src):
                    source_type = get_source_type(exp, row)
                    layer = row.get("layer", 2)
                    new_name = f"{count:03d}_{source_type}_{layer}.txt"
                    shutil.copy2(src, os.path.join(exp_dir, new_name))
                    print(f"  {os.path.basename(src)} -> {new_name}")
                    count += 1


def main():
    random.seed(2025)
    base = EXPERIMENTS_BASE_PATH
    sample_base = os.path.join(base, "70_samples")
    csv_path = os.path.join(base, "60_analyses", "csv_files")
    output_path = os.path.join(base, "80_questions_renamed")

    shutil.rmtree(sample_base, ignore_errors=True)
    shutil.rmtree(os.path.join(csv_path, "qualitative"), ignore_errors=True)
    shutil.rmtree(output_path, ignore_errors=True)

    walk_and_sample(EXP1_PATH, sample_base, "exp1", "_question", 2)
    walk_and_sample(EXP2_PATH, sample_base, "exp2", "question_", 2)
    print(f"[INFO] Sampling completed. Results: {sample_base}")

    generate_expert_csvs(sample_base, csv_path)
    rename_samples(sample_base, csv_path, output_path)

    # Cleanup temporary CSV files
    for exp_file in ["exp1a.csv", "exp1b.csv", "exp2a.csv", "exp2b.csv", "exp2c.csv"]:
        exp_file_path = os.path.join(csv_path, exp_file)
        if os.path.exists(exp_file_path):
            os.remove(exp_file_path)

    print(
        f"\nDone. Qualitative Analysis CSVs: {csv_path}/qualitative/ | Renamed samples: {output_path}"
    )


if __name__ == "__main__":
    main()
