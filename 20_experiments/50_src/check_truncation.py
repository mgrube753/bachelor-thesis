import os
import torch
import pandas as pd
from sentence_transformers import SentenceTransformer
from constants import INPUT_SOURCES_PATH, EMBEDDING_MODEL_ID, EXP1_PATH
from io import StringIO
import sys


class OutputCapture:
    def __init__(self):
        self.buffer = StringIO()
        self.stdout = sys.stdout
        self.output_text = []

    def write(self, text):
        self.stdout.write(text)
        self.buffer.write(text)
        self.output_text.append(text)

    def flush(self):
        self.stdout.flush()
        self.buffer.flush()

    def get_output(self):
        return self.buffer.getvalue()


def save_output(output_text):
    output_dir = os.path.dirname(__file__)

    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "note_truncation.md")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(output_text)

    print(f"\n[INFO] Output saved to {output_file}")
    return output_file


def load_embedding_model(model_name):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[INFO] Loading embedding model '{model_name}' on {device}")
    return SentenceTransformer(model_name, device=device)


def process_file(file_path, model):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        text = "\n".join(
            line
            for line in content.splitlines()
            if not line.strip().endswith("(Falsch)")
        )

        tokens = model.tokenizer(text, truncation=False, return_length=True)
        token_count = len(tokens["input_ids"])
        will_truncate = token_count > model.max_seq_length
        usage = (token_count / model.max_seq_length) * 100

        status = "[TRUNCATED]" if will_truncate else "[OK]"
        rel_path = os.path.relpath(file_path)
        print(f"{status:12} {rel_path}: {token_count:,} tokens ({usage:.1f}%)")

        return {
            "file_path": file_path,
            "token_count": token_count,
            "will_truncate": will_truncate,
            "usage": usage,
        }
    except Exception as e:
        print(f"[ERROR] {os.path.relpath(file_path)}: {e}")
        return None


def scan_directory(directory, description, model):
    if not os.path.exists(directory):
        print(f"[WARNING] Directory not found: {directory}")
        return pd.DataFrame()

    print(f"\n[INFO] Scanning {description}...")
    print("=" * 80)

    results = []
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".txt"):
                result = process_file(os.path.join(root, filename), model)
                if result:
                    results.append(result)

    if not results:
        print(f"[INFO] No .txt files found in {description}")
        return pd.DataFrame()

    df = pd.DataFrame(results)

    total = len(df)
    truncated_count = df["will_truncate"].sum()

    print(f"\n[SUMMARY] {description}")
    print(f"[INFO] Total files checked: {total}")
    print(
        f"[INFO] Files that will be truncated: {truncated_count} ({truncated_count/total*100:.1f}%)"
    )

    if truncated_count > 0:
        print("[WARNING] Files requiring truncation:")
        truncated_df = df[df["will_truncate"]].sort_values(
            "token_count", ascending=False
        )
        for _, row in truncated_df.iterrows():
            rel_path = os.path.relpath(row["file_path"])
            print(f"         {rel_path}: {row['token_count']:,} tokens")

    return df


def main():
    output_capture = OutputCapture()
    sys.stdout = output_capture

    try:
        model = load_embedding_model(EMBEDDING_MODEL_ID)
        print(f"[INFO] Model max sequence length: {model.max_seq_length:,} tokens")

        directories = [
            (INPUT_SOURCES_PATH, "input sources"),
            (EXP1_PATH, "Experiment 1 questions"),
        ]

        all_dfs = []
        for directory, description in directories:
            df = scan_directory(directory, description, model)
            if not df.empty:
                df["source"] = description
                all_dfs.append(df)

        if not all_dfs:
            print("[INFO] No files found to analyze")
            return

        combined_df = pd.concat(all_dfs, ignore_index=True)
        total_files = len(combined_df)
        total_truncated = combined_df["will_truncate"].sum()

        print("\n" + "=" * 80)
        print("[INFO] Overall Summary")
        print(f"[INFO] Total files processed: {total_files:,}")
        print(
            f"[INFO] Total files truncated: {total_truncated} ({total_truncated/total_files*100:.1f}%)"
        )

        if total_truncated > 0:
            print("\n[INFO] Truncated files sorted by token count:")
            truncated_df = combined_df[combined_df["will_truncate"]].sort_values(
                "token_count", ascending=False
            )
            for _, row in truncated_df.iterrows():
                rel_path = os.path.relpath(row["file_path"])
                print(
                    f"         TRUNCATED {rel_path}: {row['token_count']:,} tokens ({row['usage']:.1f}%)"
                )
        else:
            print(
                "\n[INFO] No files require truncation - all files fit within model limits"
            )

        if total_truncated > 0:
            summary = f"{total_truncated} out of {total_files} txt files were longer than the maximum length of {model.max_seq_length} tokens. \n"
            summary += "the source material files were refined before*\n"
            summary += f"and now {total_truncated} questions are longer than {model.max_seq_length} tokens.\n\n"
            full_output = summary + output_capture.get_output()
        else:
            summary = f"All {total_files} txt files fit within the maximum length of {model.max_seq_length} tokens.\n\n"
            full_output = summary + output_capture.get_output()

        save_output(full_output)

    finally:
        sys.stdout = output_capture.stdout


if __name__ == "__main__":
    main()
