"""Test-only comparisons/recorders; callers select their exact archive statements."""
import numpy as np
import pandas as pd

from polars_tf_support import assert_arrays


def assert_frame(test, before, after):
    test.assertEqual(after.columns, list(before.columns))
    test.assertEqual(after.shape, before.shape)
    for name in before.columns:
        assert_arrays(test, before[name].to_numpy(), after[name].to_numpy())


class SplitRecorder:
    """Supply prescribed positional splits at the sklearn boundary, without sklearn."""
    def __init__(self, test, positions):
        self.test = test
        self.positions = positions
        self.calls = []

    def __call__(self, rows, **kwargs):
        self.test.assertEqual(kwargs, {'test_size': 0.2})
        i = len(self.calls)
        self.test.assertLess(i, len(self.positions), 'unexpected extra split')
        order = self.positions[i]
        self.test.assertEqual(len(rows), len(order))
        self.calls.append(rows)
        count = int(np.ceil(len(rows) * 0.2))
        if isinstance(rows, pd.DataFrame):
            return rows.iloc[order[count:]].copy(), rows.iloc[order[:count]].copy()
        ids = np.asarray(rows)
        return ids[order[count:]].tolist(), ids[order[:count]].tolist()


class HistogramRecorder:
    def __init__(self):
        self.calls = []

    def hist(self, values, **kwargs):
        self.calls.append((np.asarray(values).copy(), kwargs))


def assert_model_arrays(test, old, new, features, splits):
    """Reject target swaps, feature leakage and population/full-data statistics."""
    for statistic in ('mean', 'std'):
        test.assertEqual(list(new['train_stats'][statistic]), features)
        np.testing.assert_allclose(list(new['train_stats'][statistic].values()),
                                   old['train_stats'][statistic].to_numpy(),
                                   rtol=1e-12, atol=1e-12, equal_nan=True)
    for name in splits:
        test.assertEqual(len(new[f'{name}_Y']), 2)
        for before, after in zip(old[f'{name}_Y'], new[f'{name}_Y']):
            assert_arrays(test, before, after)
        values = new[f'norm_{name}_X']
        test.assertIsInstance(values, np.ndarray)
        test.assertEqual(values.shape, (len(old[f'norm_{name}_X']), len(features)))
        np.testing.assert_allclose(values, old[f'norm_{name}_X'].to_numpy(),
                                   rtol=1e-12, atol=1e-12, equal_nan=True)
