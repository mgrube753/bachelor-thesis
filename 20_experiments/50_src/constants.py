import os

BASE_PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
EXPERIMENTS_BASE_PATH = os.path.join(BASE_PROJECT_PATH, "20_experiments")
INPUT_SOURCES_PATH = os.path.join(EXPERIMENTS_BASE_PATH, "30_input_sources")
PROMPT_TEMPLATES_PATH = os.path.join(EXPERIMENTS_BASE_PATH, "40_prompts")
EVAL_PATH = os.path.join(EXPERIMENTS_BASE_PATH, "60_eval")
EXP1_PATH = os.path.join(EXPERIMENTS_BASE_PATH, "10_exp1")
EXP2_PATH = os.path.join(EXPERIMENTS_BASE_PATH, "20_exp2")

LLM_MODEL_IDS = {
    "google": "gemini-2.5-flash-preview-05-20",
    "anthropic": "claude-3-7-sonnet-20250219",
    "openai": "o3",
}
LLM_NAMES = LLM_MODEL_IDS.keys()
EMBEDDING_MODEL_ID = "T-Systems-onsite/cross-en-de-roberta-sentence-transformer"
REQUEST_DELAY_SECONDS = 10

EXP1_PROMPT_TYPES = ["exp1_common_prompt", "exp1_complex_prompt"]
EXP1_SOURCE_TYPES_A = ["script", "transcript", "tanenbaum"]
EXP1_SOURCE_TYPE_B = "script"
EXP1_SCRIPT_SUBDIR_A = "common"
EXP1_SCRIPT_SUBDIR_B = "manipulated"
LAYERS = list(range(1, 8))

TANENBAUM_LAYER_FOR_EXP2 = 2
EXP2_QUESTION_TYPES = ["Multiple-Choice", "Open-Ended"]
BLOOM_LEVELS_ORDERED = [
    "Remembering",
    "Understanding",
    "Applying",
    "Analyzing",
    "Evaluating",
    "Creating",
]

BLOOM_DATA_FILE = os.path.join(PROMPT_TEMPLATES_PATH, "experiment", "bloom.md")
