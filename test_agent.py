from pathlib import Path

from minicoder.agent import Agent


from pathlib import Path

from minicoder.agent import Agent


def main():
    agent = Agent(
        workspace=Path("demo_project")
    )

    answer = agent.run(
        "Replace the contents of notes.txt with exactly: "
        "MiniCoder updated this file!"
    )

    print("===== AGENT ANSWER =====")
    print(answer)


if __name__ == "__main__":
    main()