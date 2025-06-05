import os
import random
import shutil
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


def main():
    print("[INFO] Starting question sampling process...")
    random.seed(2025)

    sample_base = os.path.join(constants.EXPERIMENTS_BASE_PATH, "70_samples")
    os.makedirs(sample_base, exist_ok=True)

    walk_and_sample(
        constants.EXP1_PATH, sample_base, "exp1", "_question", sample_size=2
    )
    walk_and_sample(
        constants.EXP2_PATH, sample_base, "exp2", "question_", sample_size=2
    )

    print(f"[INFO] Sampling completed. Results: {sample_base}")


if __name__ == "__main__":
    main()
