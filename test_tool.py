from pathlib import Path

from minicoder.tools.search import search_text


def main():
    workspace = Path(
        "demo_project"
    ).resolve()

    result = search_text(
        workspace=workspace,
        query="",
        path=".",
    )

    print(result)


if __name__ == "__main__":
    main()