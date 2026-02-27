import unittest
from unittest.mock import patch

from guster.web_app import GusterWebApp


class GusterWebAppTests(unittest.TestCase):
    def test_get_image_url_skips_previous_when_possible(self):
        app = GusterWebApp(image_urls=['https://example.com/a.jpg', 'https://example.com/b.jpg'])
        with patch('random.choice', side_effect=lambda seq: seq[0]):
            result = app.get_image_url(previous_image='https://example.com/a.jpg')
        self.assertEqual(result, 'https://example.com/b.jpg')

    def test_get_nickname_skips_previous_when_possible(self):
        app = GusterWebApp(image_urls=[], nicknames=['Shawn', 'Gus'])
        with patch('random.choice', side_effect=lambda seq: seq[0]):
            result = app.get_nickname(previous_nickname='Shawn')
        self.assertEqual(result, 'Gus')

    def test_get_image_url_with_history_avoids_recent_values(self):
        app = GusterWebApp(
            image_urls=[
                'https://example.com/a.jpg',
                'https://example.com/b.jpg',
                'https://example.com/c.jpg',
            ]
        )
        with patch('random.choice', side_effect=lambda seq: seq[0]):
            result = app.get_image_url_with_history(
                ['https://example.com/a.jpg', 'https://example.com/b.jpg']
            )
        self.assertEqual(result, 'https://example.com/c.jpg')

    def test_get_image_url_with_history_falls_back_when_all_recent(self):
        app = GusterWebApp(image_urls=['https://example.com/a.jpg'])
        with patch('random.choice', side_effect=lambda seq: seq[0]):
            result = app.get_image_url_with_history(['https://example.com/a.jpg'])
        self.assertEqual(result, 'https://example.com/a.jpg')


if __name__ == '__main__':
    unittest.main()
