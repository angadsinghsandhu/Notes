"""Real heart parity with exercise completion only in test memory; TODOs preserved."""
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

PATH = 'Courses/Coursera/Deep Learning AI course/TensorFlow Deployment/Course 3 - TensorFlow Datasets/Week 2/Exercises/TFDS_Week2_Exercise.ipynb'
ORIGINAL_HASH = 'c8aec3216c90f25926d1ba450bd6acd36f5633824e112ff4d81a61625cea2547'
HEART = SITE / 'tests/fixtures/real/polars/heart.csv'
HEART_HASH = 'a91c81831bb2126e5fde6ce4ebde147a78429da12005108a6677ba57ecde9244'


class TFDSWeek2ExerciseTest(unittest.TestCase):
    def test_polars_contract_syntax_and_exact_notebook_preservation(self):
        source, original = read_source(PATH), read_source(PATH, original=True)
        self.assertEqual(hashlib.sha256(original.encode()).hexdigest(), ORIGINAL_HASH)
        self.assertIn('import polars as pl', cell_source(source, 5))
        self.assertNotIn('import pandas', cell_source(source, 5))
        for i in (6, 10):
            self.assertIn('Polars', cell_source(source, i))
        self.assertIn('historical', cell_source(source, 6))
        self.assertIn('download.tensorflow.org/data/heart.csv', cell_source(source, 7))
        for i in (5, 7, 9):
            ast.parse(cell_source(source, i).replace('  %tensorflow_version 2.x', '  pass'))
        old, new = json.loads(original), json.loads(source)
        nbformat.validate(new)
        self.assertEqual(len(old['cells']), len(new['cells']))
        for i, (before, after) in enumerate(zip(old['cells'], new['cells'])):
            if i in (5, 6, 7, 9, 10, 11):
                self.assertEqual({k: v for k, v in before.items() if k != 'source'},
                                 {k: v for k, v in after.items() if k != 'source'})
            else:
                self.assertEqual(before, after, f'unapproved cell {i}')
        self.assertEqual({k: v for k, v in old.items() if k != 'cells'},
                         {k: v for k, v in new.items() if k != 'cells'})

    def test_exercise_todos_remain_incomplete(self):
        source, original = read_source(PATH), read_source(PATH, original=True)
        self.assertEqual(source.count('# YOUR CODE HERE'), original.count('# YOUR CODE HERE'))
        for notebook in (original, source):
            self.assertEqual(cell_source(notebook, 11).count('# YOUR CODE HERE'), 4)
            with self.assertRaises(SyntaxError):
                ast.parse(cell_source(notebook, 11))
        self.assertIn("features = dataframe.drop('target')", cell_source(source, 11))

    def completed_dataset(self, notebook, *, baseline):
        # Answers exist only in test memory; the archive remains an incomplete exercise.
        code = cell_source(notebook, 11)
        labels = "dataframe.pop('target')" if baseline else "dataframe['target'].to_numpy()"
        features = 'dict(dataframe)' if baseline else "{name: features[name].to_numpy() for name in features.columns}"
        code = code.replace('labels = # YOUR CODE HERE', 'labels = ' + labels, 1)
        for expression in ('tf.data.Dataset.from_tensor_slices((' + features + ', labels))',
                           'ds.shuffle(buffer_size=len(dataframe))', 'ds.batch(batch_size)'):
            code = code.replace('ds = # YOUR CODE HERE', 'ds = ' + expression, 1)
        self.assertNotIn('# YOUR CODE HERE', code)
        ast.parse(code)
        return code

    def load_frames(self):
        self.assertEqual(hashlib.sha256(HEART.read_bytes()).hexdigest(), HEART_HASH)
        provenance = json.loads((HEART.parent / 'provenance.json').read_text())['inputs'][0]
        self.assertEqual(provenance['sha256'], HEART_HASH)
        self.assertEqual(provenance['historical_equality'], 'unknown')
        frames = []
        for notebook in (read_source(PATH, original=True), read_source(PATH)):
            scope = {'pd': pd, 'pl': pl, 'URL': str(HEART)}
            exec(selected_code(cell_source(notebook, 7), [1]), scope)
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
        codes = [cell_source(read_source(PATH, original=original), 9)
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
            notebook = read_source(PATH, original=original)
            exec(self.completed_dataset(notebook, baseline=original), scope)
            functions.append(scope['df_to_dataset'])
        assert_dataset_boundaries(self, functions, cases, pd.testing.assert_frame_equal)


if __name__ == '__main__':
    unittest.main()
