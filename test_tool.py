from pathlib import Path

from minicoder.tools.manager import ToolManager


class MockFunction:
    def __init__(
        self,
        name: str,
        arguments: str,
    ):
        self.name = name
        self.arguments = arguments


class MockToolCall:
    def __init__(
        self,
        name: str,
        arguments: str,
    ):
        self.function = MockFunction(
            name=name,
            arguments=arguments,
        )


def run_test(
    manager: ToolManager,
    name: str,
    arguments: str,
):
    print("=" * 60)
    print("tool:", name)
    print("arguments:", arguments)

    tool_call = MockToolCall(
        name=name,
        arguments=arguments,
    )

    result = manager.execute(
        tool_call
    )

    print("result:")
    print(result)
    print()


def main():
    workspace = Path(
        "demo_project"
    ).resolve()

    manager = ToolManager(
        workspace=workspace
    )

    # 1. 普通命令：应该允许并真正执行
    run_test(
        manager,
        "run_command",
        '{"command": "python hello.py"}',
    )

    # 2. 明显危险命令：应该被 PolicyEngine 拒绝
    run_test(
        manager,
        "run_command",
        '{"command": "shutdown /s"}',
    )

    # 3. 修改开发环境的命令：
    # 当前应该要求 confirmation，并且不能真正执行
    run_test(
        manager,
        "run_command",
        '{"command": "pip install flask"}',
    )

    # 4. 普通读文件工具：应该正常执行
    run_test(
        manager,
        "read_file",
        '{"path": "hello.py"}',
    )


if __name__ == "__main__":
    main()