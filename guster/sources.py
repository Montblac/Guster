from pathlib import Path


class TextListRepository:
    def __init__(self, source_path: str | Path):
        self.source_path = Path(source_path)

    def load(self) -> list[str]:
        if not self.source_path.exists():
            return []

        values: list[str] = []
        with self.source_path.open(encoding="utf-8") as handle:
            for line in handle:
                value = line.strip()
                if value and not value.startswith("#"):
                    values.append(value)
        return values


class ImageUrlRepository(TextListRepository):
    pass


class NicknameRepository(TextListRepository):
    pass
