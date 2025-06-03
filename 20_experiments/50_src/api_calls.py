import time
import constants
from constants import REQUEST_DELAY_SECONDS
from google.genai import types


def gen_with_google(client, prompt_text, model_id, max_tokens):
    # https://github.com/googleapis/python-genai, https://ai.google.dev/gemini-api/docs/thinking https://ai.google.dev/gemini-api/docs/text-generation https://cloud.google.com/vertex-ai/docs/reference/rest/v1/GenerateContentResponse
    try:
        response = client.models.generate_content(
            model=model_id,
            contents=prompt_text,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=1100),
                max_output_tokens=max_tokens,
            ),
        )

        candidate = response.candidates[0]
        if candidate.finish_reason == "MAX_TOKENS":
            print(f"\n[WARNING] {model_id} ran out of tokens")
            if response.text:
                print(f"[INFO] Partial output available for {model_id}")
                return response.text
            else:
                print(f"[WARNING] No output available for {model_id}")
                return None
        return response.text
    except Exception as e:
        print(f"[ERROR] Gemini API ({model_id}): {e}")
        return None


def gen_with_anthropic(client, prompt_text, model_id, max_tokens):
    # https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking#tips-for-making-the-best-use-of-extended-thinking-mode https://docs.anthropic.com/en/api/handling-stop-reasons
    try:
        response = client.messages.create(
            model=model_id,
            thinking={"type": "enabled", "budget_tokens": 1100},
            messages=[{"role": "user", "content": prompt_text}],
            max_tokens=max_tokens,
        )

        if response.stop_reason == "max_tokens":
            print(f"\n[WARNING] {model_id} ran out of tokens")
            for block in response.content:
                if block.type == "text":
                    print(f"[INFO] Partial output available for {model_id}")
                    return block.text
            print(f"[WARNING] No output available for {model_id}")
            return None

        for block in response.content:
            if block.type == "text":
                return block.text
    except Exception as e:
        print(f"[ERROR] Claude API ({model_id}): {e}")
        return None


def gen_with_openai(client, prompt_text, model_id, max_tokens):
    # https://platform.openai.com/docs/quickstart?api-mode=responses&lang=python, https://platform.openai.com/docs/guides/reasoning?api-mode=responses
    try:
        response = client.responses.create(
            model=model_id,
            reasoning={"effort": "medium"},
            input=[{"role": "user", "content": prompt_text}],
            max_output_tokens=max_tokens,
        )
        # based on https://platform.openai.com/docs/api-reference/responses-streaming/response/incomplete[]
        if (
            response.status == "incomplete"
            and response.incomplete_details.reason == "max_output_tokens"
        ):
            print(f"\n[WARNING] {model_id} ran out of tokens")
            if response.output_text:
                print(f"[INFO] Partial output available for {model_id}")
                return response.output_text
            else:
                print(f"[WARNING] {model_id} ran out of tokens during reasoning")
                return None

        return response.output_text

    except Exception as e:
        print(f"[ERROR] OpenAI API ({model_id}): {e}")
        return None


def llm_generation(llm_name, clients, prompt_text, max_tokens):
    client = clients.get(llm_name)
    model_id = constants.LLM_MODEL_IDS.get(llm_name)

    if not client or not model_id:
        print(f"[ERROR] Client or model_id not found for LLM: {llm_name}")
        return None

    result = None
    if llm_name == "google":
        result = gen_with_google(client, prompt_text, model_id, max_tokens)
    elif llm_name == "anthropic":
        result = gen_with_anthropic(client, prompt_text, model_id, max_tokens)
    elif llm_name == "openai":
        result = gen_with_openai(client, prompt_text, model_id, max_tokens)
    else:
        print(f"[ERROR] Unknown LLM name '{llm_name}'")
        return None

    time.sleep(REQUEST_DELAY_SECONDS)
    return result
