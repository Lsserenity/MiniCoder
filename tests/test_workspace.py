from pathlib import Path

from minicoder.tools.filesystem import (
    read_file,
)


def test_read_file_blocks_workspace_escape(
    tmp_path: Path,
) -> None:
    result = read_file(
        workspace=tmp_path,
        path="../outside.txt",
    )

    assert result["success"] is False

def test_read_file_is_bounded(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "large.txt"

    file_path.write_text(
        "\n".join(
            f"line {i}"
            for i in range(1500)
        ),
        encoding="utf-8",
    )

    result = read_file(
        workspace=tmp_path,
        path="large.txt",
    )

    assert result["success"] is True
    assert result["truncated"] is True
    assert result["end_line"] == 1000
    assert result["total_lines"] == 1500