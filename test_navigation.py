import navigation_logic

ALLOWED_ACTIONS = {"FORWARD", "LEFT", "RIGHT", "STOP"}


def run_case(name, sensor_data):
    action = navigation_logic.navigate(sensor_data)
    print(f"[{name}] {sensor_data} -> {action}")

    if action not in ALLOWED_ACTIONS:
        raise AssertionError(f"Invalid action: {action}")


def main():
    run_case("front_clear", {
        "front": True,
        "left": True,
        "right": True,
        "goal_reached": False
    })

    run_case("front_blocked_left_clear", {
        "front": False,
        "left": True,
        "right": False,
        "goal_reached": False
    })

    run_case("front_blocked_right_clear", {
        "front": False,
        "left": False,
        "right": True,
        "goal_reached": False
    })

    run_case("all_blocked", {
        "front": False,
        "left": False,
        "right": False,
        "goal_reached": False
    })

    run_case("goal_reached", {
        "front": True,
        "left": True,
        "right": True,
        "goal_reached": True
    })

    print("all tests passed")


if __name__ == "__main__":
    main()