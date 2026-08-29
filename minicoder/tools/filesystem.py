from pathlib import Path

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