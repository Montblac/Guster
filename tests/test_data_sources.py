import tempfile
import unittest
from pathlib import Path

from guster.data_sources import TextListRepository


class TextListRepositoryTests(unittest.TestCase):
    def test_load_skips_comments_and_blanks(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            data_file = Path(temp_dir) / "values.txt"
            data_file.write_text("# comment\n\nalpha\n beta \n", encoding="utf-8")

            values = TextListRepository(data_file).load()

        self.assertEqual(values, ["alpha", "beta"])


if __name__ == "__main__":
    unittest.main()
