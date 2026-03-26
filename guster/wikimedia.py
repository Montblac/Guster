import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen

_REQUIRED_TERMS = ("dule", "hill", "gus", "guster", "shawn", "james", "roday", "psych")
_BLOCKED_TERMS = (
    "comic-con",
    "comic con",
    "panel",
    "cast",
    "group",
    "reunion",
    "press line",
    "red carpet",
)


def _is_preferred_subject(title: str) -> bool:
    lower = title.lower()
    return any(t in lower for t in _REQUIRED_TERMS) and not any(t in lower for t in _BLOCKED_TERMS)


def _score_title(title: str) -> int:
    lower = title.lower()
    score = 0
    if "dule hill" in lower:
        score += 5
    if "burton guster" in lower or "gus" in lower or "guster" in lower:
        score += 4
    if "james roday" in lower or "shawn" in lower:
        score += 2
    if "psych" in lower:
        score += 2
    if "portrait" in lower or "headshot" in lower or "still" in lower:
        score += 2
    return score


class WikimediaImageRepository:
    _API_URL = "https://commons.wikimedia.org/w/api.php"
    _DEFAULT_QUERIES = [
        '"Dule Hill" portrait',
        '"Dule Hill" Psych',
        '"Dule Hill" "James Roday"',
        '"Burton Guster" Psych',
    ]
    _ALLOWED_MIME = {"image/jpeg", "image/jpg", "image/png", "image/webp"}

    def __init__(
        self,
        search_queries: list[str] | None = None,
        limit: int = 48,
        query_limit: int = 50,
        min_width: int = 1200,
        min_height: int = 800,
        timeout_seconds: float = 5.0,
    ):
        self.search_queries = search_queries or self._DEFAULT_QUERIES
        self.limit = limit
        self.query_limit = query_limit
        self.min_width = min_width
        self.min_height = min_height
        self.timeout_seconds = timeout_seconds

    def _is_high_quality(self, image_info: dict) -> bool:
        mime = str(image_info.get("mime", "")).lower()
        width = int(image_info.get("width", 0))
        height = int(image_info.get("height", 0))
        return mime in self._ALLOWED_MIME and width >= self.min_width and height >= self.min_height

    def _fetch_query(self, query: str) -> list[tuple[int, str]]:
        params = {
            "action": "query",
            "format": "json",
            "generator": "search",
            "gsrnamespace": "6",
            "gsrsearch": query,
            "gsrlimit": str(self.query_limit),
            "prop": "imageinfo",
            "iiprop": "url|size|mime",
            "origin": "*",
        }
        request = Request(
            f"{self._API_URL}?{urlencode(params)}",
            headers={"User-Agent": "GusterApp/1.0"},
        )
        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except Exception:
            return []

        results: list[tuple[int, str]] = []
        for page in payload.get("query", {}).get("pages", {}).values():
            title = page.get("title", "")
            info = page.get("imageinfo", [])
            if not info or not _is_preferred_subject(title):
                continue
            image_info = info[0]
            if not self._is_high_quality(image_info):
                continue
            url = image_info.get("url")
            if url:
                score = _score_title(title) + min(int(image_info.get("width", 0)) // 800, 5)
                results.append((score, url))
        return results

    def load(self) -> list[str]:
        scored: list[tuple[int, str]] = []
        for query in self.search_queries:
            scored.extend(self._fetch_query(query))

        seen: set[str] = set()
        urls: list[str] = []
        for _, url in sorted(scored, key=lambda e: e[0], reverse=True):
            if url not in seen:
                seen.add(url)
                urls.append(url)
            if len(urls) >= self.limit:
                break
        return urls
