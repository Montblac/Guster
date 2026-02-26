import unittest
from unittest.mock import patch

import gui


class WebAppTests(unittest.TestCase):
    def test_get_image_name_skips_previous_when_possible(self):
        app = gui.WebApp(images=['/tmp/a.jpg', '/tmp/b.jpg'])
        with patch('random.choice', side_effect=lambda seq: seq[0]):
            result = app.get_image_name(previous_image='a.jpg')
        self.assertEqual(result, 'b.jpg')

    def test_resolve_image_path_blocks_path_traversal(self):
        app = gui.WebApp(images=[])
        blocked = app.resolve_image_path('../etc/passwd')
        self.assertIsNone(blocked)


if __name__ == '__main__':
    unittest.main()
