import os
import csv
import constants
from file_utils import load_txt, save_result, slugify
from prompt_utils import (
    load_prompt,
    format_prompt,
    get_bloom,
    q_format,
)
from api_calls import llm_generation
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from tqdm import tqdm
from collections import defaultdict


def create_csvs(exp_name, headers, rows):
    try:
        initial_csv_dir = os.path.join(
            os.path.dirname(constants.EXP1_PATH), "60_analyses", "csv", "initial"
        )
        # Create experiment subdirectory
        if exp_name.startswith("exp1"):
            exp_subdir = os.path.join(initial_csv_dir, "exp1")
        elif exp_name.startswith("exp2"):
            exp_subdir = os.path.join(initial_csv_dir, "exp2")
        else:
            exp_subdir = initial_csv_dir

        file_path = os.path.join(exp_subdir, f"{exp_name}.csv")

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            if rows:
                writer.writerows(rows)
        print(f"[INFO] Initial CSV created: {os.path.relpath(file_path)}")
    except IOError as e:
        print(f"[ERROR] Could not write to CSV file {file_path}: {e}")


llm_counters = defaultdict(int)
counter_lock = threading.Lock()


def increment_counter(llm_name):
    with counter_lock:
        llm_counters[llm_name] += 1


def reset_counters():
    with counter_lock:
        llm_counters.clear()
        for llm_name in constants.LLM_NAMES:
            llm_counters[llm_name] = 0


def get_progress():
    with counter_lock:
        if not llm_counters:
            return "Progress"
        desc_parts = []
        for llm_name in sorted(llm_counters.keys()):
            count = llm_counters[llm_name]
            desc_parts.append(f"{llm_name}:{count}")
        return f"Progress [{' | '.join(desc_parts)}]"


def generate_task(
    llm_name,
    clients,
    prompt_or_template,
    output_path,
    description,
    input_text=None,
    max_tokens=2400,
):
    try:
        if llm_name == "deepseek":
            save_result(output_path, "")
            increment_counter(llm_name)
            return True

        if input_text is not None:
            formatted_prompt = format_prompt(prompt_or_template, text=input_text)
        else:
            formatted_prompt = prompt_or_template

        if not formatted_prompt:
            return None

        generated_question = llm_generation(
            llm_name, clients, formatted_prompt, max_tokens=max_tokens
        )
        if generated_question:
            save_result(output_path, generated_question)
            increment_counter(llm_name)
            return True
    except Exception as e:
        print(f"[ERROR] {llm_name}: {description} - {e}")
    return False


def run_tasks(tasks, exp_desc):
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(generate_task, *task): task for task in tasks}

        with tqdm(
            total=len(tasks), desc=f"{exp_desc} {get_progress()}", unit="task"
        ) as pbar:
            for future in as_completed(futures):
                future.result()
                pbar.set_description(f"{exp_desc} {get_progress()}")
                pbar.update(1)


def run_exp_1a(clients):
    print("\n[INFO] Experiment 1a: Content Fidelity")
    reset_counters()
    tasks = []
    csv_rows = []

    for prompt_type_file_name in constants.EXP1_PROMPT_TYPES:
        prompt_path = os.path.join(
            constants.PROMPT_TEMPLATES_PATH,
            "experiment",
            prompt_type_file_name + ".md",
        )
        prompt_template = load_prompt(prompt_path)
        if not prompt_template:
            continue

        output_dir_name = prompt_type_file_name.replace("exp1_", "")

        for source_type in constants.EXP1_SOURCE_TYPES_A:
            for layer_num in constants.LAYERS:
                if source_type == "script":
                    input_text_path = os.path.join(
                        constants.INPUT_SOURCES_PATH,
                        source_type,
                        constants.EXP1_SCRIPT_SUBDIR_A,
                        f"layer{layer_num}.txt",
                    )
                else:
                    input_text_path = os.path.join(
                        constants.INPUT_SOURCES_PATH,
                        source_type,
                        f"layer{layer_num}.txt",
                    )

                input_text = load_txt(input_text_path)
                if not input_text:
                    continue

                for llm_name in constants.LLM_NAMES:
                    output_path = os.path.join(
                        constants.EXP1_PATH,
                        "run_a_content",
                        output_dir_name,
                        llm_name,
                        source_type,
                        f"layer{layer_num}_question.txt",
                    )
                    description = f"{source_type}/layer{layer_num}"

                    tasks.append(
                        (
                            llm_name,
                            clients,
                            prompt_template,
                            output_path,
                            description,
                            input_text,
                            1800,
                        )
                    )
                    prompt_type = output_dir_name.replace("_prompt", "")
                    csv_rows.append([llm_name, source_type, layer_num, prompt_type])

    csv_rows.sort(key=lambda row: (row[0], row[1], int(row[2]), row[3]))
    headers = ["llm", "input_source", "layer", "prompt_type"]
    create_csvs("exp1a", headers, csv_rows)
    run_tasks(tasks, "Exp 1a")


def run_exp_1b(clients):
    print("\n[INFO] Experiment 1b: Error Propagation")
    reset_counters()
    source_type = constants.EXP1_SOURCE_TYPE_B
    tasks = []
    csv_rows = []

    for prompt_type_file_name in constants.EXP1_PROMPT_TYPES:
        prompt_path = os.path.join(
            constants.PROMPT_TEMPLATES_PATH,
            "experiment",
            prompt_type_file_name + ".md",
        )
        prompt_template = load_prompt(prompt_path)
        if not prompt_template:
            continue

        output_dir_name = prompt_type_file_name.replace("exp1_", "")

        for layer_num in constants.LAYERS:
            input_text_path = os.path.join(
                constants.INPUT_SOURCES_PATH,
                source_type,
                constants.EXP1_SCRIPT_SUBDIR_B,
                f"layer{layer_num}.txt",
            )
            input_text = load_txt(input_text_path)
            if not input_text:
                print(f"[WARNING] {source_type}/layer{layer_num}: file not found")
                continue

            for llm_name in constants.LLM_NAMES:
                output_path = os.path.join(
                    constants.EXP1_PATH,
                    "run_b_error",
                    output_dir_name,
                    llm_name,
                    source_type,
                    f"layer{layer_num}_question.txt",
                )
                description = f"{source_type}/layer{layer_num}"

                tasks.append(
                    (
                        llm_name,
                        clients,
                        prompt_template,
                        output_path,
                        description,
                        input_text,
                        1800,
                    )
                )
                prompt_type = output_dir_name.replace("_prompt", "")
                csv_rows.append([llm_name, source_type, layer_num, prompt_type])

    csv_rows.sort(key=lambda row: (row[0], row[1], int(row[2]), row[3]))
    headers = ["llm", "input_source", "layer", "prompt_type"]
    create_csvs("exp1b", headers, csv_rows)
    run_tasks(tasks, "Exp 1b")


def run_exp_1a_no_source(clients):
    print("\n[INFO] Experiment 1a: No Source Content")
    reset_counters()
    tasks = []
    csv_rows = []

    prompt_path = os.path.join(
        constants.PROMPT_TEMPLATES_PATH,
        "experiment",
        "exp1a_complex_prompt_no_source.md",
    )
    prompt_template = load_prompt(prompt_path)
    if not prompt_template:
        print("[ERROR] Could not load prompt template: exp1a_complex_prompt_no_source")
        return

    for layer_num in constants.LAYERS:
        for llm_name in constants.LLM_NAMES:
            formatted_prompt = format_prompt(prompt_template, layer=layer_num)

            output_path = os.path.join(
                constants.EXP1_PATH,
                "run_a_content",
                "complex_prompt_no_source",
                llm_name,
                f"layer{layer_num}_question.txt",
            )
            description = f"layer{layer_num}"

            tasks.append(
                (
                    llm_name,
                    clients,
                    formatted_prompt,
                    output_path,
                    description,
                    None,
                    1800,
                )
            )
            csv_rows.append([llm_name, "no_source", layer_num, "complex_no_source"])

    csv_rows.sort(key=lambda row: (row[0], row[1], int(row[2]), row[3]))
    headers = ["llm", "input_source", "layer", "prompt_type"]
    create_csvs("exp1a_no_source", headers, csv_rows)
    run_tasks(tasks, "Exp 1 No Source")


def run_exp_2a(clients):
    print("\n[INFO] Experiment 2a: Question Type")
    reset_counters()
    tasks = []
    csv_rows = []
    source_name = "tanenbaum"
    layer_num = constants.TANENBAUM_LAYER_FOR_EXP2

    tanenbaum_text_path = os.path.join(
        constants.INPUT_SOURCES_PATH,
        source_name,
        f"layer{layer_num}.txt",
    )
    base_text_for_exp2 = load_txt(tanenbaum_text_path)

    prompt_template_type = load_prompt(
        os.path.join(constants.PROMPT_TEMPLATES_PATH, "experiment", "exp2_type.md")
    )
    if not prompt_template_type:
        return

    for q_type in constants.EXP2_QUESTION_TYPES:
        q_type_slug = slugify(q_type)
        q_type_format_str = q_format(q_type)
        for i in range(6):
            question_id = i + 1
            formatted_prompt = format_prompt(
                prompt_template_type,
                text=base_text_for_exp2,
                question_type=q_type,
                question_type_format=q_type_format_str,
            )

            for llm_name in constants.LLM_NAMES:
                output_path = os.path.join(
                    constants.EXP2_PATH,
                    "run_a_type",
                    llm_name,
                    q_type_slug,
                    f"question_{question_id}.txt",
                )
                description = f"{q_type} question {question_id}"

                tasks.append(
                    (
                        llm_name,
                        clients,
                        formatted_prompt,
                        output_path,
                        description,
                        None,  # no input_text
                        2400,  # max_tokens
                    )
                )
                csv_rows.append(
                    [
                        llm_name,
                        source_name,
                        layer_num,
                        q_type.lower().replace("-", "_"),
                        question_id,
                    ]
                )

    csv_rows.sort(key=lambda row: (row[0], row[1], int(row[2]), row[3], row[4]))
    headers = ["llm", "input_source", "layer", "question_type", "question_id"]
    create_csvs("exp2a", headers, csv_rows)
    run_tasks(tasks, "Exp 2a")


def run_exp_2b(clients):
    print("\n[INFO] Experiment 2b: Bloom Level")
    reset_counters()
    tasks = []
    csv_rows = []
    source_name = "tanenbaum"
    layer_num = constants.TANENBAUM_LAYER_FOR_EXP2
    bloom_data = get_bloom()

    tanenbaum_text_path = os.path.join(
        constants.INPUT_SOURCES_PATH,
        source_name,
        f"layer{layer_num}.txt",
    )
    base_text_for_exp2 = load_txt(tanenbaum_text_path)

    prompt_template_bloom = load_prompt(
        os.path.join(constants.PROMPT_TEMPLATES_PATH, "experiment", "exp2_bloom.md")
    )
    if not prompt_template_bloom:
        return

    for bloom_level_index, bloom_level_name in enumerate(
        constants.BLOOM_LEVELS_ORDERED
    ):
        bloom_original = bloom_level_index + 1
        level_data = bloom_data.get(bloom_level_name, {})
        formatted_prompt = format_prompt(
            prompt_template_bloom,
            text=base_text_for_exp2,
            bloom_level=bloom_level_name,
            bloom_level_description=level_data.get("description", ""),
            bloom_level_verbs=level_data.get("verbs", ""),
        )

        for llm_name in constants.LLM_NAMES:
            output_path = os.path.join(
                constants.EXP2_PATH,
                "run_b_bloom",
                llm_name,
                f"question_{bloom_original}.txt",
            )
            description = f"{bloom_level_name}"

            tasks.append(
                (
                    llm_name,
                    clients,
                    formatted_prompt,
                    output_path,
                    description,
                    None,  # no input_text
                    2400,  # max_tokens
                )
            )
            csv_rows.append([llm_name, source_name, layer_num, bloom_original])

    csv_rows.sort(key=lambda row: (row[0], row[1], int(row[2]), row[3]))
    headers = ["llm", "input_source", "layer", "bloom_original"]
    create_csvs("exp2b", headers, csv_rows)
    run_tasks(tasks, "Exp 2b")


def run_exp_2c(clients):
    print("\n[INFO] Experiment 2c: Combined Type and Bloom")
    reset_counters()
    tasks = []
    csv_rows = []
    source_name = "tanenbaum"
    layer_num = constants.TANENBAUM_LAYER_FOR_EXP2
    bloom_data = get_bloom()

    tanenbaum_text_path = os.path.join(
        constants.INPUT_SOURCES_PATH,
        source_name,
        f"layer{layer_num}.txt",
    )
    base_text_for_exp2 = load_txt(tanenbaum_text_path)

    prompt_template_both = load_prompt(
        os.path.join(constants.PROMPT_TEMPLATES_PATH, "experiment", "exp2_both.md")
    )
    if not prompt_template_both:
        return

    for q_type in constants.EXP2_QUESTION_TYPES:
        q_type_slug = slugify(q_type)
        for i, bloom_level_name in enumerate(constants.BLOOM_LEVELS_ORDERED):
            bloom_original = i + 1
            level_data = bloom_data.get(bloom_level_name, {})
            q_type_format_str = q_format(q_type)

            formatted_prompt = format_prompt(
                prompt_template_both,
                text=base_text_for_exp2,
                question_type=q_type,
                bloom_level=bloom_level_name,
                bloom_level_description=level_data.get("description", ""),
                bloom_level_verbs=level_data.get("verbs", ""),
                question_type_format=q_type_format_str,
            )

            for llm_name in constants.LLM_NAMES:
                output_path = os.path.join(
                    constants.EXP2_PATH,
                    "run_c_both",
                    llm_name,
                    q_type_slug,
                    f"question_{bloom_original}.txt",
                )
                description = f"{q_type} {bloom_level_name}"

                tasks.append(
                    (
                        llm_name,
                        clients,
                        formatted_prompt,
                        output_path,
                        description,
                        None,  # no input_text
                        2400,  # max_tokens
                    )
                )
                csv_rows.append(
                    [
                        llm_name,
                        source_name,
                        layer_num,
                        q_type.lower().replace("-", "_"),
                        bloom_original,
                    ]
                )

    csv_rows.sort(key=lambda row: (row[0], row[1], int(row[2]), row[3], row[4]))
    headers = ["llm", "input_source", "layer", "question_type", "bloom_original"]
    create_csvs("exp2c", headers, csv_rows)
    run_tasks(tasks, "Exp 2c")
