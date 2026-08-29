from pathlib import Path

from minicoder.tools.filesystem import write_file


def main():
    workspace = Path(
        "demo_project"
    ).resolve()

    result = write_file(
        workspace=workspace,
        path="../../danger.txt",
        content="MiniCoder works!",
        overwrite=True,
    )

    print(result)


if __name__ == "__main__":
    main()