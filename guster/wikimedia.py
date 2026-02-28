import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class WikimediaImageRepository:
    def __init__(
        self,
        search_queries: list[str] | None = None,
        limit: int = 48,
        query_limit: int = 50,
        min_width: int = 1200,
        min_height: int = 800,
        timeout_seconds: float = 5.0,
    ):
        self.search_queries = search_queries or [
            '"Dule Hill" portrait',
            '"Dule Hill" Psych',
            '"Dule Hill" "James Roday"',
            '"Burton Guster" Psych',
        ]
        self.limit = limit
        self.query_limit = query_limit
        self.min_width = min_width
        self.min_height = min_height
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

    @staticmethod
    def _score_title(page_title: str) -> int:
        title = page_title.lower()
        score = 0
        if "dule hill" in title:
            score += 5
        if "burton guster" in title or "gus" in title or "guster" in title:
            score += 4
        if "james roday" in title or "shawn" in title:
            score += 2
        if "psych" in title:
            score += 2
        if "portrait" in title or "headshot" in title or "still" in title:
            score += 2
        return score

    def _is_high_quality(self, image_info: dict) -> bool:
        mime = str(image_info.get("mime", "")).lower()
        width = int(image_info.get("width", 0))
        height = int(image_info.get("height", 0))
        allowed_mime = {"image/jpeg", "image/jpg", "image/png", "image/webp"}
        return mime in allowed_mime and width >= self.min_width and height >= self.min_height

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
        url = f"https://commons.wikimedia.org/w/api.php?{urlencode(params)}"
        request = Request(url, headers={"User-Agent": "GusterApp/1.0"})

        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except Exception:
            return []

        pages = payload.get("query", {}).get("pages", {})
        results: list[tuple[int, str]] = []
        for page in pages.values():
            page_title = page.get("title", "")
            info = page.get("imageinfo", [])
            if not info:
                continue
            image_info = info[0]
            if not self._is_preferred_subject(page_title):
                continue
            if not self._is_high_quality(image_info):
                continue

            image_url = image_info.get("url")
            if image_url:
                score = self._score_title(page_title) + min(int(image_info.get("width", 0)) // 800, 5)
                results.append((score, image_url))
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
        scored_urls: list[tuple[int, str]] = []
        for query in self.search_queries:
            scored_urls.extend(self._fetch_query(query))

        for _, image_url in sorted(scored_urls, key=lambda entry: entry[0], reverse=True):
            if image_url in seen:
                continue
            seen.add(image_url)
            urls.append(image_url)
            if len(urls) >= self.limit:
                break
        return urls
