import json
import re
from ollama import chat

MODEL = "qwen2.5:7b"
ALLOWED_ACTIONS = {"FORWARD", "LEFT", "RIGHT", "STOP"}

SYSTEM_PROMPT = """You are the Developer Agent for a robot navigation system.
Return only Python code. Do not include markdown fences.
The code must define a function named navigate(sensor_data).
The function must return exactly one of: FORWARD, LEFT, RIGHT, STOP.
The code must follow the given plan, including the stop condition.
Do not use external libraries. Do not access files or network.
The sensor_data argument is a dict. Use front, left, right, and goal_reached when needed."""


def _get_content(response):
    if isinstance(response, dict):
        return response["message"]["content"]
    return response.message.content


def _extract_code(text):
    text = text.strip()
    text = re.sub(r"^```(?:python)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def validate_code(code):
    if not isinstance(code, str):
        raise TypeError("code must be a string")

    code = code.strip()
    if not code:
        raise ValueError("code must not be empty")

    if "def navigate" not in code:
        raise ValueError("code must define navigate(sensor_data)")

    compile(code, "navigation_logic.py", "exec")
    return code


def run_developer(plan):
    if not isinstance(plan, dict):
        raise TypeError("plan must be a dict")

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": json.dumps(plan, ensure_ascii=False)},
    ]

    response = chat(
        model=MODEL,
        messages=messages,
        options={"temperature": 0.2},
    )

    content = _get_content(response)
    code = _extract_code(content)
    return validate_code(code)