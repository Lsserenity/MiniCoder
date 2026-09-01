from pathlib import Path

path = Path(
    "demo_project/large.txt"
)

content = "\n".join(
    f"line {i}"
    for i in range(1, 10001)
)

path.write_text(
    content,
    encoding="utf-8",
)