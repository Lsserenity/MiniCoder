import difflib

from pathlib import Path

MAX_READ_LINES = 1000

SENSITIVE_FILE_NAMES = {
    ".env",
}


def is_sensitive_path(
    path: Path,
) -> bool:
    return path.name.lower() in SENSITIVE_FILE_NAMES

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
    读取工作目录下的 UTF-8 文本文件。

    默认最多返回 MAX_READ_LINES 行。
    可以通过 start_line 和 end_line 指定读取范围。
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

    if is_sensitive_path(target):
        return {
            "success": False,
            "error": f"Access to sensitive file is denied: {path}",
        }

    if start_line < 1:
        return {
            "success": False,
            "error": "start_line must be at least 1.",
        }

    if (
        end_line is not None
        and end_line < start_line
    ):
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
    total_lines = len(lines)

    if total_lines == 0:
        return {
            "success": True,
            "path": path,
            "start_line": 1,
            "end_line": 0,
            "content": "",
            "total_lines": 0,
            "truncated": False,
        }

    if start_line > total_lines:
        return {
            "success": False,
            "error": (
                f"start_line {start_line} exceeds "
                f"file length {total_lines}."
            ),
        }

    max_end_line = (
        start_line + MAX_READ_LINES - 1
    )

    if end_line is None:
        actual_end_line = min(
            max_end_line,
            total_lines,
        )
    else:
        actual_end_line = min(
            end_line,
            max_end_line,
            total_lines,
        )

    selected_lines = lines[
        start_line - 1:actual_end_line
    ]

    numbered_lines = []

    for line_number, line in enumerate(
        selected_lines,
        start=start_line,
    ):
        numbered_lines.append(
            f"{line_number}: {line}"
        )

    content = "\n".join(
        numbered_lines
    )

    truncated = (
        actual_end_line < total_lines
    )

    return {
        "success": True,
        "path": path,
        "start_line": start_line,
        "end_line": actual_end_line,
        "content": content,
        "total_lines": total_lines,
        "truncated": truncated,
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

    if is_sensitive_path(target):
        return {
            "success": False,
            "error": f"Writing sensitive file is denied: {path}",
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

# 编辑文件
def edit_file(
    workspace: Path,
    path: str,
    old_text: str,
    new_text: str,
) -> dict:
    """
    在一个已经存在的utf-8编码的文件中替换只出现一次的old_text为new_text
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

    if is_sensitive_path(target):
        return {
            "success": False,
            "error": f"Editing sensitive file is denied: {path}",
        }

    try:
        original_text = target.read_text(
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

    match_count = original_text.count(
        old_text
    )

    if match_count == 0:
        return {
            "success": False,
            "error": (
                "old_text was not found in "
                f"the file: {path}"
            ),
        }

    if match_count > 1:
        return {
            "success": False,
            "error": (
                f"old_text matched multiple locations in the file: {path}. "
                "Please provide a more specific match."
            ),
        }

    updated_text = original_text.replace(
        old_text,
        new_text,
        1,
    )

    diff_lines = difflib.unified_diff(
        original_text.splitlines(),
        updated_text.splitlines(),
        fromfile=f"{path} (before)",
        tofile=f"{path} (after)",
        lineterm="",
    )

    diff = "\n".join(diff_lines)

    try:
        target.write_text(
            updated_text,
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
        "replacements": 1,
        "diff": diff,
    }
