import json
import re

def clean_llm_response(text: str) -> str:
    if not text:
        raise ValueError("Empty LLM response")

    # remove markdown blocks
    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)

    # remove null chars (your crash reason)
    text = text.replace("\x00", "")

    # trim spaces
    text = text.strip()

    return text


def safe_parse_json(text: str):
    cleaned = clean_llm_response(text)
    return json.loads(cleaned)