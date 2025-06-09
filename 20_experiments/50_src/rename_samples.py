import os
import shutil
import pandas as pd
from constants import EXPERIMENTS_BASE_PATH


def main():
    base = EXPERIMENTS_BASE_PATH
    samples = os.path.join(base, "70_samples")
    evals = os.path.join(base, "60_eval", "csv_files", "auto")
    output = os.path.join(base, "80_questions_renamed")

    os.makedirs(output, exist_ok=True)

    print("Processing exp1...")
    count = process_exp("exp1", samples, evals, output, 1)
    print(f"Exp1: {count-1} questions")

    print("Processing exp2...")
    count = process_exp("exp2", samples, evals, output, 1)
    print(f"Exp2: {count-1} questions")
    print(f"Done. Output: {output}")


def process_exp(prefix, samples, evals, output, count):
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
                print(f"{os.path.basename(src)} -> {new_name}")
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
        elif "transcript" in src:
            return "transcript"
        elif "script" in src:
            return "script"
        elif "tanenbaum" in src:
            return "tanenbaum"
        return "unknown"
    return "tanenbaum"


def get_file(samples, exp, row):
    if exp.startswith("exp1"):
        return get_exp1_file(samples, exp, row)
    return get_exp2_file(samples, exp, row)


def get_exp1_file(samples, exp, row):
    run = "run_a_content" if exp == "exp1a" else "run_b_error"
    prompt = f"{row['prompt_type']}_prompt"
    llm = row["llm"]
    source = row["input_source"].replace("_manipulated", "")
    layer = row["layer"]

    dir_path = os.path.join(samples, "exp1", run, prompt, llm, source)

    if os.path.exists(dir_path):
        for f in os.listdir(dir_path):
            if f"layer{layer}_question" in f and f.endswith(".txt"):
                return os.path.join(dir_path, f)
    return None


def get_exp2_file(samples, exp, row):
    runs = {"exp2a": "run_a_type", "exp2b": "run_b_bloom", "exp2c": "run_c_both"}
    run = runs.get(exp)
    if not run:
        return None

    llm = row["llm"]

    if exp == "exp2a":
        qtype = row["question_type"].lower().replace("-", "_")
        qid = row.get("question_id", 1)
        dir_path = os.path.join(samples, "exp2", run, llm, qtype)
        pattern = f"question_{qid}"
    elif exp == "exp2b":
        bloom = row.get("bloom_original", 1)
        dir_path = os.path.join(samples, "exp2", run, llm)
        pattern = f"question_{bloom}"
    else:
        qtype = row["question_type"].lower().replace("-", "_")
        bloom = row.get("bloom_original", 1)
        dir_path = os.path.join(samples, "exp2", run, llm, qtype)
        pattern = f"question_{bloom}"

    if os.path.exists(dir_path):
        for f in os.listdir(dir_path):
            if pattern in f and f.endswith(".txt"):
                return os.path.join(dir_path, f)
    return None


if __name__ == "__main__":
    main()
