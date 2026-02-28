import unittest
from unittest.mock import patch

from guster.app import GusterApp


class GusterAppTests(unittest.TestCase):
    def test_pick_nickname_skips_previous(self):
        app = GusterApp(nicknames=["Shawn", "Gus"])
        with patch("random.choice", side_effect=lambda seq: seq[0]):
            self.assertEqual(app.pick_nickname(previous="Shawn"), "Gus")

    def test_pick_nickname_returns_none_when_empty(self):
        self.assertIsNone(GusterApp().pick_nickname())

    def test_pick_image_avoids_recent(self):
        app = GusterApp(image_urls=["https://a.jpg", "https://b.jpg", "https://c.jpg"])
        with patch("random.choice", side_effect=lambda seq: seq[0]):
            result = app.pick_image(["https://a.jpg", "https://b.jpg"])
        self.assertEqual(result, "https://c.jpg")

    def test_pick_image_falls_back_when_all_recent(self):
        app = GusterApp(image_urls=["https://a.jpg"])
        with patch("random.choice", side_effect=lambda seq: seq[0]):
            self.assertEqual(app.pick_image(["https://a.jpg"]), "https://a.jpg")

    def test_pick_image_returns_none_when_empty(self):
        self.assertIsNone(GusterApp().pick_image([]))

    def test_update_recent_appends_and_caps(self):
        app = GusterApp(max_recent=3)
        result = app.update_recent(["a", "b", "c"], "d")
        self.assertEqual(result, ["b", "c", "d"])

    def test_update_recent_deduplicates_current(self):
        app = GusterApp()
        result = app.update_recent(["a", "b"], "b")
        self.assertEqual(result, ["a", "b"])


if __name__ == "__main__":
    unittest.main()
