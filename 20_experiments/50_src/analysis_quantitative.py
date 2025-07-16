import os
import pandas as pd
import numpy as np
import concurrent.futures
import threading
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm
from constants import (
    EXP1_PATH,
    INPUT_SOURCES_PATH,
    ANALYSES_PATH,
    PROMPT_TEMPLATES_PATH,
    EMBEDDING_MODEL_ID,
)
from file_utils import load_txt
from api_calls import llm_generation
from api_config import init_clients


def load_model():
    return SentenceTransformer(EMBEDDING_MODEL_ID)


def calc_cossim_batch(model, questions, sources):
    all_texts = questions + sources
    embeddings = model.encode(all_texts, batch_size=32, show_progress_bar=True)

    question_embeddings = embeddings[: len(questions)]
    source_embeddings = embeddings[len(questions) :]

    similarities = cosine_similarity(question_embeddings, source_embeddings)
    return np.diag(similarities)


def get_adherence_scores(clients, question, source_text, evaluator):
    prompt_path = os.path.join(
        PROMPT_TEMPLATES_PATH, "evaluation", "exp1_adherence_eval.md"
    )
    prompt_template = load_txt(prompt_path)

    prompt = prompt_template.replace("{question_text}", question).replace(
        "{context_text}", source_text
    )

    response = llm_generation(evaluator, clients, prompt, max_tokens=1200)
    if response:
        try:
            score = float(response.strip())
            if 0 <= score <= 1:
                return score
            else:
                return None
        except ValueError:
            return None
    else:
        return None


def get_adherence_scores_parallel(
    clients,
    questions_sources_pairs,
    max_workers=2,
    df=None,
    valid_indices=None,
    csv_path=None,
):
    results = [(None, None)] * len(questions_sources_pairs)
    completed_count = 0
    count_lock = threading.Lock()

    def process_single(index, question, source_text):
        nonlocal completed_count

        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            future_openai = executor.submit(
                get_adherence_scores, clients, question, source_text, "openai"
            )
            future_anthropic = executor.submit(
                get_adherence_scores, clients, question, source_text, "anthropic"
            )
            openai_score = future_openai.result()
            anthropic_score = future_anthropic.result()

        results[index] = (openai_score, anthropic_score)

        # Save incrementally if parameters provided
        if df is not None and valid_indices is not None and csv_path is not None:
            with count_lock:
                idx = valid_indices[index]
                if openai_score is not None:
                    df.at[idx, "adherence_score_openai"] = openai_score
                if anthropic_score is not None:
                    df.at[idx, "adherence_score_anthropic"] = anthropic_score
                df.to_csv(csv_path, index=False)

        with count_lock:
            completed_count += 1

    # https://docs.python.org/3/library/concurrent.futures.html
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(process_single, i, q, s)
            for i, (q, s) in enumerate(questions_sources_pairs)
        ]

        with tqdm(
            total=len(questions_sources_pairs),
            desc="Adherence scores (OpenAI & Anthropic)",
            unit="pair",
        ) as pbar:
            for future in concurrent.futures.as_completed(futures):
                future.result()
                pbar.update(1)

    return results


def get_question_path(exp_name, llm, source, layer, prompt_type):
    if exp_name == "exp1a":
        if source == "no_source":
            base_path = os.path.join(
                EXP1_PATH, "run_a_content", "complex_prompt_no_source"
            )
            filename = f"layer{layer}_question.txt"
            return os.path.join(base_path, llm, filename)
        else:
            base_path = os.path.join(EXP1_PATH, "run_a_content")
            filename = f"layer{layer}_question.txt"
            return os.path.join(
                base_path, f"{prompt_type}_prompt", llm, source, filename
            )
    elif exp_name == "exp1b":
        base_path = os.path.join(EXP1_PATH, "run_b_error")
        filename = f"layer{layer}_question.txt"
        actual_source = "script" if source == "script_manipulated" else source
        return os.path.join(
            base_path, f"{prompt_type}_prompt", llm, actual_source, filename
        )
    else:
        raise ValueError(f"Unknown experiment name: {exp_name}")


def get_source_file_path(source, layer, is_manipulated=False):
    if source == "no_source":
        source_dir = os.path.join(INPUT_SOURCES_PATH, "script", "common")
        source_type = "script (common) - reference for no_source"
        filename = f"layer{layer}.txt"
        return os.path.join(source_dir, filename), source_type

    if is_manipulated:
        source_dir = os.path.join(INPUT_SOURCES_PATH, "script", "manipulated")
        source_type = f"{source} (manipulated)"
    else:
        if source == "script":
            source_dir = os.path.join(INPUT_SOURCES_PATH, source, "common")
            source_type = f"{source} (common)"
        else:
            source_dir = os.path.join(INPUT_SOURCES_PATH, source)
            source_type = source

    filename = f"layer{layer}.txt"
    return os.path.join(source_dir, filename), source_type


def expand_no_source_data(df):
    expanded_rows = []
    for _, row in df.iterrows():
        if row["input_source"] == "no_source":
            for source in ["script", "tanenbaum", "transcript"]:
                new_row = row.copy()
                new_row["comparison_source"] = source
                expanded_rows.append(new_row)
        else:
            new_row = row.copy()
            new_row["comparison_source"] = row["input_source"]
            expanded_rows.append(new_row)

    return pd.DataFrame(expanded_rows).reset_index(drop=True)


def process_experiment(exp_name):
    print(f"[INFO] Processing {exp_name}")
    print("=" * 80)

    model = load_model()
    clients = init_clients()

    if exp_name == "exp1a_no_source":
        csv_input_path = os.path.join(
            ANALYSES_PATH, "csv", "initial", "exp1", f"{exp_name}.csv"
        )
        csv_output_path = os.path.join(
            ANALYSES_PATH, "csv", "quantitative", "exp1", f"{exp_name}.csv"
        )
        actual_exp_name = "exp1a"

        # Expand no_source data to compare with all three sources
        df_original = pd.read_csv(csv_input_path)
        df = expand_no_source_data(df_original)

        # Add missing columns for expanded DataFrame
        for col in [
            "cosine_similarity",
            "adherence_score_openai",
            "adherence_score_anthropic",
        ]:
            if col not in df.columns:
                df[col] = np.nan
    else:
        csv_input_path = os.path.join(
            ANALYSES_PATH, "csv", "quantitative", "exp1", f"{exp_name}.csv"
        )
        csv_output_path = csv_input_path
        actual_exp_name = exp_name
        df = pd.read_csv(csv_input_path)

    questions = []
    sources = []
    valid_indices = []
    comparison_info = []

    print("[INFO] Loading questions and sources...")
    for idx, row in df.iterrows():
        llm = row["llm"]
        layer = row["layer"]
        prompt_type = row["prompt_type"]

        # Use comparison_source for source file selection
        comparison_source = row.get("comparison_source", row["input_source"])
        input_source = row["input_source"]

        question_path = get_question_path(
            actual_exp_name, llm, input_source, layer, prompt_type
        )
        question_content = load_txt(question_path)

        if not question_content:
            print(f"[WARNING] No question found: {question_path}")
            continue

        question = "\n".join(
            line
            for line in question_content.splitlines()
            if not line.strip().endswith("(Falsch)")
        )

        if not question:
            print(f"[WARNING] Question is empty after filtering: {question_path}")
            continue

        is_manipulated = actual_exp_name == "exp1b"
        source_path, source_type = get_source_file_path(
            comparison_source, layer, is_manipulated
        )
        source_text = load_txt(source_path)

        if not source_text:
            print(f"[WARNING] No source found: {source_path}")
            continue

        print(
            f"[MATCH {len(questions)+1:3d}] Question: {os.path.relpath(question_path, EXP1_PATH)}"
        )
        print(f"             Source:   {source_type} - layer{layer}.txt")
        print(f"             LLM:      {llm} | Prompt: {prompt_type}")
        print("-" * 80)

        questions.append(question)
        sources.append(source_text)
        valid_indices.append(idx)
        comparison_info.append(
            {
                "question_path": question_path,
                "source_path": source_path,
                "source_type": source_type,
                "llm": llm,
                "prompt_type": prompt_type,
                "layer": layer,
            }
        )

    if not questions:
        print("[ERROR] No valid question-source pairs found!")
        return

    print(f"\n[INFO] Total valid pairs found: {len(questions)}")
    print("=" * 80)

    print("[INFO] Calculating cosine similarities in batch...")
    similarities = calc_cossim_batch(model, questions, sources)

    for i, idx in enumerate(valid_indices):
        df.at[idx, "cosine_similarity"] = similarities[i]
        info = comparison_info[i]
        print(
            f"[COSINE] {info['source_type']} layer{info['layer']} -> {info['llm']} ({info['prompt_type']}): {similarities[i]:.4f}"
        )

    df.to_csv(csv_output_path, index=False)
    print("=" * 80)

    questions_sources_pairs = list(zip(questions, sources))

    print("[INFO] Processing adherence scores with OpenAI and Anthropic...")
    adherence_results = get_adherence_scores_parallel(
        clients,
        questions_sources_pairs,
        max_workers=2,
        df=df,
        valid_indices=valid_indices,
        csv_path=csv_output_path,
    )

    for i, idx in enumerate(valid_indices):
        openai_score, anthropic_score = adherence_results[i]
        info = comparison_info[i]
        print(
            f"[ADHERENCE OpenAI] {info['source_type']} layer{info['layer']} -> {info['llm']} ({info['prompt_type']}): {openai_score}"
        )
        print(
            f"[ADHERENCE Anthropic] {info['source_type']} layer{info['layer']} -> {info['llm']} ({info['prompt_type']}): {anthropic_score}"
        )

    print(f"\n[INFO] Final results saved to {csv_output_path}")
    print("=" * 80)


if __name__ == "__main__":
    process_experiment("exp1a")
    process_experiment("exp1b")
    process_experiment("exp1a_no_source")
