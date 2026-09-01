from pathlib import Path

from minicoder.tools.shell import run_command


def test_run_command_success(
    tmp_path: Path,
) -> None:
    result = run_command(
        workspace=tmp_path,
        command=(
            'python -c "print(\'hello\')"'
        ),
    )

    assert result["success"] is True
    assert result["exit_code"] == 0
    assert "hello" in result["stdout"]
    assert result["timed_out"] is False


def test_run_command_nonzero_exit(
    tmp_path: Path,
) -> None:
    result = run_command(
        workspace=tmp_path,
        command=(
            'python -c '
            '"import sys; sys.exit(3)"'
        ),
    )

    assert result["success"] is False
    assert result["exit_code"] == 3
    assert result["timed_out"] is False


def test_run_command_truncates_output(
    tmp_path: Path,
) -> None:
    result = run_command(
        workspace=tmp_path,
        command=(
            'python -c '
            '"print(\'A\' * 30000)"'
        ),
    )

    assert result["success"] is True
    assert result["stdout_truncated"] is True
    assert (
        "...[output truncated]..."
        in result["stdout"]
    )


def test_run_command_timeout(
    tmp_path: Path,
) -> None:
    result = run_command(
        workspace=tmp_path,
        command=(
            'python -c '
            '"import time; '
            'time.sleep(2)"'
        ),
        timeout=1,
    )

    assert result["success"] is False
    assert result["exit_code"] is None
    assert result["timed_out"] is True