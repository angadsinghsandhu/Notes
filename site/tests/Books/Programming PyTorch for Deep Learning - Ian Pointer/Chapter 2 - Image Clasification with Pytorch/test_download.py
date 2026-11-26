"""All real image-list rows; never import or call the downloader."""
import ast
import hashlib
import os
from pathlib import Path
import sys
import unittest

import pandas as pd
import polars as pl

SITE = next(parent for parent in Path(__file__).resolve().parents if parent.name == 'site')
sys.path.insert(0, str(SITE / 'scripts'))
from check_polars import ROOT, read_source

PATH = 'Books/Programming PyTorch for Deep Learning - Ian Pointer/Chapter 2 - Image Clasification with Pytorch/download.py'
ORIGINAL_HASH = 'ebe16af39a112e7e5d36cb9e617aa1f07af8a868a9043e1fd7dec151e7b55d3f'
INPUT_HASH = 'dd829fdcf45906fbe4fe6648918361d7139c61420e2339419fb1bc9b3cfc246e'


def read_and_rows(source):
    tree = ast.parse(source)
    main = tree.body[12]
    assert isinstance(main, ast.If)
    assert isinstance(main.body[1], ast.Assign)
    assert main.body[1].targets[0].id == 'imagesDF'
    scope = {'pd': pd, 'pl': pl}
    cwd = Path.cwd()
    try:
        os.chdir((ROOT / PATH).parent)
        exec(compile(ast.Module(body=[main.body[1]], type_ignores=[]), '<CSV read only>', 'exec'), scope)
    finally:
        os.chdir(cwd)
    comprehension = main.body[4].value
    assert isinstance(comprehension, ast.ListComp)
    # Evaluate only the iterator, excluding download_image and every main side effect.
    rows = eval(compile(ast.Expression(comprehension.generators[0].iter), '<ordered rows only>', 'eval'), scope)
    return scope['imagesDF'], list(rows)


class DownloadTest(unittest.TestCase):
    def test_polars_source_contract(self):
        source = read_source(PATH)
        self.assertIn('import polars as pl', source)
        self.assertNotIn('import pandas', source)
        self.assertIn('.select("url", "class", "type").iter_rows()', source)

    def test_real_all_rows_match_exact_original_order_and_string_columns(self):
        original = read_source(PATH, original=True)
        self.assertEqual(hashlib.sha256(original.encode()).hexdigest(), ORIGINAL_HASH)
        data = (ROOT / PATH).parent / 'images.csv'
        self.assertEqual(hashlib.sha256(data.read_bytes()).hexdigest(), INPUT_HASH)
        before, expected = read_and_rows(original)
        after, actual = read_and_rows(read_source(PATH))
        self.assertEqual(actual, expected)
        self.assertIsInstance(after, pl.DataFrame, "CSV read still returns Pandas")
        self.assertEqual(list(before.columns), after.columns)
        self.assertEqual(after.columns, ['url', 'class', 'type'])
        self.assertEqual(len(actual), 1393)
        self.assertEqual(actual, expected)
        self.assertTrue(all(dtype == pl.String for dtype in after.dtypes))
        self.assertEqual(after.null_count().row(0), (0, 0, 0))
        self.assertFalse(before.isna().to_numpy().any())
        old_tree, new_tree = ast.parse(original), ast.parse(read_source(PATH))
        self.assertEqual(ast.get_source_segment(original, old_tree.body[11]),
                         ast.get_source_segment(read_source(PATH), new_tree.body[11]))


if __name__ == '__main__':
    unittest.main()
