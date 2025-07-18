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
        if "complex_prompt_no_source" in root:
            continue

        if any(pattern in f and f.endswith(".txt") for f in files):
            rel_path = root.replace(base_path, "").lstrip(os.sep)
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
            record["question_type"] = parts[3].replace("-", "_")
            record["question_id"] = int(parts[4].split("_")[1].replace(".txt", ""))
        elif exp_name == "exp2b":
            record["bloom_original"] = int(parts[3].split("_")[1].replace(".txt", ""))
        elif exp_name == "exp2c":
            record["question_type"] = parts[3].replace("-", "_")
            record["bloom_original"] = int(parts[4].split("_")[1].replace(".txt", ""))
        return record
    return None


def generate_expert_csvs(sample_base, csv_path):
    print("\n[INFO] Generating CSV files for expert evaluation from samples...")

    records = []
    for root, _, files in os.walk(sample_base):
        for file in files:
            if file.endswith(".txt"):
                # Calculate relative path manually to avoid getcwd issues
                full_path = os.path.join(root, file)
                rel_path = full_path.replace(sample_base, "").lstrip(os.sep)
                parts = rel_path.split(os.sep)
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

    # Ensure integer columns are properly typed
    if "question_id" in df.columns:
        df["question_id"] = df["question_id"].astype("Int64")
    if "bloom_original" in df.columns:
        df["bloom_original"] = df["bloom_original"].astype("Int64")
    if "layer" in df.columns:
        df["layer"] = df["layer"].astype("Int64")

    # Generate hint files for exp1
    print("\n[INFO] Generating hint CSV files for exp1...")
    exp1_hint_data = df[df["exp_name"].isin(["exp1a", "exp1b"])].copy()

    if not exp1_hint_data.empty:
        output_columns = ["llm", "prompt_type", "input_source", "layer"]

        for exp_name, group in exp1_hint_data.groupby("exp_name"):
            hints_path = os.path.join(
                csv_path, "qualitative", "exp1", "hints", f"{exp_name}_hints.csv"
            )
            os.makedirs(os.path.dirname(hints_path), exist_ok=True)
            group_to_save = group[output_columns]
            group_to_save.to_csv(hints_path, index=False)
            print(f"  - Saved hint file: {os.path.basename(hints_path)}")

    # Generate hint files for exp2
    print("\n[INFO] Generating hint CSV files for exp2...")
    exp2_hint_data = df[df["exp_name"].isin(["exp2a", "exp2b", "exp2c"])].copy()

    if not exp2_hint_data.empty:
        for exp_name, group in exp2_hint_data.groupby("exp_name"):
            hints_path = os.path.join(
                csv_path, "qualitative", "exp2", "hints", f"{exp_name}_hints.csv"
            )
            os.makedirs(os.path.dirname(hints_path), exist_ok=True)

            if exp_name == "exp2a":
                output_columns = ["llm", "question_id", "question_type"]
            elif exp_name == "exp2b":
                output_columns = ["llm", "bloom_original"]
            else:  # exp2c
                output_columns = ["llm", "bloom_original", "question_type"]

            group_to_save = group[output_columns]
            group_to_save.to_csv(hints_path, index=False)
            print(f"  - Saved hint file: {os.path.basename(hints_path)}")

    # Exp1: Save to expert_1 through expert_5 folders
    exp1_data = df[df["exp_name"].isin(["exp1a", "exp1b"])]
    for exp_name, group in exp1_data.groupby("exp_name"):
        output_df = group[["input_source", "layer"]].copy()

        output_df = output_df.reset_index(drop=True)
        output_df["sample_id"] = [f"{i+1:03d}" for i in range(len(output_df))]

        if exp_name == "exp1a":
            categories = [
                "relevance",
                "clarity",
                "answerability",
                "challenging",
                "value",
                "language",
                "correctness",
                "answer_problems",
                "comments",
            ]
        else:
            categories = [
                "relevance",
                "clarity",
                "answerability",
                "challenging",
                "value",
                "language",
                "manipulation_handling",
                "answer_problems",
                "comments",
            ]

        for col in categories:
            output_df[col] = ""

        for i in range(1, 6):
            expert_dir = os.path.join(
                csv_path, "qualitative", "exp1", "experts", f"expert_{i}"
            )
            os.makedirs(expert_dir, exist_ok=True)
            output_df.to_csv(os.path.join(expert_dir, f"{exp_name}.csv"), index=False)

    # Exp2: Save to student folders (only evaluation columns, no sensitive data)
    exp2_data = df[df["exp_name"].isin(["exp2a", "exp2b", "exp2c"])]
    for exp_name, group in exp2_data.groupby("exp_name"):
        output_df = pd.DataFrame()
        output_df["sample_id"] = [f"{i+1:03d}" for i in range(len(group))]

        for col in [
            "relevance",
            "clarity",
            "answerability",
            "challenging",
            "value",
            "language",
            "bloom_rating",
            "answer_problems",
            "comments",
        ]:
            output_df[col] = ""

        for i in range(1, 4):
            student_dir = os.path.join(
                csv_path, "qualitative", "exp2", "students", f"student_{i}"
            )
            os.makedirs(student_dir, exist_ok=True)
            output_df.to_csv(os.path.join(student_dir, f"{exp_name}.csv"), index=False)


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
    return "script"


def rename_samples(samples, csv_path, output_path):
    print("\n[INFO] Renaming samples for manual inspection...")

    # Look for initial CSV files in the new structure
    for exp_prefix in ["exp1", "exp2"]:
        exp_csv_dir = os.path.join(csv_path, "initial", exp_prefix)
        if not os.path.exists(exp_csv_dir):
            continue

        csvs = [
            f
            for f in os.listdir(exp_csv_dir)
            if f.startswith(exp_prefix) and f.endswith(".csv")
        ]
        for csv in sorted(csvs):
            count = 1
            exp = csv.replace(".csv", "")
            df = pd.read_csv(os.path.join(exp_csv_dir, csv))
            exp_dir = os.path.join(output_path, exp)
            os.makedirs(exp_dir, exist_ok=True)

            for _, row in df.iterrows():
                src = find_file(samples, exp, row)
                if src and os.path.exists(src):
                    source_type = get_source_type(exp, row)
                    if exp.startswith("exp1"):
                        layer = row.get("layer", 2)
                        new_name = f"{count:03d}_{source_type}_{layer}.txt"
                    else:  # exp2
                        new_name = f"{count:03d}_{source_type}_all.txt"
                    shutil.copy2(src, os.path.join(exp_dir, new_name))
                    print(f"  {os.path.basename(src)} -> {new_name}")
                    count += 1


def main():
    random.seed(2025)
    base = EXPERIMENTS_BASE_PATH
    sample_base = os.path.join(base, "70_samples")
    csv_path = os.path.join(base, "60_analyses", "csv")
    output_path = os.path.join(base, "80_samples_renamed")

    # Ensure directories exist without cleaning them up first.
    # Cleanup should be handled by a separate script or manually.
    os.makedirs(sample_base, exist_ok=True)
    os.makedirs(output_path, exist_ok=True)
    for exp_folder in ["exp1", "exp2"]:
        for subfolder in ["experts", "students", "hints"]:
            path_to_create = os.path.join(
                csv_path, "qualitative", exp_folder, subfolder
            )
            os.makedirs(path_to_create, exist_ok=True)

    walk_and_sample(EXP1_PATH, sample_base, "exp1", "_question", 2)
    walk_and_sample(EXP2_PATH, sample_base, "exp2", "question_", 2)
    print(f"[INFO] Sampling completed. Results: {sample_base}")

    generate_expert_csvs(sample_base, csv_path)
    rename_samples(sample_base, csv_path, output_path)

    print(
        f"\nDone. Qualitative Analysis CSVs: {csv_path}/qualitative/ | Renamed samples: {output_path}"
    )


if __name__ == "__main__":
    main()
