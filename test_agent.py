from pathlib import Path

from minicoder.agent import Agent


def main():
    agent = Agent(
        workspace=Path("demo_todo")
    )

    answer = agent.run(
        "Run the test suite, diagnose any failures, fix the underlying bug, "
        "and rerun the tests until they pass."
    )

    print("===== AGENT ANSWER =====")
    print(answer)


if __name__ == "__main__":
    main()