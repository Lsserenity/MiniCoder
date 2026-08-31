import subprocess
from pathlib import Path


BLOCKED_COMMANDS = [
    "rm -rf",
    "del /s",
    "format ",
    "shutdown",
    "reboot",
]

MAX_OUTPUT_CHARS = 20_000

def truncate_output(
    text: str,
    max_chars: int = MAX_OUTPUT_CHARS,
) -> tuple[str, bool]:
    if len(text) <= max_chars:
        return text, False

    half = max_chars // 2

    truncated = (
        text[:half]
        + "\n...[output truncated]...\n"
        + text[-half:]
    )

    return truncated, True

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
        raw_stdout = exc.stdout or ""
        raw_stderr = exc.stderr or ""

        if isinstance(raw_stdout, bytes):
            raw_stdout = raw_stdout.decode(
                "utf-8",
                errors="replace",
            )

        if isinstance(raw_stderr, bytes):
            raw_stderr = raw_stderr.decode(
                "utf-8",
                errors="replace",
            )

        stdout, stdout_truncated = truncate_output(
            raw_stdout
        )

        stderr, stderr_truncated = truncate_output(
            raw_stderr
        )

        return {
            "success": False,
            "command": command,
            "exit_code": None,
            "stdout": stdout,
            "stderr": stderr,
            "stdout_truncated": stdout_truncated,
            "stderr_truncated": stderr_truncated,
            "timed_out": True,
        }

    except OSError as exc:
        return {
            "success": False,
            "error": str(exc),
        }

    stdout, stdout_truncated = truncate_output(
        completed.stdout
    )

    stderr, stderr_truncated = truncate_output(
        completed.stderr
    )

    return {
        "success": completed.returncode == 0,
        "command": command,
        "exit_code": completed.returncode,
        "stdout": stdout,
        "stderr": stderr,
        "stdout_truncated": stdout_truncated,
        "stderr_truncated": stderr_truncated,
        "timed_out": False,
    }