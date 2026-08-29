LIST_FILES_TOOL = {
    "type": "function",
    "function": {
        "name": "list_files",
        "description": "List files and directories inside the current project workspace.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": (
                        "Directory path relative to the workspace root. "
                        "Use '.' for the root directory."
                    ),
                }
            },
            "required": ["path"],
            "additionalProperties": False,
        },
    },
}


TOOLS = [
    LIST_FILES_TOOL,
]