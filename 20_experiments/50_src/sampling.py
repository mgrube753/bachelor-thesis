import os
import random
import shutil
import pandas as pd
import constants


def sample_questions(src_path, dest_path, pattern, sample_size=3):
    question_files = [
        f for f in os.listdir(src_path) if pattern in f and f.endswith(".txt")
    ]
    if len(question_files) < sample_size:
        print(f"[WARNING] Only {len(question_files)} questions available in {src_path}")
        sample_size = len(question_files)
    if sample_size == 0:
        return []

    sampled = random.sample(question_files, sample_size)
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


def generate_expert_csvs(sample_base, expert_csv_path):
    os.makedirs(expert_csv_path, exist_ok=True)
    print("\n[INFO] Generating CSV files for expert evaluation from samples...")

    all_records = []
    runs_map = {"run_a_type": "exp2a", "run_b_bloom": "exp2b", "run_c_both": "exp2c"}

    for root, _, files in os.walk(sample_base):
        for file in files:
            if not file.endswith(".txt"):
                continue

            parts = os.path.relpath(os.path.join(root, file), sample_base).split(os.sep)
            record = {}
            try:
                if parts[0] == "exp1":
                    record["exp_name"] = (
                        "exp1a" if parts[1] == "run_a_content" else "exp1b"
                    )
                    record["prompt_type"] = parts[2].replace("_prompt", "")
                    record["llm"] = parts[3]
                    record["input_source"] = parts[4]
                    record["layer"] = int(parts[5].split("_")[0].replace("layer", ""))

                elif parts[0] == "exp2":
                    exp_name = runs_map.get(parts[1])
                    if not exp_name:
                        continue
                    record["exp_name"] = exp_name
                    record["llm"] = parts[2]
                    record["layer"] = 2

                    if exp_name == "exp2a":
                        record["question_type"] = parts[3].replace("_", "-")
                        record["question_id"] = int(
                            parts[4].split("_")[1].replace(".txt", "")
                        )
                    elif exp_name == "exp2b":
                        record["bloom_original"] = int(
                            parts[3].split("_")[1].replace(".txt", "")
                        )
                    elif exp_name == "exp2c":
                        record["question_type"] = parts[3].replace("_", "-")
                        record["bloom_original"] = int(
                            parts[4].split("_")[1].replace(".txt", "")
                        )
                else:
                    continue
                all_records.append(record)
            except (IndexError, ValueError):
                print(f"[WARNING] Could not parse path: {os.path.join(*parts)}")
                continue

    if not all_records:
        return

    df = pd.DataFrame(all_records)

    # Process exp1 files - save for renaming process
    exp1_data = df[df["exp_name"].isin(["exp1a", "exp1b"])]
    if not exp1_data.empty:
        for exp_name, group in exp1_data.groupby("exp_name"):
            # Save CSV for renaming process (with all columns needed)
            csv_path = os.path.join(expert_csv_path, f"{exp_name}.csv")
            group.to_csv(csv_path, index=False)
            print(
                f"  - Generated {os.path.relpath(csv_path, constants.EXPERIMENTS_BASE_PATH)}"
            )

            # Create expert evaluation CSVs
            output_df = group[["input_source", "layer"]].copy()
            output_df["relevance"] = ""
            output_df["clarity"] = ""
            output_df["answerability"] = ""
            output_df["challenging"] = ""
            output_df["correctness"] = ""

            # Save to each expert folder
            for i in range(1, 6):
                expert_dir = os.path.join(expert_csv_path, "qualitative", f"expert_{i}")
                os.makedirs(expert_dir, exist_ok=True)
                expert_csv_path_full = os.path.join(expert_dir, f"{exp_name}.csv")
                output_df.to_csv(expert_csv_path_full, index=False)

    # Process exp2 files - save for renaming process
    exp2_data = df[df["exp_name"].isin(["exp2a", "exp2b", "exp2c"])]
    if not exp2_data.empty:
        for exp_name, group in exp2_data.groupby("exp_name"):
            # Save CSV for renaming process (with all columns needed)
            csv_path = os.path.join(expert_csv_path, f"{exp_name}.csv")
            group.to_csv(csv_path, index=False)
            print(
                f"  - Generated {os.path.relpath(csv_path, constants.EXPERIMENTS_BASE_PATH)}"
            )

            # Create expert evaluation CSVs
            cols = ["llm"]
            if (
                "bloom_original" in group.columns
                and not group["bloom_original"].isna().all()
            ):
                cols.append("bloom_original")
            cols.append("layer")

            output_df = group[cols].copy()
            output_df.rename(columns={"llm": "llm_input_source"}, inplace=True)
            output_df["llm_input_source"] = output_df["llm_input_source"] + "_tanenbaum"

            if "bloom_original" in output_df.columns:
                output_df["bloom_original"] = output_df["bloom_original"].astype(int)

            output_df["relevance"] = ""
            output_df["clarity"] = ""
            output_df["answerability"] = ""
            output_df["challenging"] = ""
            output_df["bloom_rating"] = ""
            output_df["bloom_score"] = ""

            # Save to both expert folders
            for expert_type in ["expert_anthropic", "expert_openai"]:
                expert_dir = os.path.join(expert_csv_path, "qualitative", expert_type)
                os.makedirs(expert_dir, exist_ok=True)
                expert_csv_path_full = os.path.join(expert_dir, f"{exp_name}.csv")
                output_df.to_csv(expert_csv_path_full, index=False)


def process_exp(prefix, samples, evals, output, count):
    """Reads CSVs and renames corresponding samples for inspection."""
    csvs = [f for f in os.listdir(evals) if f.startswith(prefix) and f.endswith(".csv")]
    for csv in sorted(csvs):
        exp = csv.replace(".csv", "")
        df = pd.read_csv(os.path.join(evals, csv))
        exp_dir = os.path.join(output, exp)
        os.makedirs(exp_dir, exist_ok=True)

        for _, row in df.iterrows():
            src = get_file(samples, exp, row)
            if src and os.path.exists(src):
                source_type = get_source(exp, row)
                layer = get_layer(exp, row)
                new_name = f"{count:03d}_{source_type}_{layer}.txt"
                dst = os.path.join(exp_dir, new_name)
                shutil.copy2(src, dst)
                print(f"  {os.path.basename(src)} -> {new_name}")
                count += 1
    return count


def get_layer(exp, row):
    if exp.startswith("exp1"):
        return row.get("layer", 1)
    return 2


def get_source(exp, row):
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


def get_file(samples, exp, row):
    """Finds the corresponding file path for a row in the CSV."""
    if exp.startswith("exp1"):
        return get_exp1_file(samples, exp, row)
    return get_exp2_file(samples, exp, row)


def get_exp1_file(samples, exp, row):
    run = "run_a_content" if exp == "exp1a" else "run_b_error"
    source = row["input_source"].replace("_manipulated", "")
    dir_path = os.path.join(
        samples, "exp1", run, f"{row['prompt_type']}_prompt", row["llm"], source
    )
    if os.path.exists(dir_path):
        layer = row.get("layer")
        if pd.isna(layer):
            return None
        pattern = f"layer{int(layer)}_question"
        for f in os.listdir(dir_path):
            if pattern in f and f.endswith(".txt"):
                return os.path.join(dir_path, f)
    return None


def get_exp2_file(samples, exp, row):
    runs = {"exp2a": "run_a_type", "exp2b": "run_b_bloom", "exp2c": "run_c_both"}
    run = runs.get(exp)
    if not run:
        return None

    llm = row["llm"]
    dir_path = None
    filename = None

    try:
        if exp == "exp2a":
            qtype = row["question_type"].lower().replace("-", "_")
            dir_path = os.path.join(samples, "exp2", run, llm, qtype)
            qid = row.get("question_id")
            if not pd.isna(qid):
                filename = f"question_{int(qid)}.txt"
        elif exp == "exp2b":
            dir_path = os.path.join(samples, "exp2", run, llm)
            bloom_id = row.get("bloom_original")
            if not pd.isna(bloom_id):
                filename = f"question_{int(bloom_id)}.txt"
        else:  # exp2c
            qtype = row["question_type"].lower().replace("-", "_")
            dir_path = os.path.join(samples, "exp2", run, llm, qtype)
            bloom_id = row.get("bloom_original")
            if not pd.isna(bloom_id):
                filename = f"question_{int(bloom_id)}.txt"
    except (ValueError, TypeError):
        return None

    if dir_path and filename:
        file_path = os.path.join(dir_path, filename)
        if os.path.exists(file_path):
            return file_path

    return None


def main():
    random.seed(2025)
    base = constants.EXPERIMENTS_BASE_PATH
    sample_base = os.path.join(base, "70_samples")
    expert_csv_path = os.path.join(base, "60_eval", "csv_files")
    renamed_output_path = os.path.join(base, "80_questions_renamed")

    # --- 1. Sampling ---
    shutil.rmtree(sample_base, ignore_errors=True)
    walk_and_sample(constants.EXP1_PATH, sample_base, "exp1", "_question", 2)
    walk_and_sample(constants.EXP2_PATH, sample_base, "exp2", "question_", 2)
    print(f"[INFO] Sampling completed. Results: {sample_base}")

    # --- 2. Generate expert CSVs from samples ---
    # Only remove the qualitative folder and specific CSV files, not the entire csv_files directory
    qualitative_path = os.path.join(expert_csv_path, "qualitative")
    shutil.rmtree(qualitative_path, ignore_errors=True)

    generate_expert_csvs(sample_base, expert_csv_path)

    # --- 3. Rename samples for inspection based on generated CSVs ---
    print("\n[INFO] Starting renaming process for manual inspection...")
    shutil.rmtree(renamed_output_path, ignore_errors=True)

    print("Processing exp1...")
    count = process_exp("exp1", sample_base, expert_csv_path, renamed_output_path, 1)
    print(f"Exp1: {count - 1} questions renamed.")

    print("Processing exp2...")
    count = process_exp("exp2", sample_base, expert_csv_path, renamed_output_path, 1)
    print(f"Exp2: {count - 1} questions renamed.")
    print(f"\nDone. Renamed questions for inspection: {renamed_output_path}")

    # Remove only exp CSV files from the root csv_files directory
    for exp_file in ["exp1a.csv", "exp1b.csv", "exp2a.csv", "exp2b.csv", "exp2c.csv"]:
        exp_file_path = os.path.join(expert_csv_path, exp_file)
        if os.path.exists(exp_file_path):
            os.remove(exp_file_path)


if __name__ == "__main__":
    main()
