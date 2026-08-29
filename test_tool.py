from pathlib import Path

from minicoder.tools.filesystem import list_files


def main():
    workspace = Path("demo_project").resolve()

    result = list_files(
        workspace=workspace,
        path=".",
    )

    print(result)


if __name__ == "__main__":
    main()