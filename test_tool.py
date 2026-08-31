from pathlib import Path

from minicoder.tools.shell import run_command


def main():
    workspace = Path(
        "demo_project"
    ).resolve()

    result = run_command(
        workspace=workspace,
        command='python -c "import time; time.sleep(5)"',
        timeout=1
    )

    print(
        "success:",
        result["success"],
    )

    print(
        "stderr length:",
        len(result["stderr"]),
    )

    print(
        "stderr truncated:",
        result["stderr_truncated"],
    )

    print(
        "contains marker:",
        "[output truncated]" in result["stderr"],
    )

    print(
        "timed out:",
        result["timed_out"],
    )


if __name__ == "__main__":
    main()