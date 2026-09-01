import sys
from pathlib import Path

from minicoder.agent import Agent
from minicoder.tools.shell import run_command

# 展示当前计划的函数
def print_plan(agent: Agent) -> None:
    plan = agent.plan_state.to_dict()
    steps = plan["steps"]

    if not steps:
        print("No active plan.")
        return

    print("Plan:")

    for step in steps:
        status = step["status"]
        description = step["description"]

        if status == "completed":
            marker = "[x]"
        elif status == "in_progress":
            marker = "[>]"
        else:
            marker = "[ ]"

        print(
            f"{marker} {description}"
        )

# 展示文件修改diff的函数
def print_diff(
    workspace: Path,
) -> None:
    # 先检查当前 workspace 是否位于 Git working tree 中
    repo_check = run_command(
        workspace=workspace,
        command=(
            "git rev-parse "
            "--is-inside-work-tree"
        ),
    )

    if not repo_check["success"]:
        print(
            "This workspace is not inside "
            "a Git repository."
        )
        return

    # 只显示当前 workspace 范围内的修改
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
            f"Unable to show diff: {error}"
        )
        return

    diff = result["stdout"]

    if not diff.strip():
        print(
            "No uncommitted changes."
        )
        return

    print(diff)

# 打印 help 说明
def print_help() -> None:
    print("Commands:")
    print("  /help  Show available commands")
    print("  /plan  Show the current task plan")
    print("  /diff  Show uncommitted workspace changes")
    print("  /exit  Exit MiniCoder")

# 主函数
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
            f"Workspace does not exist: "
            f"{workspace}"
        )
        return

    if not workspace.is_dir():
        print(
            f"Workspace is not a directory: "
            f"{workspace}"
        )
        return

    agent = Agent(
        workspace=workspace
    )

    print("MiniCoder")
    print(
        f"Workspace: {workspace}"
    )
    print(
        "Type /exit to quit."
    )
    print(
        "Type /help for commands."
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
            print("Bye.")
            break

        if not user_input:
            continue

        if user_input == "/exit":
            print("Bye.")
            break

        if user_input == "/plan":
            print_plan(agent)
            print()
            continue

        if user_input == "/diff":
            print_diff(workspace)
            print()
            continue

        if user_input == "/help":
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