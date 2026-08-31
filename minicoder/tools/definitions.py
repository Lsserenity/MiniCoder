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

EDIT_FILE_TOOL = {
    "type": "function",
    "function": {
        "name": "edit_file",
        "description": (
            "Modify an existing UTF-8 text file by replacing "
            "exactly one occurrence of old_text with new_text. "
            "The old_text must match exactly one location."
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
                "old_text": {
                    "type": "string",
                    "description": (
                        "Exact existing text to replace. "
                        "It must occur exactly once in the file."
                    ),
                },
                "new_text": {
                    "type": "string",
                    "description": (
                        "Replacement text. "
                        "Use an empty string to delete old_text."
                    ),
                },
            },
            "required": [
                "path",
                "old_text",
                "new_text",
            ],
            "additionalProperties": False,
        },
    },
}

SEARCH_TEXT_TOOL = {
    "type": "function",
    "function": {
        "name": "search_text",
        "description": (
            "Search recursively for exact text inside UTF-8 files "
            "within the current project workspace. "
            "Returns matching file paths, line numbers, and lines."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": (
                        "Exact text to search for."
                    ),
                },
                "path": {
                    "type": "string",
                    "description": (
                        "File or directory path relative to "
                        "the workspace root. "
                        "Defaults to '.'."
                    ),
                },
                "max_results": {
                    "type": "integer",
                    "description": (
                        "Maximum number of matches to return. "
                        "Defaults to 50."
                    ),
                },
            },
            "required": [
                "query",
            ],
            "additionalProperties": False,
        },
    },
}

RUN_COMMAND_TOOL = {
    "type": "function",
    "function": {
        "name": "run_command",
        "description": (
            "Run a shell command inside the current project workspace. "
            "Use this to execute programs, run tests, or inspect command output."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": (
                        "Shell command to execute inside "
                        "the workspace."
                    ),
                },
                "timeout": {
                    "type": "integer",
                    "description": (
                        "Maximum execution time in seconds. "
                        "Defaults to 30."
                    ),
                },
            },
            "required": [
                "command",
            ],
            "additionalProperties": False,
        },
    },
}

TOOLS = [
    LIST_FILES_TOOL,
    READ_FILE_TOOL,
    WRITE_FILE_TOOL,
    EDIT_FILE_TOOL,
    SEARCH_TEXT_TOOL,
    RUN_COMMAND_TOOL,
]