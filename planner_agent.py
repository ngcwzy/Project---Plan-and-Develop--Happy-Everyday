import json
import re
from ollama import chat

MODEL = "qwen2.5:7b"
ALLOWED_ACTIONS = {"FORWARD", "LEFT", "RIGHT", "STOP"}

SYSTEM_PROMPT = """You are the Planner Agent for a robot navigation system.
Return only a JSON object. Do not include markdown.
The JSON must have:
- strategy: a non-empty string
- decisions: a non-empty list of objects, each with condition and action
- stop_condition: a non-empty string
Allowed actions are only: FORWARD, LEFT, RIGHT, STOP.
Use the requirements as context. Keep the plan deterministic and safe."""


def _get_content(response):
    if isinstance(response, dict):
        return response["message"]["content"]
    return response.message.content


def _extract_json(text):
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            raise
        return json.loads(match.group(0))


def validate_plan(data):
    if not isinstance(data, dict):
        raise TypeError("plan must be a dict")

    strategy = data.get("strategy")
    if not isinstance(strategy, str) or not strategy.strip():
        raise ValueError("strategy must be a non-empty string")

    decisions = data.get("decisions")
    if not isinstance(decisions, list) or not decisions:
        raise ValueError("decisions must be a non-empty list")

    for i, item in enumerate(decisions):
        if not isinstance(item, dict):
            raise TypeError(f"decisions[{i}] must be a dict")

        condition = item.get("condition")
        action = item.get("action")

        if not isinstance(condition, str) or not condition.strip():
            raise ValueError(f"decisions[{i}].condition must be a non-empty string")

        if action not in ALLOWED_ACTIONS:
            raise ValueError(
                f"decisions[{i}].action must be one of {sorted(ALLOWED_ACTIONS)}"
            )

    stop_condition = data.get("stop_condition")
    if not isinstance(stop_condition, str) or not stop_condition.strip():
        raise ValueError("stop_condition must be a non-empty string")

    return data


def run_planner(requirement):
    if not isinstance(requirement, dict):
        raise TypeError("requirement must be a dict")

    required_keys = ["goal", "allowed_actions", "safe_stop", "avoid_obstacles"]
    for key in required_keys:
        if key not in requirement:
            raise ValueError(f"requirement missing key: {key}")

    if not isinstance(requirement["allowed_actions"], list):
        raise TypeError("allowed_actions must be a list")

    for action in requirement["allowed_actions"]:
        if action not in ALLOWED_ACTIONS:
            raise ValueError(f"unsupported action: {action}")

    if not isinstance(requirement["safe_stop"], bool):
        raise TypeError("safe_stop must be a bool")

    if not isinstance(requirement["avoid_obstacles"], bool):
        raise TypeError("avoid_obstacles must be a bool")

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": json.dumps(requirement, ensure_ascii=False)},
    ]

    response = chat(
        model=MODEL,
        messages=messages,
        format="json",
        options={"temperature": 0.2},
    )

    content = _get_content(response)
    plan = _extract_json(content)
    return validate_plan(plan)