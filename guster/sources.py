from pathlib import Path


def load_text_file(path: str | Path) -> list[str]:
    path = Path(path)
    if not path.exists():
        return []
    lines = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                lines.append(stripped)
    return lines
