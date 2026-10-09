"""Selected real heart boundaries only; invalid FIXME and training stay untouched."""
import ast
import hashlib
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest

import numpy as np
import pandas as pd
import polars as pl

SITE = next(parent for parent in Path(__file__).resolve().parents if parent.name == 'site')
sys.path.insert(0, str(SITE / 'scripts'))
from check_polars import read_source, selected_code

PATH = 'Courses/Coursera/tf deployment/Course 3/Week 2/1_input_pipelines.py'
ORIGINAL_HASH = '1148e323f9084d3ef49efb453cd8e486a9b06961fa46ace4510b2eaefc1306b1'
HEART = SITE / 'tests/fixtures/real/polars/heart.csv'
HEART_HASH = 'a91c81831bb2126e5fde6ce4ebde147a78429da12005108a6677ba57ecde9244'
MARKER = '\n\nbatch_size = 5'
FIXME = 'FIXME(OverflowError: Python int too large to convert to C long)'


class RecordedDataset:
    """Record input arrays and arguments only, with no dataset/model behavior."""
    def __init__(self, value):
        self.value = value
        self.calls = []

    def shuffle(self, **kwargs):
        self.calls.append(('shuffle', kwargs))
        return self

    def batch(self, size):
        self.calls.append(('batch', size))
        return self


class InputPipelinesTest(unittest.TestCase):
    def test_polars_selected_syntax_and_invalid_fixme_preservation(self):
        source, original = read_source(PATH), read_source(PATH, original=True)
        self.assertEqual(hashlib.sha256(original.encode()).hexdigest(), ORIGINAL_HASH)
        self.assertIn('import polars as pl', source)
        self.assertNotIn('import pandas', source)
        self.assertNotIn('.iloc', source)
        self.assertIn('historical', source)
        self.assertIn('download.tensorflow.org/data/heart.csv', source)
        ast.parse(source.split(MARKER, 1)[0])
        self.assertEqual(source.split(MARKER, 1)[1], original.split(MARKER, 1)[1])
        for text in (original, source):
            self.assertIn(FIXME, text)
            with self.assertRaises(SyntaxError):
                ast.parse(text)

    def load_frames(self):
        self.assertEqual(hashlib.sha256(HEART.read_bytes()).hexdigest(), HEART_HASH)
        frames = []
        for source in (read_source(PATH, original=True), read_source(PATH)):
            scope = {'pd': pd, 'pl': pl, 'URL': str(HEART)}
            exec(selected_code(source.split(MARKER, 1)[0], [5]), scope)
            frames.append(scope['df'])
        self.assertIsInstance(frames[1], pl.DataFrame, 'heart read still returns Pandas')
        self.assertEqual(frames[1].shape, (303, 14))
        self.assertEqual(frames[1].columns, list(frames[0].columns))
        return frames

    def assert_arrays(self, before, after):
        self.assertIsInstance(after, np.ndarray)
        if before.dtype.kind in 'biuf':
            self.assertEqual(after.dtype, before.dtype)
            np.testing.assert_allclose(after, before, equal_nan=True)
        else:
            self.assertIn(after.dtype.kind, 'OU')
            np.testing.assert_array_equal(after, before)

    def selected_scope(self, source, frame):
        tf = SimpleNamespace(data=SimpleNamespace(Dataset=SimpleNamespace(
            from_tensor_slices=RecordedDataset)))
        scope = {'df': frame, 'tf': tf}
        # Explicit original AST positions: ratios/round lengths/slices plus df_to_dataset.
        exec(selected_code(source.split(MARKER, 1)[0], [7, 8, 9, 10, 11, 12, 13, 17]), scope)
        return scope

    def test_full_real_ingestion_and_round_contiguous_splits(self):
        before, after = self.load_frames()
        for name in before.columns:
            self.assert_arrays(before[name].to_numpy(), after[name].to_numpy())
        for length in (303, 0, 1, 5, 6, 8):
            frames = (before.iloc[:length], after[:length])
            scopes = [self.selected_scope(source, frame) for source, frame in
                      zip((read_source(PATH, original=True), read_source(PATH)), frames)]
            train_end = int(round(length * 0.8))
            val_start = int(round(train_end * 0.8))
            ranges = (range(val_start), range(val_start, train_end), range(train_end, length))
            if length == 303:
                self.assertEqual([len(scopes[1][key]) for key in ('train', 'val', 'test')], [194, 48, 61])
            for key, indices in zip(('train', 'val', 'test'), ranges):
                old, new = scopes[0][key], scopes[1][key]
                np.testing.assert_array_equal(old.index.to_numpy(), list(indices))
                self.assertEqual(len(new), len(indices))
                self.assertEqual(new.columns, list(old.columns))
                for name in old.columns:
                    self.assert_arrays(old[name].to_numpy(), new[name].to_numpy())

    def test_recorded_features_labels_shuffle_batch_and_immutable_input(self):
        before, after = self.load_frames()
        synthetic_before = before.iloc[:3].copy()
        synthetic_before.loc[0, 'oldpeak'] = np.nan
        synthetic_after = after[:3].with_columns(
            pl.Series('oldpeak', [None, after['oldpeak'][1], after['oldpeak'][2]], dtype=pl.Float64))
        for frames in ((before, after), (before.iloc[[4, 1, 2]], after[[4, 1, 2]]),
                       (before.iloc[:0], after[:0]), (synthetic_before, synthetic_after)):
            for shuffle in (False, True):
                records = []
                for source, frame in zip((read_source(PATH, original=True), read_source(PATH)), frames):
                    saved = frame.copy(deep=True) if isinstance(frame, pd.DataFrame) else frame.clone()
                    scope = self.selected_scope(source, frame)
                    dataset = scope['df_to_dataset'](frame, shuffle=shuffle, batch_size=7)
                    expected = [('shuffle', {'buffer_size': len(frame)})] if shuffle else []
                    self.assertEqual(dataset.calls, expected + [('batch', 7)])
                    records.append(dataset.value)
                    if isinstance(frame, pd.DataFrame):
                        pd.testing.assert_frame_equal(frame, saved)
                    else:
                        self.assertTrue(frame.equals(saved))
                (old_features, old_labels), (features, labels) = records
                self.assertEqual(list(features), [name for name in frames[0].columns if name != 'target'])
                self.assertNotIn('target', features)
                self.assertNotIn('index', features)
                self.assertNotIn('row_id', features)
                for name in old_features:
                    self.assert_arrays(np.asarray(old_features[name]), features[name])
                self.assert_arrays(np.asarray(old_labels), labels)

    def test_missing_target_still_fails_at_input_boundary(self):
        before, after = self.load_frames()
        for source, frame, error in zip((read_source(PATH, original=True), read_source(PATH)),
                                       (before.drop(columns='target'), after.drop('target')),
                                       (KeyError, pl.exceptions.ColumnNotFoundError)):
            with self.assertRaises(error):
                self.selected_scope(source, frame)['df_to_dataset'](frame)


if __name__ == '__main__':
    unittest.main()
