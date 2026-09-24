import json
from pathlib import Path

from planner_agent import run_planner

REQUIREMENTS_PATH = Path("requirements.json")
PLAN_PATH = Path("plan.json")


def main():
    if not REQUIREMENTS_PATH.exists():
        raise FileNotFoundError("requirements.json not found")

    requirement = json.loads(REQUIREMENTS_PATH.read_text(encoding="utf-8"))
    plan = run_planner(requirement)

    PLAN_PATH.write_text(
        json.dumps(plan, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"Wrote {PLAN_PATH}")


if __name__ == "__main__":
    main()