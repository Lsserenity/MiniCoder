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

READ_FILE_TOOL = {
    "type": "function",
    "function": {
        "name": "read_file",
        "description": (
            "Read the contents of a text file inside the current project workspace. "
            "You may optionally specify a line range."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": (
                        "File path relative to the workspace root."
                    ),
                },
                "start_line": {
                    "type": "integer",
                    "description": (
                        "First line to read. "
                        "Line numbers start from 1."
                    ),
                },
                "end_line": {
                    "type": "integer",
                    "description": (
                        "Last line to read, inclusive."
                    ),
                },
            },
            "required": [
                "path",
            ],
            "additionalProperties": False,
        },
    },
}

WRITE_FILE_TOOL = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": (
            "Create a new UTF-8 text file inside "
            "the current project workspace. "
            "Existing files are not overwritten unless "
            "overwrite is explicitly set to true."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": (
                        "File path relative to "
                        "the workspace root."
                    ),
                },
                "content": {
                    "type": "string",
                    "description": (
                        "Complete text content "
                        "to write into the file."
                    ),
                },
                "overwrite": {
                    "type": "boolean",
                    "description": (
                        "Whether an existing file may "
                        "be overwritten. Defaults to false."
                    ),
                },
            },
            "required": [
                "path",
                "content",
            ],
            "additionalProperties": False,
        },
    },
}

TOOLS = [
    LIST_FILES_TOOL,
    READ_FILE_TOOL,
    WRITE_FILE_TOOL,
]