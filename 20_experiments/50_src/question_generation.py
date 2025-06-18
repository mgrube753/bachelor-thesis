import os
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

print_lock = threading.Lock()
llm_counters = defaultdict(int)
counter_lock = threading.Lock()


def safe_print(message):
    with print_lock:
        print(message)


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


def generate_task_exp1(
    llm_name, clients, prompt_template, input_text, output_path, description
):
    try:
        formatted_prompt = format_prompt(prompt_template, text=input_text)
        if not formatted_prompt:
            return None

        generated_question = llm_generation(
            llm_name, clients, formatted_prompt, max_tokens=1600
        )
        if generated_question:
            save_result(output_path, generated_question)
            increment_counter(llm_name)
            return True
    except Exception as e:
        safe_print(f"[ERROR] {llm_name}: {description} - {e}")
    return False


def generate_task_exp2(llm_name, clients, formatted_prompt, output_path, description):
    try:
        if not formatted_prompt:
            return None

        generated_question = llm_generation(
            llm_name, clients, formatted_prompt, max_tokens=2400
        )
        if generated_question:
            save_result(output_path, generated_question)
            increment_counter(llm_name)
            return True
    except Exception as e:
        safe_print(f"[ERROR] {llm_name}: {description} - {e}")
    return False


def run_exp_1a(clients):
    safe_print("\n[INFO] Experiment 1a: Content Fidelity")
    reset_counters()
    tasks = []

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
                            input_text,
                            output_path,
                            description,
                        )
                    )

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(generate_task_exp1, *task): task for task in tasks}

        with tqdm(
            total=len(tasks), desc=f"Exp 1a {get_progress()}", unit="task"
        ) as pbar:
            for future in as_completed(futures):
                future.result()
                pbar.set_description(f"Exp 1a {get_progress()}")
                pbar.update(1)


def run_exp_1b(clients):
    safe_print("\n[INFO] Experiment 1b: Error Propagation")
    reset_counters()
    source_type = constants.EXP1_SOURCE_TYPE_B
    tasks = []

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
                safe_print(f"[WARNING] {source_type}/layer{layer_num}: file not found")
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
                        input_text,
                        output_path,
                        description,
                    )
                )

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(generate_task_exp1, *task): task for task in tasks}

        with tqdm(
            total=len(tasks), desc=f"Exp 1b {get_progress()}", unit="task"
        ) as pbar:
            for future in as_completed(futures):
                future.result()
                pbar.set_description(f"Exp 1b {get_progress()}")
                pbar.update(1)


def run_exp_2a(clients):
    safe_print("\n[INFO] Experiment 2a: Question Type")
    reset_counters()

    tanenbaum_text_path = os.path.join(
        constants.INPUT_SOURCES_PATH,
        "tanenbaum",
        f"layer{constants.TANENBAUM_LAYER_FOR_EXP2}.txt",
    )
    base_text_for_exp2 = load_txt(tanenbaum_text_path)

    prompt_template_type = load_prompt(
        os.path.join(constants.PROMPT_TEMPLATES_PATH, "experiment", "exp2_type.md")
    )
    if not prompt_template_type:
        return

    tasks = []

    for q_type in constants.EXP2_QUESTION_TYPES:
        q_type_slug = slugify(q_type)
        q_type_format_str = q_format(q_type)
        for i in range(6):
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
                    f"question_{i + 1}.txt",
                )
                description = f"{q_type} question {i + 1}"

                tasks.append(
                    (llm_name, clients, formatted_prompt, output_path, description)
                )

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(generate_task_exp2, *task): task for task in tasks}

        with tqdm(
            total=len(tasks), desc=f"Exp 2a {get_progress()}", unit="task"
        ) as pbar:
            for future in as_completed(futures):
                future.result()
                pbar.set_description(f"Exp 2a {get_progress()}")
                pbar.update(1)


def run_exp_2b(clients):
    safe_print("\n[INFO] Experiment 2b: Bloom Level")
    reset_counters()
    bloom_data = get_bloom()

    tanenbaum_text_path = os.path.join(
        constants.INPUT_SOURCES_PATH,
        "tanenbaum",
        f"layer{constants.TANENBAUM_LAYER_FOR_EXP2}.txt",
    )
    base_text_for_exp2 = load_txt(tanenbaum_text_path)

    prompt_template_bloom = load_prompt(
        os.path.join(constants.PROMPT_TEMPLATES_PATH, "experiment", "exp2_bloom.md")
    )
    if not prompt_template_bloom:
        return

    tasks = []

    for bloom_level_index, bloom_level_name in enumerate(
        constants.BLOOM_LEVELS_ORDERED
    ):
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
                f"question_{bloom_level_index + 1}.txt",
            )
            description = f"{bloom_level_name}"

            tasks.append(
                (llm_name, clients, formatted_prompt, output_path, description)
            )

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(generate_task_exp2, *task): task for task in tasks}

        with tqdm(
            total=len(tasks), desc=f"Exp 2b {get_progress()}", unit="task"
        ) as pbar:
            for future in as_completed(futures):
                future.result()
                pbar.set_description(f"Exp 2b {get_progress()}")
                pbar.update(1)


def run_exp_2c(clients):
    safe_print("\n[INFO] Experiment 2c: Combined Type and Bloom")
    reset_counters()
    bloom_data = get_bloom()

    tanenbaum_text_path = os.path.join(
        constants.INPUT_SOURCES_PATH,
        "tanenbaum",
        f"layer{constants.TANENBAUM_LAYER_FOR_EXP2}.txt",
    )
    base_text_for_exp2 = load_txt(tanenbaum_text_path)

    prompt_template_both = load_prompt(
        os.path.join(constants.PROMPT_TEMPLATES_PATH, "experiment", "exp2_both.md")
    )
    if not prompt_template_both:
        return

    tasks = []

    for q_type in constants.EXP2_QUESTION_TYPES:
        q_type_slug = slugify(q_type)
        for i, bloom_level_name in enumerate(constants.BLOOM_LEVELS_ORDERED):
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
                    f"question_{i + 1}.txt",
                )
                description = f"{q_type} {bloom_level_name}"

                tasks.append(
                    (llm_name, clients, formatted_prompt, output_path, description)
                )

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(generate_task_exp2, *task): task for task in tasks}

        with tqdm(
            total=len(tasks), desc=f"Exp 2c {get_progress()}", unit="task"
        ) as pbar:
            for future in as_completed(futures):
                future.result()
                pbar.set_description(f"Exp 2c {get_progress()}")
                pbar.update(1)
