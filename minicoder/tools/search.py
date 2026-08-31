from pathlib import Path

from minicoder.tools.filesystem import resolve_workspace_path


DEFAULT_IGNORED_DIRS = {
    ".git",
    "__pycache__",
    ".idea",
    ".vscode",
    "node_modules",
    "venv",
    ".venv",
    ".pytest_cache",
}


def search_text(
    workspace: Path,
    query: str,
    path: str = ".",
    max_results: int = 50,
) -> dict:
    """
    递归搜索工作目录下的utf-8的文件中的文本
    """

    if query == "":
        return {
            "success": False,
            "error": "query must not be empty.",
        }

    if max_results < 1:
        return {
            "success": False,
            "error": "max_results must be at least 1.",
        }

    try:
        target = resolve_workspace_path(
            workspace,
            path,
        )
    except PermissionError as exc:
        return {
            "success": False,
            "error": str(exc),
        }

    if not target.exists():
        return {
            "success": False,
            "error": f"Path does not exist: {path}",
        }

    matches = []

    if target.is_file():
        files = [target]
    else:
        files = target.rglob("*")

    for file_path in files:
        if len(matches) >= max_results:
            break

        if not file_path.is_file():
            continue

        relative_parts = file_path.relative_to(
            workspace
        ).parts

        if any(
            part in DEFAULT_IGNORED_DIRS
            for part in relative_parts
        ):
            continue

        try:
            text = file_path.read_text(
                encoding="utf-8"
            )
        except (UnicodeDecodeError, OSError):
            continue

        for line_number, line in enumerate(
            text.splitlines(),
            start=1,
        ):
            if query in line:
                matches.append(
                    {
                        "path": str(
                            file_path.relative_to(
                                workspace
                            )
                        ),
                        "line": line_number,
                        "text": line,
                    }
                )

                if len(matches) >= max_results:
                    break

    return {
        "success": True,
        "query": query,
        "path": path,
        "matches": matches,
        "count": len(matches),
        "truncated": (
            len(matches) >= max_results
        ),
    }