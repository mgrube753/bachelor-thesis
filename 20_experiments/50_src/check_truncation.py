import os
import torch
import pandas as pd
from sentence_transformers import SentenceTransformer
from constants import INPUT_SOURCES_PATH, EMBEDDING_MODEL_ID


def load_embedding_model(model_name):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[INFO] Loading embedding model '{model_name}' on {device}")
    return SentenceTransformer(model_name, device=device)


def process_file(file_path, model, results):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        tokens = model.tokenizer(text, truncation=False, return_length=True)
        token_count = len(tokens["input_ids"])
        will_truncate = token_count > model.max_seq_length
        usage = (token_count / model.max_seq_length) * 100

        results["File Path"].append(file_path)
        results["Token Count"].append(token_count)
        results["Will Truncate"].append("Yes" if will_truncate else "No")
        results["Percentage Used"].append(f"{usage:.2f}%")

        status = "🔴 TRUNCATED" if will_truncate else "✅ OK"
        print(f"{status:12} {file_path}: {token_count:,} tokens ({usage:.1f}%)")
    except Exception as e:
        print(f"❌ ERROR    {file_path}: {e}")


def main():
    model = load_embedding_model(EMBEDDING_MODEL_ID)
    results = {
        "File Path": [],
        "Token Count": [],
        "Will Truncate": [],
        "Percentage Used": [],
    }

    print(f"\n[INFO] Model max sequence length: {model.max_seq_length}")
    print(f"[INFO] Scanning: {INPUT_SOURCES_PATH}\n{'-' * 60}")

    for root, _, files in os.walk(INPUT_SOURCES_PATH):
        for filename in files:
            if filename.endswith(".txt"):
                process_file(os.path.join(root, filename), model, results)

    print("\n" + "=" * 60)
    df = pd.DataFrame(results)

    if not df.empty:
        truncated_count = results["Will Truncate"].count("Yes")
        total_count = len(results["Will Truncate"])
        print(f"\nChecked: {total_count} files")
        print(
            f"Truncated: {truncated_count} ({truncated_count/total_count*100:.2f}%)\n"
        )
        print("All files sorted by token count:\n")
        print(df.sort_values("Token Count", ascending=False))
    else:
        print("[INFO] No valid .txt files found.")


if __name__ == "__main__":
    main()
