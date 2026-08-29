from pathlib import Path

from minicoder.tools.filesystem import edit_file


def main():
    workspace = Path(
        "demo_project"
    ).resolve()

    result = edit_file(
        workspace=workspace,
        path="../../notes.txt",
        old_text='MiniCoder',
        new_text='return "hello"',
    )

    print(result)


if __name__ == "__main__":
    main()