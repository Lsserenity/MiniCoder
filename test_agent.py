from pathlib import Path

from minicoder.agent import Agent


def main():
    agent = Agent(
        workspace=Path("demo_project")
    )

    answer = agent.run(
        "Run hello.py. If it fails, inspect the error and fix the problem."
    )

    print("===== AGENT ANSWER =====")
    print(answer)


if __name__ == "__main__":
    main()