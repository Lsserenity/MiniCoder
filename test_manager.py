import json
from pathlib import Path

from minicoder.llm.openai_client import LLMClient
from minicoder.tools.definitions import TOOLS
from minicoder.tools.manager import ToolManager


def main():
    llm = LLMClient()

    manager = ToolManager(
        workspace=Path("demo_project")
    )

    messages = [
        {
            "role": "system",
            "content": (
                "You are a coding agent working "
                "inside a local project. "
                "Use available tools when needed."
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

    # 第一次调用 LLM：
    # 期望模型返回一个 list_files tool call。
    message = llm.chat(
        messages=messages,
        tools=TOOLS,
    )

    # 保存 assistant 的完整回复。
    messages.append(message)

    if not message.tool_calls:
        print("No tool call returned.")
        print(message.content)
        return

    # 第一版暂时只处理第一个 tool call。
    tool_call = message.tool_calls[0]

    result = manager.execute(tool_call)

    # 把 Python dict 转成 JSON 字符串，
    # 再作为 tool message 发给模型。
    tool_message = {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": json.dumps(
            result,
            ensure_ascii=False,
        ),
    }

    messages.append(tool_message)

    # 第二次调用 LLM：
    # 此时模型已经能看到刚才的工具执行结果。
    final_message = llm.chat(
        messages=messages,
        tools=TOOLS,
    )

    print("===== TOOL RESULT =====")
    print(result)

    print()

    print("===== FINAL ANSWER =====")
    print(final_message.content)


if __name__ == "__main__":
    main()