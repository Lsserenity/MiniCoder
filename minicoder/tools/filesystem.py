from pathlib import Path

# 解析工作目录下的文件路径，保证不会越界
def resolve_workspace_path(
    workspace: Path,
    path: str,
) -> Path:
    '''
    解析文件路径，保证路径不会超过当前工作目录
    '''
    workspace = workspace.resolve()
    target = (workspace / path).resolve()

    try:
        target.relative_to(workspace)
    except ValueError:
        raise PermissionError(
            f"Access to {target} is denied. It is outside the workspace {workspace}."
        )

    return target

# 列出当前工作目录下的所有文件和文件夹
def list_files(
        workspace: Path,
        path: str = '.',
) -> dict:
    """
    列出当前工作目录下的所有文件和文件夹
    单层遍历，不会递归
    """
    try:
        target = resolve_workspace_path(workspace, path)
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
    if not target.is_dir():
        return {
            "success": False,
            "error": f"Path is not a directory: {path}",
        }

    entries = []
    for item in sorted(
        target.iterdir(),
        key=lambda x: (not x.is_dir(), x.name.lower())
    ):
        entries.append(
            {
                "name": item.name,
                "type": ("directory" if item.is_dir() else "file"),
            }
        )

    return {
        "success": True,
        "path": path,
        "entries": entries
    }

# 读文件
def read_file(
    workspace: Path,
    path: str,
    start_line: int = 1,
    end_line: int | None = None,
) -> dict:
    """
    读取工作目录下的文件内容
    可选返回指定行的内容
    """
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
            "error": f"File does not exist: {path}",
        }

    if not target.is_file():
        return {
            "success": False,
            "error": f"Path is not a file: {path}",
        }

    if start_line < 1:
        return {
            "success": False,
            "error": "start_line must be at least 1.",
        }

    if end_line is not None and end_line < start_line:
        return {
            "success": False,
            "error": (
                "end_line must be greater than "
                "or equal to start_line."
            ),
        }

    try:
        text = target.read_text(
            encoding="utf-8"
        )
    except UnicodeDecodeError:
        return {
            "success": False,
            "error": (
                f"File is not valid UTF-8 text: {path}"
            ),
        }
    except OSError as exc:
        return {
            "success": False,
            "error": str(exc),
        }

    lines = text.splitlines()

    start_index = start_line - 1

    if end_line is None:
        selected_lines = lines[start_index:]
    else:
        selected_lines = lines[
            start_index:end_line
        ]

    numbered_lines = []

    for index, line in enumerate(
        selected_lines,
        start=start_line,
    ):
        numbered_lines.append(
            f"{index}: {line}"
        )

    return {
        "success": True,
        "path": path,
        "start_line": start_line,
        "end_line": (
            start_line + len(selected_lines) - 1
            if selected_lines
            else start_line
        ),
        "content": "\n".join(numbered_lines),
        "total_lines": len(lines),
    }

# 写文件
def write_file(
    workspace: Path,
    path: str,
    content: str,
    overwrite: bool = False,
) -> dict:
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

    existed_before = target.exists()

    if existed_before and not overwrite:
        return {
            "success": False,
            "error": (
                f"File already exists: {path}. "
                "Set overwrite=true to replace it."
            ),
        }

    if existed_before and not target.is_file():
        return {
            "success": False,
            "error": f"Path is not a file: {path}",
        }

    try:
        target.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        target.write_text(
            content,
            encoding="utf-8",
        )

    except OSError as exc:
        return {
            "success": False,
            "error": str(exc),
        }

    return {
        "success": True,
        "path": path,
        "bytes_written": len(
            content.encode("utf-8")
        ),
        "overwritten": existed_before,
    }