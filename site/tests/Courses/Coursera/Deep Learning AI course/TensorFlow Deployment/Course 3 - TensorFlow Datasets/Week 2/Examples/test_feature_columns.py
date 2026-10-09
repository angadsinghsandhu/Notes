"""Real heart candidate and prescribed row splits; no TensorFlow/sklearn execution."""
import ast
import hashlib
import json
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest

import nbformat
import numpy as np
import pandas as pd
import polars as pl

SITE = next(parent for parent in Path(__file__).resolve().parents if parent.name == 'site')
sys.path.insert(0, str(SITE / 'scripts'))
from check_polars import cell_source, read_source, selected_code

PATH = 'Courses/Coursera/Deep Learning AI course/TensorFlow Deployment/Course 3 - TensorFlow Datasets/Week 2/Examples/feature_columns.ipynb'
ORIGINAL_HASH = 'edbf00fb9c4e94af7409d0b1a9787d75f0245385beb9d80f44fa628a94245398'
HEART = SITE / 'tests/fixtures/real/polars/heart.csv'
HEART_HASH = 'a91c81831bb2126e5fde6ce4ebde147a78429da12005108a6677ba57ecde9244'


class RecordedDataset:
    """Capture boundary arguments and pipeline calls without emulating datasets."""
    def __init__(self, value):
        self.value = value
        self.calls = []

    def shuffle(self, **kwargs):
        self.calls.append(('shuffle', kwargs))
        return self

    def batch(self, size):
        self.calls.append(('batch', size))
        return self


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

    def assert_arrays(self, before, after):
        self.assertIsInstance(after, np.ndarray)
        if before.dtype.kind in 'biuf':
            self.assertEqual(after.dtype, before.dtype)
            np.testing.assert_allclose(after, before, equal_nan=True)
        else:
            self.assertIn(after.dtype.kind, 'OU')
            np.testing.assert_array_equal(after, before)

    def test_full_real_heart_ingestion_and_prescribed_random_split_rows(self):
        before, after = self.load_frames()
        for name in before.columns:
            self.assert_arrays(before[name].to_numpy(), after[name].to_numpy())
        results, calls = [], []
        positions = [np.random.RandomState(23).permutation(303),
                     np.random.RandomState(29).permutation(242)]
        for notebook, frame in zip((read_source(PATH, original=True), read_source(PATH)), (before, after)):
            seen = []

            def split(rows, **kwargs):
                self.assertEqual(kwargs, {'test_size': 0.2}, 'retain original default randomness')
                i = len(seen)
                self.assertEqual(len(rows), len(positions[i]))
                ids = rows.index.to_numpy() if isinstance(rows, pd.DataFrame) else np.asarray(rows)
                seen.append(ids.copy())
                n_test = int(np.ceil(len(rows) * kwargs['test_size']))
                train_positions, test_positions = positions[i][n_test:], positions[i][:n_test]
                if isinstance(rows, pd.DataFrame):
                    return rows.iloc[train_positions], rows.iloc[test_positions]
                return ids[train_positions].tolist(), ids[test_positions].tolist()

            scope = {'dataframe': frame, 'train_test_split': split, 'print': lambda *args: None}
            exec(cell_source(notebook, 11), scope)
            results.append([scope[name] for name in ('train', 'val', 'test')])
            calls.append(seen)
        for old_call, new_call in zip(*calls):
            np.testing.assert_array_equal(old_call, new_call)
        self.assertEqual([len(frame) for frame in results[1]], [193, 49, 61])
        first_train = positions[0][61:]
        ids = [first_train[positions[1][49:]], first_train[positions[1][:49]], positions[0][:61]]
        self.assertEqual(sorted(np.concatenate(ids)), list(range(303)))
        for old, new, expected_ids in zip(*results, ids):
            np.testing.assert_array_equal(old.index.to_numpy(), expected_ids)
            self.assertEqual(new.columns, list(old.columns))
            for name in old.columns:
                self.assert_arrays(old[name].to_numpy(), new[name].to_numpy())

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
        for frames in cases:
            for shuffle in (False, True):
                recorded = []
                for notebook, frame in zip((read_source(PATH, original=True), read_source(PATH)), frames):
                    saved = frame.copy(deep=True) if isinstance(frame, pd.DataFrame) else frame.clone()
                    tf = SimpleNamespace(data=SimpleNamespace(Dataset=SimpleNamespace(
                        from_tensor_slices=RecordedDataset)))
                    scope = {'tf': tf}
                    exec(cell_source(notebook, 13), scope)
                    dataset = scope['df_to_dataset'](frame, shuffle=shuffle, batch_size=7)
                    expected = [('shuffle', {'buffer_size': len(frame)})] if shuffle else []
                    self.assertEqual(dataset.calls, expected + [('batch', 7)])
                    if isinstance(frame, pd.DataFrame):
                        pd.testing.assert_frame_equal(frame, saved)
                    else:
                        self.assertTrue(frame.equals(saved))
                    recorded.append(dataset.value)
                (old_features, old_labels), (features, labels) = recorded
                self.assertEqual(list(features), [name for name in frames[0].columns if name != 'target'])
                self.assertNotIn('target', features)
                self.assertNotIn('index', features)
                self.assertNotIn('row_id', features)
                for name in old_features:
                    self.assert_arrays(np.asarray(old_features[name]), features[name])
                self.assert_arrays(np.asarray(old_labels), labels)


if __name__ == '__main__':
    unittest.main()
