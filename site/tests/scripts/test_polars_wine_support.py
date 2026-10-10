"""Shared wine assertions reject reordered/retargeted values and wrong splits."""
import importlib.util
from pathlib import Path
import sys
import unittest

import numpy as np
import pandas as pd
import polars as pl

SITE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SITE / 'scripts'))
HELPER = SITE / 'scripts/polars_wine_support.py'


class WineSupportTest(unittest.TestCase):
    def setUp(self):
        self.assertTrue(HELPER.exists(), 'shared wine parity assertions missing')
        spec = importlib.util.spec_from_file_location('polars_wine_support', HELPER)
        self.helper = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.helper)

    def test_frame_comparison_checks_values_order_dtype_and_missingness(self):
        old = pd.DataFrame({'x': [1., np.nan], 'quality': [5, 6]})
        new = pl.DataFrame({'x': [1., None], 'quality': [5, 6]})
        self.helper.assert_frame(self, old, new)
        for bad in (new.reverse(), new.select('quality', 'x'), new.with_columns(pl.lit(7).alias('quality')),
                    new.with_columns(pl.col('quality').cast(pl.Float64))):
            with self.assertRaises(AssertionError):
                self.helper.assert_frame(self, old, bad)

    def test_split_recorder_retains_prescribed_positions_and_rejects_wrong_boundary(self):
        old = pd.DataFrame({'x': np.arange(5)}, index=[9, 8, 7, 6, 5])
        position = np.array([3, 0, 4, 1, 2])
        before = self.helper.SplitRecorder(self, [position])
        after = self.helper.SplitRecorder(self, [position])
        a, b = before(old, test_size=0.2)
        c, d = after(range(5), test_size=0.2)
        self.assertEqual(a.index.tolist(), [9, 5, 8, 7])
        self.assertEqual(b.index.tolist(), [6])
        self.assertEqual((c, d), ([0, 4, 1, 2], [3]))
        with self.assertRaises(AssertionError):
            self.helper.SplitRecorder(self, [position])(range(5), test_size=0.3)
        with self.assertRaises(AssertionError):
            self.helper.SplitRecorder(self, [position])(range(4), test_size=0.2)
        with self.assertRaises(AssertionError):
            after(range(5), test_size=0.2)

    def test_histogram_records_real_numpy_values_without_mutable_alias(self):
        recorder = self.helper.HistogramRecorder()
        values = np.array([5, 6, 5])
        recorder.hist(values, bins=20)
        values[0] = 9
        self.assertEqual(recorder.calls[0][1], {'bins': 20})
        np.testing.assert_array_equal(recorder.calls[0][0], [5, 6, 5])

    def test_model_assertion_rejects_target_swap_and_feature_leak(self):
        frame = pd.DataFrame({'x': [1., 3.], 'quality': [5, 6], 'is_red': [0, 1]})
        data = pl.DataFrame({n: frame[n].to_numpy() for n in frame})
        old = {'train_Y': (np.array([5, 6]), np.array([0, 1])), 'norm_train_X': pd.DataFrame({'x': [-1., 1.]}),
               'train_stats': frame[['x']].describe().transpose()}
        new = {'train_Y': old['train_Y'], 'norm_train_X': np.array([[-1.], [1.]]),
               'train_stats': {'mean': {'x': 2.}, 'std': {'x': np.sqrt(2.)}}}
        self.helper.assert_model_arrays(self, old, new, ['x'], ['train'])
        for bad in (dict(new, train_Y=tuple(reversed(new['train_Y']))),
                    dict(new, norm_train_X=np.zeros((2, 2))),
                    dict(new, train_stats={'mean': {'x': 2.}, 'std': {'x': 1.}})):
            with self.assertRaises(AssertionError):
                self.helper.assert_model_arrays(self, old, bad, ['x'], ['train'])


if __name__ == '__main__':
    unittest.main()
