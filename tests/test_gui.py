import unittest
from unittest.mock import patch

import gui


class WebAppTests(unittest.TestCase):
    def test_get_image_name_skips_previous_when_possible(self):
        app = gui.WebApp(images=['https://example.com/a.jpg', 'https://example.com/b.jpg'])
        with patch('random.choice', side_effect=lambda seq: seq[0]):
            result = app.get_image_name(previous_image='https://example.com/a.jpg')
        self.assertEqual(result, 'https://example.com/b.jpg')

    def test_get_nickname_skips_previous_when_possible(self):
        app = gui.WebApp(images=[], nicknames=['Shawn', 'Gus'])
        with patch('random.choice', side_effect=lambda seq: seq[0]):
            result = app.get_nickname(previous_nickname='Shawn')
        self.assertEqual(result, 'Gus')


if __name__ == '__main__':
    unittest.main()
