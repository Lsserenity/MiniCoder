import subprocess
from pathlib import Path


BLOCKED_COMMANDS = [
    "rm -rf",
    "del /s",
    "format ",
    "shutdown",
    "reboot",
]


def run_command(
    workspace: Path,
    command: str,
    timeout: int = 30,
) -> dict:
    if command.strip() == "":
        return {
            "success": False,
            "error": "command must not be empty.",
        }

    if timeout < 1:
        return {
            "success": False,
            "error": "timeout must be at least 1 second.",
        }

    normalized_command = command.lower()

    for blocked in BLOCKED_COMMANDS:
        if blocked in normalized_command:
            return {
                "success": False,
                "error": (
                    f"Command is blocked for safety: {command}"
                ),
            }

    try:
        completed = subprocess.run(
            command,
            cwd=workspace,      # current working directory
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        return {
            "success": False,
            "command": command,
            "exit_code": None,
            "stdout": exc.stdout or "",
            "stderr": exc.stderr or "",
            "timed_out": True,
        }
    except OSError as exc:
        return {
            "success": False,
            "error": str(exc),
        }

    return {
        "success": completed.returncode == 0,
        "command": command,
        "exit_code": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "timed_out": False,
    }