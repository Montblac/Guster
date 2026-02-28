import random
from dataclasses import dataclass, field


def _pick_different(options: list[str], exclude: str | None) -> str | None:
    if not options:
        return None
    candidates = [v for v in options if v != exclude] or options
    return random.choice(candidates)


@dataclass
class GusterApp:
    image_urls: list[str] = field(default_factory=list)
    nicknames: list[str] = field(default_factory=list)
    max_recent: int = 10

    def pick_nickname(self, previous: str | None = None) -> str | None:
        return _pick_different(self.nicknames, previous)

    def pick_image(self, recent: list[str]) -> str | None:
        if not self.image_urls:
            return None
        recent_set = set(recent)
        candidates = [u for u in self.image_urls if u not in recent_set] or self.image_urls
        return random.choice(candidates)

    def update_recent(self, recent: list[str], current: str | None) -> list[str]:
        updated = [v for v in recent if v != current]
        if current:
            updated.append(current)
        return updated[-self.max_recent:]
