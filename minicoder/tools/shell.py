import locale
import subprocess
from pathlib import Path


# 这部分暂时保留，作为 run_command 自身的一层防御。
# 更上层还有 PolicyEngine。
BLOCKED_COMMANDS = [
    "rm -rf",
    "rm -fr",
    "rm -r ",
    "del /s",
    "del /f",
    "del /q",
    "erase /s",
    "format ",
    "rd /s",
    "rmdir /s",
    "remove-item -recurse",
    "remove-item -r",
    "remove-item -force",
    "shutdown",
    "reboot",
    "git reset --hard",
    "git clean -fd",
    "git clean -xdf",
]


MAX_OUTPUT_CHARS = 20_000


def decode_output(
    data: bytes | str | None,
) -> str:
    if data is None:
        return ""

    if isinstance(data, str):
        return data

    try:
        return data.decode(
            "utf-8"
        )
    except UnicodeDecodeError:
        system_encoding = (
            locale.getpreferredencoding(False)
        )

        try:
            return data.decode(
                system_encoding
            )
        except UnicodeDecodeError:
            return data.decode(
                "utf-8",
                errors="replace",
            )
        

def truncate_output(
    text: str,
    max_chars: int = MAX_OUTPUT_CHARS,
) -> tuple[str, bool]:
    """
    Limit tool output size to avoid flooding the LLM context.

    When output is too long, preserve both the beginning
    and the end of the output.
    """
    if not text:
        return "", False

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
    """
    在指定的工作目录中执行 shell 命令，并返回结果。
    """

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
            cwd=workspace,
            shell=True,
            capture_output=True,
            timeout=timeout,
        )

    except subprocess.TimeoutExpired as exc:
        stdout_text = decode_output(
            exc.stdout
        )

        stderr_text = decode_output(
            exc.stderr
        )

        stdout, stdout_truncated = truncate_output(
            stdout_text
        )

        stderr, stderr_truncated = truncate_output(
            stderr_text
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

    stdout_text = decode_output(
        completed.stdout
    )

    stderr_text = decode_output(
        completed.stderr
    )

    # Limit output size
    stdout, stdout_truncated = truncate_output(
        stdout_text
    )

    stderr, stderr_truncated = truncate_output(
        stderr_text
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
