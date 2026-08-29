from pathlib import Path

from minicoder.agent import Agent


def main():
    agent = Agent(
        workspace=Path("demo_project")
    )

    answer = agent.run(
        "Inspect hello.py and change the hello() function "
        'so that it returns "Hello from MiniCoder!" instead.'
    )

    print("===== AGENT ANSWER =====")
    print(answer)


if __name__ == "__main__":
    main()