import sys
from pathlib import Path

from minicoder.agent import Agent


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

        answer = agent.run(
            user_input
        )

        print()
        print(answer)
        print()


if __name__ == "__main__":
    main()