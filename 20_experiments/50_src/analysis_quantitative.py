import os
import pandas as pd
import numpy as np
import concurrent.futures
import threading
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import constants
from file_utils import load_txt
from api_calls import llm_generation
from api_config import init_clients


def load_model():
    return SentenceTransformer(constants.EMBEDDING_MODEL_ID)


def calc_cossim_batch(model, questions, sources):
    all_texts = questions + sources
    embeddings = model.encode(all_texts, batch_size=32, show_progress_bar=True)

    question_embeddings = embeddings[: len(questions)]
    source_embeddings = embeddings[len(questions) :]

    similarities = cosine_similarity(question_embeddings, source_embeddings)
    return np.diag(similarities)


def get_adherence_scores(clients, question, source_text):
    prompt_path = os.path.join(
        constants.PROMPT_TEMPLATES_PATH, "evaluation", "exp1_adherence_eval.md"
    )
    prompt_template = load_txt(prompt_path)

    prompt = prompt_template.replace("{question_text}", question).replace(
        "{context_text}", source_text
    )

    response = llm_generation("anthropic", clients, prompt, max_tokens=1200)
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


def get_adherence_scores_parallel(clients, questions_sources_pairs, max_workers=3):
    results = [None] * len(questions_sources_pairs)
    rate_limiter = threading.Semaphore(max_workers)

    def process_single(index, question, source_text):
        with rate_limiter:
            result = get_adherence_scores(clients, question, source_text)
            results[index] = result

    # https://docs.python.org/3/library/concurrent.futures.html
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(process_single, i, q, s)
            for i, (q, s) in enumerate(questions_sources_pairs)
        ]
        concurrent.futures.wait(futures)

    return results


def get_question_path(exp_name, llm, source, layer, prompt_type):
    if exp_name == "exp1a":
        base_path = os.path.join(constants.EXP1_PATH, "run_a_content")
    elif exp_name == "exp1b":
        base_path = os.path.join(constants.EXP1_PATH, "run_b_error")
    else:
        raise ValueError(f"Unknown experiment name: {exp_name}")

    filename = f"layer{layer}_question.txt"
    return os.path.join(base_path, f"{prompt_type}_prompt", llm, source, filename)


def get_source_file_path(source, layer, is_manipulated=False):

    if is_manipulated:
        source_dir = os.path.join(constants.INPUT_SOURCES_PATH, source, "manipulated")
        source_type = f"{source} (manipulated)"
    else:
        if source == "script":
            source_dir = os.path.join(constants.INPUT_SOURCES_PATH, source, "common")
            source_type = f"{source} (common)"
        else:
            source_dir = os.path.join(constants.INPUT_SOURCES_PATH, source)
            source_type = source

    filename = f"layer{layer}.txt"
    return os.path.join(source_dir, filename), source_type


def process_experiment(exp_name):
    print(f"[INFO] Processing {exp_name}")
    print("=" * 80)

    model = load_model()
    clients = init_clients()
    csv_path = os.path.join(constants.EVAL_PATH, "csv_files", "auto", f"{exp_name}.csv")
    df = pd.read_csv(csv_path)

    questions = []
    sources = []
    valid_indices = []
    comparison_info = []

    print("[INFO] Loading questions and sources...")
    for idx, row in df.iterrows():
        llm = row["llm"]
        source = row["input_source"].replace("_manipulated", "")
        layer = row["layer"]
        prompt_type = row["prompt_type"]

        question_path = get_question_path(exp_name, llm, source, layer, prompt_type)
        question = load_txt(question_path)

        if not question:
            print(f"[WARNING] No question found: {question_path}")
            continue

        is_manipulated = exp_name == "exp1b"
        source_path, source_type = get_source_file_path(source, layer, is_manipulated)
        source_text = load_txt(source_path)

        if not source_text:
            print(f"[WARNING] No source found: {source_path}")
            continue

        print(
            f"[MATCH {len(questions)+1:3d}] Question: {os.path.relpath(question_path, constants.EXP1_PATH)}"
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
        df.at[idx, "cosine_similarity"] = round(similarities[i], 4)
        info = comparison_info[i]
        print(
            f"[COSINE] {info['source_type']} layer{info['layer']} -> {info['llm']} ({info['prompt_type']}): {similarities[i]:.4f}"
        )

    print("=" * 80)

    # This takes a while, since the maximum of output tokens for Anthropic is 8000 per minute
    print("[INFO] Processing adherence scores in parallel...")
    questions_sources_pairs = list(zip(questions, sources))
    adherence_results = get_adherence_scores_parallel(clients, questions_sources_pairs)

    for i, idx in enumerate(valid_indices):
        adherence_score = adherence_results[i]

        if adherence_score is not None:
            df.at[idx, "adherence_score"] = round(adherence_score, 4)

        info = comparison_info[i]
        print(
            f"[ADHERENCE] {info['source_type']} layer{info['layer']} -> {info['llm']} ({info['prompt_type']}): {adherence_score}"
        )

    df.to_csv(csv_path, index=False)
    print(f"\n[INFO] Saved results to {csv_path}")
    print("=" * 80)


if __name__ == "__main__":
    process_experiment("exp1a")
    process_experiment("exp1b")
