"""Unused import removal only; preserve the unfinished course exercise."""
import ast
import hashlib
from pathlib import Path
import sys
import unittest

SITE = next(parent for parent in Path(__file__).resolve().parents if parent.name == 'site')
sys.path.insert(0, str(SITE / 'scripts'))
from check_polars import read_source

PATH = 'Courses/Coursera/tf deployment/Course 3/Week 2/2_input_pipelines_custom.py'
ORIGINAL_HASH = '6452c5c77ec62a9dd50b85dff342ce72e5d96908aca1f338341220a6e621c029'


class CustomInputTest(unittest.TestCase):
    def test_unused_pandas_import_is_removed_without_replacement(self):
        source = read_source(PATH)
        imports = [alias.name for node in ast.parse(source).body if isinstance(node, ast.Import)
                   for alias in node.names]
        self.assertNotIn('pandas', imports)
        self.assertNotIn('polars', imports)

    def test_every_other_byte_including_todo_and_upstream_link_is_preserved(self):
        original = read_source(PATH, original=True)
        self.assertEqual(hashlib.sha256(original.encode()).hexdigest(), ORIGINAL_HASH)
        self.assertEqual(read_source(PATH), original.replace('import pandas as pd\n', '', 1))
        ast.parse(read_source(PATH))


if __name__ == '__main__':
    unittest.main()
