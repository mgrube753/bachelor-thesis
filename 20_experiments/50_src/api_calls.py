import time
import constants
from constants import REQUEST_DELAY_SECONDS
from google.genai import types


def gen_with_google(client, prompt_text, model_id):
    # https://github.com/googleapis/python-genai, https://ai.google.dev/gemini-api/docs/thinking
    try:
        response = client.models.generate_content(
            model=model_id,
            contents=prompt_text,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=1100)
            ),
        )
        return response.text
    except Exception as e:
        print(f"[ERROR] Gemini API ({model_id}): {e}")
        return None


def gen_with_anthropic(client, prompt_text, model_id):
    # https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking#tips-for-making-the-best-use-of-extended-thinking-mode
    try:
        response = client.messages.create(
            model=model_id,
            thinking={"type": "enabled", "budget_tokens": 1100},
            messages=[{"role": "user", "content": prompt_text}],
            max_tokens=1400,
        )
        for block in response.content:
            if block.type == "text":
                return block.text
    except Exception as e:
        print(f"[ERROR] Claude API ({model_id}): {e}")
        return None


def gen_with_openai(client, prompt_text, model_id):
    # https://platform.openai.com/docs/quickstart?api-mode=responses&lang=python, https://platform.openai.com/docs/guides/reasoning?api-mode=responses
    try:
        response = client.responses.create(
            model=model_id,
            reasoning={"effort": "medium"},
            input=[{"role": "user", "content": prompt_text}],
            max_output_tokens=1400,
        )
        if (
            response.status == "incomplete"
            and response.incomplete_details.reason == "max_output_tokens"
        ):
            print("[WARNING] Ran out of tokens")
            if response.output_text:
                print("[INFO] Partial output available")
                return response.output_text
            else:
                print("[WARNING] Ran out of tokens during reasoning")
                return None

        return response.output_text

    except Exception as e:
        print(f"[ERROR] OpenAI API ({model_id}): {e}")
        return None


def llm_generation(llm_name, clients, prompt_text):
    client = clients.get(llm_name)
    model_id = constants.LLM_MODEL_IDS.get(llm_name)

    if not client or not model_id:
        print(f"[ERROR] Client or model_id not found for LLM: {llm_name}")
        return None

    # print(f"[INFO] Generating with {llm_name} {model_id}...")

    result = None
    if llm_name == "google":
        result = gen_with_google(client, prompt_text, model_id)
    elif llm_name == "anthropic":
        result = gen_with_anthropic(client, prompt_text, model_id)
    elif llm_name == "openai":
        result = gen_with_openai(client, prompt_text, model_id)
    else:
        print(f"[ERROR] Unknown LLM name '{llm_name}'")
        return None

    time.sleep(REQUEST_DELAY_SECONDS)
    return result
