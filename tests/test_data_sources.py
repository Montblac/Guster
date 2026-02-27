import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from guster.data_sources import TextListRepository, WikimediaImageRepository


class TextListRepositoryTests(unittest.TestCase):
    def test_load_skips_comments_and_blanks(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            data_file = Path(temp_dir) / "values.txt"
            data_file.write_text("# comment\n\nalpha\n beta \n", encoding="utf-8")

            values = TextListRepository(data_file).load()

        self.assertEqual(values, ["alpha", "beta"])


class WikimediaImageRepositoryTests(unittest.TestCase):
    def test_load_filters_group_images_and_deduplicates_urls(self):
        payload = (
            b'{"query":{"pages":{"1":{"title":"File:Dule Hill portrait.jpg","imageinfo":[{"url":"https://a.jpg","mime":"image/jpeg","width":2400,"height":1600}]},'
            b'"2":{"title":"File:Psych cast at Comic-Con.jpg","imageinfo":[{"url":"https://blocked.jpg","mime":"image/jpeg","width":2600,"height":1700}]},'
            b'"3":{"title":"File:James Roday and Dule Hill.jpg","imageinfo":[{"url":"https://b.jpg","mime":"image/jpeg","width":2000,"height":1300}]},'
            b'"4":{"title":"File:Burton Guster still.jpg","imageinfo":[{"url":"https://a.jpg","mime":"image/jpeg","width":2600,"height":1700}]},'
            b'"5":{"title":"File:Dule Hill tiny.jpg","imageinfo":[{"url":"https://small.jpg","mime":"image/jpeg","width":640,"height":480}]}}}}'
        )

        class FakeResponse:
            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

            def read(self):
                return payload

        with patch("guster.data_sources.urlopen", return_value=FakeResponse()):
            urls = WikimediaImageRepository().load()

        self.assertEqual(urls, ["https://a.jpg", "https://b.jpg"])


if __name__ == "__main__":
    unittest.main()
