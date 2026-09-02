from pathlib import Path

from minicoder.tools.filesystem import (
    edit_file,
    read_file,
    write_file,
)
from minicoder.tools.search import search_text


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


def test_read_file_blocks_sensitive_file(
    tmp_path: Path,
) -> None:
    (tmp_path / ".env").write_text(
        "MODEL_API_KEY=secret",
        encoding="utf-8",
    )

    result = read_file(
        workspace=tmp_path,
        path=".env",
    )

    assert result["success"] is False
    assert "sensitive" in result["error"].lower()


def test_write_file_blocks_sensitive_file(
    tmp_path: Path,
) -> None:
    result = write_file(
        workspace=tmp_path,
        path=".env",
        content="MODEL_API_KEY=secret",
    )

    assert result["success"] is False
    assert "sensitive" in result["error"].lower()


def test_edit_file_blocks_sensitive_file(
    tmp_path: Path,
) -> None:
    (tmp_path / ".env").write_text(
        "MODEL_API_KEY=secret",
        encoding="utf-8",
    )

    result = edit_file(
        workspace=tmp_path,
        path=".env",
        old_text="secret",
        new_text="changed",
    )

    assert result["success"] is False
    assert "sensitive" in result["error"].lower()


def test_search_text_skips_sensitive_file(
    tmp_path: Path,
) -> None:
    (tmp_path / ".env").write_text(
        "MODEL_API_KEY=secret",
        encoding="utf-8",
    )

    (tmp_path / "notes.txt").write_text(
        "secret",
        encoding="utf-8",
    )

    result = search_text(
        workspace=tmp_path,
        query="secret",
    )

    assert result["success"] is True
    assert result["count"] == 1
    assert result["matches"][0]["path"] == "notes.txt"
