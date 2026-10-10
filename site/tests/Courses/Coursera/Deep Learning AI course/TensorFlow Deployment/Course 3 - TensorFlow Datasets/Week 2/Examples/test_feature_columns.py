"""Real heart candidate and prescribed row splits; no TensorFlow/sklearn execution."""
import ast
import hashlib
import json
from pathlib import Path
import sys
import unittest

import nbformat
import numpy as np
import pandas as pd
import polars as pl

SITE = next(parent for parent in Path(__file__).resolve().parents if parent.name == 'site')
sys.path.insert(0, str(SITE / 'scripts'))
from check_polars import cell_source, read_source, selected_code
from polars_tf_support import (assert_arrays, assert_dataset_boundaries,
                               assert_prescribed_splits, recording_tf)

PATH = 'Courses/Coursera/Deep Learning AI course/TensorFlow Deployment/Course 3 - TensorFlow Datasets/Week 2/Examples/feature_columns.ipynb'
ORIGINAL_HASH = 'edbf00fb9c4e94af7409d0b1a9787d75f0245385beb9d80f44fa628a94245398'
HEART = SITE / 'tests/fixtures/real/polars/heart.csv'
HEART_HASH = 'a91c81831bb2126e5fde6ce4ebde147a78429da12005108a6677ba57ecde9244'


class FeatureColumnsTest(unittest.TestCase):
    def test_polars_contract_syntax_and_exact_notebook_preservation(self):
        source, original = read_source(PATH), read_source(PATH, original=True)
        self.assertEqual(hashlib.sha256(original.encode()).hexdigest(), ORIGINAL_HASH)
        self.assertIn('import polars as pl', cell_source(source, 7))
        self.assertNotIn('import pandas', cell_source(source, 7))
        for i in (4, 8, 12):
            self.assertIn('Polars', cell_source(source, i))
        self.assertIn('historical', cell_source(source, 8))
        self.assertIn('download.tensorflow.org/data/heart.csv', cell_source(source, 9))
        for i in (7, 9, 11, 13):
            ast.parse(cell_source(source, i).replace('  %tensorflow_version 2.x', '  pass'))
        old, new = json.loads(original), json.loads(source)
        nbformat.validate(new)
        self.assertEqual(len(old['cells']), len(new['cells']))
        for i, (before, after) in enumerate(zip(old['cells'], new['cells'])):
            if i in (4, 7, 8, 9, 11, 12, 13):
                self.assertEqual({k: v for k, v in before.items() if k != 'source'},
                                 {k: v for k, v in after.items() if k != 'source'})
            else:
                self.assertEqual(before, after, f'unapproved cell {i}')
        self.assertEqual({k: v for k, v in old.items() if k != 'cells'},
                         {k: v for k, v in new.items() if k != 'cells'})

    def load_frames(self):
        self.assertEqual(hashlib.sha256(HEART.read_bytes()).hexdigest(), HEART_HASH)
        provenance = json.loads((HEART.parent / 'provenance.json').read_text())['inputs'][0]
        self.assertEqual(provenance['sha256'], HEART_HASH)
        self.assertEqual(provenance['historical_equality'], 'unknown')
        frames = []
        for notebook in (read_source(PATH, original=True), read_source(PATH)):
            scope = {'pd': pd, 'pl': pl, 'URL': str(HEART)}
            exec(selected_code(cell_source(notebook, 9), [1]), scope)
            frames.append(scope['dataframe'])
        self.assertIsInstance(frames[1], pl.DataFrame, 'heart read still returns Pandas')
        self.assertEqual(frames[1].shape, (303, 14))
        self.assertEqual(frames[1].columns, list(frames[0].columns))
        self.assertEqual(frames[1]['oldpeak'].dtype, pl.Float64)
        self.assertEqual(frames[1]['thal'].dtype, pl.String)
        return frames

    def test_full_real_heart_ingestion_and_prescribed_random_split_rows(self):
        before, after = self.load_frames()
        for name in before.columns:
            assert_arrays(self, before[name].to_numpy(), after[name].to_numpy())
        codes = [cell_source(read_source(PATH, original=original), 11)
                 for original in (True, False)]
        assert_prescribed_splits(self, codes, (before, after))

    def test_recorded_feature_label_arrays_and_shuffle_batch_without_mutation(self):
        before, after = self.load_frames()
        cases = [(before, after), (before.iloc[[4, 1, 2]], after[[4, 1, 2]]),
                 (before.iloc[:0], after[:0])]
        # Explicit synthetic edge, independent of the real fixture's zero missing values.
        synthetic_before = before.iloc[:3].copy()
        synthetic_before.loc[0, 'oldpeak'] = np.nan
        synthetic_after = after[:3].with_columns(
            pl.Series('oldpeak', [None, after['oldpeak'][1], after['oldpeak'][2]], dtype=pl.Float64))
        cases.append((synthetic_before, synthetic_after))
        functions = []
        for original in (True, False):
            scope = {'tf': recording_tf()}
            exec(cell_source(read_source(PATH, original=original), 13), scope)
            functions.append(scope['df_to_dataset'])
        assert_dataset_boundaries(self, functions, cases, pd.testing.assert_frame_equal)


if __name__ == '__main__':
    unittest.main()
