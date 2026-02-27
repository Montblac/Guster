import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen


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


class WikimediaImageRepository:
    def __init__(
        self,
        search_queries: list[str] | None = None,
        limit: int = 24,
        thumb_width: int = 1920,
        timeout_seconds: float = 5.0,
    ):
        self.search_queries = search_queries or [
            '"Dule Hill" Psych',
            '"Dule Hill" "James Roday" Psych',
            '"Burton Guster" Psych',
        ]
        self.limit = limit
        self.thumb_width = thumb_width
        self.timeout_seconds = timeout_seconds

    @staticmethod
    def _is_preferred_subject(page_title: str) -> bool:
        title = page_title.lower()
        required_terms = ("dule", "hill", "gus", "guster", "shawn", "james", "roday", "psych")
        blocked_terms = (
            "comic-con",
            "comic con",
            "panel",
            "cast",
            "group",
            "reunion",
            "press line",
            "red carpet",
        )
        has_subject = any(term in title for term in required_terms)
        is_blocked = any(term in title for term in blocked_terms)
        return has_subject and not is_blocked

    def _fetch_query(self, query: str) -> list[tuple[str, str]]:
        params = {
            "action": "query",
            "format": "json",
            "generator": "search",
            "gsrnamespace": "6",
            "gsrsearch": query,
            "gsrlimit": str(self.limit),
            "prop": "imageinfo",
            "iiprop": "url",
            "iiurlwidth": str(self.thumb_width),
            "origin": "*",
        }
        url = f"https://commons.wikimedia.org/w/api.php?{urlencode(params)}"
        request = Request(url, headers={"User-Agent": "GusterApp/1.0"})

        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except Exception:
            return []

        pages = payload.get("query", {}).get("pages", {})
        results: list[tuple[str, str]] = []
        for page in pages.values():
            page_title = page.get("title", "")
            info = page.get("imageinfo", [])
            if not info:
                continue
            image_url = info[0].get("url") or info[0].get("thumburl")
            if image_url:
                results.append((page_title, image_url))
        return results

    def load(self) -> list[str]:
        """
        Fetches high-resolution image URLs from Wikimedia Commons.
        Prioritizes images focused on Gus or Gus+Shawn and filters out
        Comic-Con/group-panel style results.
        Returns an empty list if requests fail.
        """
        urls: list[str] = []
        seen: set[str] = set()
        for query in self.search_queries:
            for page_title, image_url in self._fetch_query(query):
                if not self._is_preferred_subject(page_title):
                    continue
                if image_url in seen:
                    continue
                seen.add(image_url)
                urls.append(image_url)

            if len(urls) >= self.limit:
                break
        return urls
