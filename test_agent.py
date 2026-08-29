from pathlib import Path

from minicoder.agent import Agent


def main():
    agent = Agent(
        workspace=Path("demo_project")
    )

    answer = agent.run(
        "Find where the hello function is defined, "
        "read the relevant file, and explain what it does."
    )

    print("===== AGENT ANSWER =====")
    print(answer)


if __name__ == "__main__":
    main()