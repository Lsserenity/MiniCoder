from pathlib import Path

from minicoder.agent import Agent


def main():
    agent = Agent(
        workspace=Path("demo_todo")
    )

    answer = agent.run(
        "Inspect this project, run its test suite, and explain whether "
        "the todo implementation is currently correct. "
        "Use an explicit plan for this multi-step task."
    )

    print("===== AGENT ANSWER =====")
    print(answer)

    print()
    print("===== FINAL PLAN =====")
    print(
        agent.plan_state.to_dict()
    )

if __name__ == "__main__":
    main()