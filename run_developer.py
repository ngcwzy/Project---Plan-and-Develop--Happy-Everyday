import json
from pathlib import Path

from developer_agent import run_developer

PLAN_PATH = Path("plan.json")
OUTPUT_PATH = Path("navigation_logic.py")


def main():
    if not PLAN_PATH.exists():
        raise FileNotFoundError("plan.json not found")

    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    code = run_developer(plan)

    OUTPUT_PATH.write_text(code + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()