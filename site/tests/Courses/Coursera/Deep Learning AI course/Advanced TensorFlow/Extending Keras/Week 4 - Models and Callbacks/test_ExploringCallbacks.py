"""CSV head parity on synthetic logs only; no callback training occurs."""
import ast
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

import nbformat
import numpy as np
import pandas as pd
import polars as pl

SITE = next(parent for parent in Path(__file__).resolve().parents if parent.name == 'site')
sys.path.insert(0, str(SITE / 'scripts'))
from check_polars import cell_source, read_source, selected_expression

PATH = 'Courses/Coursera/Deep Learning AI course/Advanced TensorFlow/Extending Keras/Week 4 - Models and Callbacks/ExploringCallbacks.ipynb'
ORIGINAL_HASH = '7818e5532748749694eb976b94dad969682e28956e3305ed89d1aa102b0008b3'


class ExploringCallbacksTest(unittest.TestCase):
    def test_polars_read_head_contract_and_changed_cell_syntax(self):
        source = read_source(PATH)
        imports = cell_source(source, 3)
        self.assertIn('import polars as pl', imports)
        self.assertNotIn('import pandas', imports)
        self.assertEqual(cell_source(source, 24), 'pl.read_csv(csv_file).head()')
        # Only these known original Colab magics are excluded from syntax validation.
        imports = imports.replace(' %tensorflow_version 2.x', ' pass')
        imports = imports.replace('%load_ext tensorboard\n', '')
        ast.parse(imports)
        ast.parse(cell_source(source, 24))

    def test_synthetic_numeric_log_head_matches_original_with_missing_value(self):
        original = read_source(PATH, original=True)
        self.assertEqual(hashlib.sha256(original.encode()).hexdigest(), ORIGINAL_HASH)
        with tempfile.TemporaryDirectory() as directory:
            csv = Path(directory) / 'synthetic_training.csv'
            csv.write_text('epoch,accuracy,loss,val_accuracy,val_loss\n0,0.6,0.9,0.5,1.2\n1,0.7,0.8,0.6,1.1\n2,0.8,,0.7,1.0\n3,0.8,0.6,0.8,0.9\n4,0.9,0.5,0.9,0.8\n5,0.9,0.4,0.9,0.7\n')
            scope = {'pd': pd, 'pl': pl, 'csv_file': str(csv)}
            before = eval(selected_expression(cell_source(original, 24), 0), scope)
            after = eval(selected_expression(cell_source(read_source(PATH), 24), 0), scope)
        self.assertIsInstance(after, pl.DataFrame, 'CSV head still returns Pandas')
        self.assertEqual(after.columns, list(before.columns))
        self.assertEqual(after.height, 5)
        self.assertEqual(after.dtypes, [pl.Int64, pl.Float64, pl.Float64, pl.Float64, pl.Float64])
        np.testing.assert_allclose(after.to_numpy(), before.to_numpy(), equal_nan=True)
        np.testing.assert_array_equal(after.select(pl.all().is_null()).to_numpy(), before.isna().to_numpy())
        old, new = json.loads(original), json.loads(read_source(PATH))
        nbformat.validate(new)
        self.assertEqual(len(old['cells']), len(new['cells']))
        for i, (left, right) in enumerate(zip(old['cells'], new['cells'])):
            if i in (3, 24):
                self.assertEqual({k: v for k, v in left.items() if k != 'source'},
                                 {k: v for k, v in right.items() if k != 'source'})
            else:
                self.assertEqual(left, right, f'unapproved cell {i}')
        self.assertEqual({k: v for k, v in old.items() if k != 'cells'},
                         {k: v for k, v in new.items() if k != 'cells'})


if __name__ == '__main__':
    unittest.main()
