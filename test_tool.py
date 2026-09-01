from pathlib import Path

from minicoder.tools.shell import run_command


def show_result(
    title: str,
    result: dict,
) -> None:
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)
    print(result)


def main():
    workspace = Path(".").resolve()

    # Test 1: 普通成功命令
    result = run_command(
        workspace=workspace,
        command=(
            'python -c "print(\'hello\')"'
        ),
    )

    show_result(
        "TEST 1 - normal stdout",
        result,
    )

    # Test 2: stderr 有内容，但是 exit code 仍然为 0
    result = run_command(
        workspace=workspace,
        command=(
            'python -c '
            '"import sys; '
            'print(\'warning\', file=sys.stderr)"'
        ),
    )

    show_result(
        "TEST 2 - stderr with success",
        result,
    )

    # Test 3: 非零退出码
    result = run_command(
        workspace=workspace,
        command=(
            'python -c '
            '"import sys; sys.exit(3)"'
        ),
    )

    show_result(
        "TEST 3 - non-zero exit code",
        result,
    )

    # Test 4: 中文 / Unicode 输出
    result = run_command(
        workspace=workspace,
        command=(
            'python -c '
            '"print(\'你好 MiniCoder\')"'
        ),
    )

    show_result(
        "TEST 4 - unicode stdout",
        result,
    )

    # Test 5: 大量输出，应该被截断
    result = run_command(
        workspace=workspace,
        command=(
            'python -c '
            '"print(\'A\' * 30000)"'
        ),
    )

    show_result(
        "TEST 5 - output truncation",
        result,
    )

    # Test 6: timeout
    result = run_command(
        workspace=workspace,
        command=(
            'python -c '
            '"import time; '
            'print(\'before sleep\'); '
            'time.sleep(3)"'
        ),
        timeout=1,
    )

    show_result(
        "TEST 6 - timeout",
        result,
    )

    # Test 7: dangerous command block
    result = run_command(
        workspace=workspace,
        command="shutdown /s",
    )

    show_result(
        "TEST 7 - blocked command",
        result,
    )


if __name__ == "__main__":
    main()