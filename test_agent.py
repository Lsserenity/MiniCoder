from pathlib import Path

from minicoder.agent import Agent


def main():
    agent = Agent(
        workspace=Path("demo_todo")
    )

    answer = agent.run(
        "Add a delete_todo(todo_id) function to this project. "
        "It should delete and return the todo with the given id. "
        "If the id does not exist, it should raise KeyError. "
        "Add tests for both successful deletion and the missing-id case. "
        "Run the full test suite and fix any failures before finishing."
    )

    print("===== AGENT ANSWER =====")
    print(answer)


if __name__ == "__main__":
    main()