from pathlib import Path

from minicoder.tools.filesystem import list_files, read_file


def main():
    workspace = Path("demo_project").resolve()

    result = read_file(
        workspace=workspace,
        path="hello.txt",
    )

    print(result)


if __name__ == "__main__":
    main()