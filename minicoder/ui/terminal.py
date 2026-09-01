import json
import os
import sys


RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"


def supports_color() -> bool:
    if os.getenv("NO_COLOR") is not None:
        return False

    return sys.stdout.isatty()


def style(
    text: str,
    *styles: str,
) -> str:
    if not supports_color():
        return text

    prefix = "".join(styles)

    return (
        f"{prefix}"
        f"{text}"
        f"{RESET}"
    )


def pretty_json(
    data: object,
) -> str:
    return json.dumps(
        data,
        indent=2,
        ensure_ascii=False,
    )

def format_tool_result(
    tool_name: str,
    result: dict,
) -> str:
    success = result.get(
        "success",
        False,
    )

    if not success:
        error = (
            result.get("error")
            or result.get("stderr")
            or "Unknown error."
        )

        return (
            f"failed\n"
            f"  error: {error}"
        )

    if tool_name == "read_file":
        return (
            "success\n"
            f"  path: "
            f"{result.get('path')}\n"
            f"  lines: "
            f"{result.get('start_line')}-"
            f"{result.get('end_line')} / "
            f"{result.get('total_lines')}\n"
            f"  truncated: "
            f"{str(result.get('truncated')).lower()}"
        )

    if tool_name == "run_command":
        return (
            "success\n"
            f"  exit_code: "
            f"{result.get('exit_code')}\n"
            f"  timed_out: "
            f"{str(result.get('timed_out')).lower()}\n"
            f"  stdout_truncated: "
            f"{str(result.get('stdout_truncated')).lower()}"
        )

    if tool_name == "list_files":
        entries = result.get(
            "entries",
            [],
        )

        return (
            "success\n"
            f"  path: "
            f"{result.get('path')}\n"
            f"  entries: "
            f"{len(entries)}"
        )

    if tool_name == "search_text":
        matches = result.get(
            "matches",
            [],
        )

        return (
            "success\n"
            f"  matches: "
            f"{len(matches)}\n"
            f"  truncated: "
            f"{str(result.get('truncated')).lower()}"
        )

    if tool_name == "update_plan":
        plan = result.get(
            "plan",
            {},
        )

        steps = plan.get(
            "steps",
            [],
        )

        lines = [
            "success"
        ]

        for step in steps:
            status = step.get(
                "status"
            )

            if status == "completed":
                marker = "[x]"
            elif status == "in_progress":
                marker = "[>]"
            else:
                marker = "[ ]"

            lines.append(
                f"  {marker} "
                f"{step.get('description')}"
            )

        return "\n".join(lines)

    return pretty_json(
        result
    )