from pathlib import Path

from minicoder.tools.filesystem import read_file


def main():
    workspace = Path(
        "demo_project"
    ).resolve()

    large_file = (
        workspace / "large.txt"
    )

    content = "\n".join(
        f"line {i}"
        for i in range(1, 10001)
    )

    large_file.write_text(
        content,
        encoding="utf-8",
    )

    result = read_file(
        workspace=workspace,
        path="large.txt",
        start_line = 10000,
    )

    print(
        "start_line:",
        result["start_line"],
    )
    print(
        "end_line:",
        result["end_line"],
    )
    print(
        "total_lines:",
        result["total_lines"],
    )
    print(
        "truncated:",
        result["truncated"],
    )


if __name__ == "__main__":
    main()