from pathlib import Path

from minicoder.agent import Agent


def main():
    agent = Agent(
        workspace=Path("demo_todo")
    )

    answer = agent.run(
        "Run hello.py and tell me what it prints."
    )

    print("===== AGENT ANSWER =====")
    print(answer)


if __name__ == "__main__":
    main()