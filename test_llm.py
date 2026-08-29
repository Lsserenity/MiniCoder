from minicoder.llm.openai_client import LLMClient
from minicoder.tools.definitions import TOOLS

def main():
    llm = LLMClient()

    messages = [
        {
            "role": "system",
            "content": (
                "You are a coding agent working "
                "inside a local project. "
                "Use available tools when you need "
                "information about the project."
            ),
        },
        {
            "role": "user",
            "content": (
                "Please inspect the files "
                "in the current project."
            ),
        },
    ]

    message = llm.chat(
        messages=messages,
        tools=TOOLS,
    )

    print("===== MODEL CONTENT =====")
    print(message.content)

    print()

    print("===== TOOL CALLS =====")
    print(message.tool_calls)

    if message.tool_calls:
        call = message.tool_calls[0]

        print()
        print("===== FIRST TOOL CALL =====")

        print("ID:")
        print(call.id)

        print()

        print("Name:")
        print(call.function.name)

        print()

        print("Arguments:")
        print(call.function.arguments)

if __name__ == "__main__":
    main()