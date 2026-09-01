import sys
from pathlib import Path

from minicoder import __version__
from minicoder.agent import Agent
from minicoder.tools.shell import run_command
from minicoder.ui.terminal import (
    BOLD,
    CYAN,
    DIM,
    GREEN,
    RED,
    YELLOW,
    style,
)


def print_banner(
    workspace: Path,
) -> None:
    print(
        f"{style('::', CYAN)} "
        f"{style('MiniCoder', CYAN, BOLD)} "
        f"{style('v' + __version__, DIM)}"
    )

    print(
        f"{style('::', CYAN)} "
        f"{style('lightweight local coding agent', DIM)}"
    )

    print()

    print(
        f"{style('workspace', GREEN)}  "
        f"{workspace}"
    )

    print(
        f"{style('type', GREEN)}       "
        f"{style('/help for commands', DIM)}"
    )


def print_plan(
    agent: Agent,
) -> None:
    plan = agent.plan_state.to_dict()
    steps = plan["steps"]

    if not steps:
        print(
            style(
                "No active plan.",
                DIM,
            )
        )
        return

    print(
        style(
            "Plan",
            CYAN,
            BOLD,
        )
    )

    for step in steps:
        status = step["status"]
        description = step["description"]

        if status == "completed":
            marker = style(
                "[x]",
                GREEN,
            )

        elif status == "in_progress":
            marker = style(
                "[>]",
                YELLOW,
                BOLD,
            )

        else:
            marker = style(
                "[ ]",
                DIM,
            )

        print(
            f"{marker} {description}"
        )


def print_diff(
    workspace: Path,
) -> None:
    repo_check = run_command(
        workspace=workspace,
        command=(
            "git rev-parse "
            "--is-inside-work-tree"
        ),
    )

    if not repo_check["success"]:
        print(
            style(
                (
                    "This workspace is not inside "
                    "a Git repository."
                ),
                YELLOW,
            )
        )
        return

    result = run_command(
        workspace=workspace,
        command="git diff -- .",
    )

    if not result["success"]:
        error = (
            result.get("stderr")
            or result.get("error")
            or "Unknown error."
        )

        print(
            style(
                f"Unable to show diff: {error}",
                RED,
            )
        )
        return

    diff = result["stdout"]

    if not diff.strip():
        print(
            style(
                "No uncommitted changes.",
                DIM,
            )
        )
        return

    print(diff)


def print_help() -> None:
    print(
        style(
            "Commands",
            BOLD,
            CYAN,
        )
    )

    print(
        f"  {style('/help', GREEN)}  "
        "Show available commands"
    )

    print(
        f"  {style('/plan', GREEN)}  "
        "Show the current task plan"
    )

    print(
        f"  {style('/diff', GREEN)}  "
        "Show uncommitted workspace changes"
    )

    print(
        f"  {style('/exit', GREEN)}  "
        "Exit MiniCoder"
    )


def confirm_tool_call(
    tool_name: str,
    arguments: dict,
    reason: str,
) -> bool:
    print()

    print(
        style(
            "[!] Confirmation required",
            YELLOW,
            BOLD,
        )
    )

    print(
        f"{style('Tool', BOLD)}     "
        f"{tool_name}"
    )

    if tool_name == "run_command":
        command = arguments.get(
            "command",
            "",
        )

        print(
            f"{style('Command', BOLD)}  "
            f"{command}"
        )

    else:
        print(
            f"{style('Arguments', BOLD)} "
            f"{arguments}"
        )

    print(
        f"{style('Reason', BOLD)}   "
        f"{reason}"
    )

    print()

    answer = input(
        style(
            "Allow once? [y/N] ",
            YELLOW,
        )
    ).strip().lower()

    return answer in {
        "y",
        "yes",
    }


def main() -> None:
    if len(sys.argv) >= 2:
        workspace = Path(
            sys.argv[1]
        )
    else:
        workspace = Path(".")

    workspace = workspace.resolve()

    if not workspace.exists():
        print(
            style(
                (
                    "Workspace does not exist: "
                    f"{workspace}"
                ),
                RED,
            )
        )
        return

    if not workspace.is_dir():
        print(
            style(
                (
                    "Workspace is not a directory: "
                    f"{workspace}"
                ),
                RED,
            )
        )
        return

    try:
        agent = Agent(
            workspace=workspace,
            confirmation_handler=confirm_tool_call,
        )

    except RuntimeError as exc:
        print(
            style(
                f"Unable to start MiniCoder: {exc}",
                RED,
            )
        )
        return

    print_banner(
        workspace
    )
    print()

    while True:
        try:
            user_input = input("> ").strip()

        except (
            EOFError,
            KeyboardInterrupt,
        ):
            print()
            print(
                style(
                    "Bye.",
                    DIM,
                )
            )
            break

        if not user_input:
            continue

        command = user_input.lower()

        if command in {
            "/exit",
            "exit",
            "/quit",
            "quit",
        }:
            print(
                style(
                    "Bye.",
                    DIM,
                )
            )
            break

        if command == "/plan":
            print_plan(
                agent
            )
            print()
            continue

        if command == "/diff":
            print_diff(
                workspace
            )
            print()
            continue

        if command in {
            "/help",
            "help",
        }:
            print_help()
            print()
            continue

        answer = agent.run(
            user_input
        )

        print()
        print(answer)
        print()


if __name__ == "__main__":
    main()