"""Shared recorder/assertions prove real selected archive boundaries and reject drift."""
import importlib.util
from pathlib import Path
import sys
import unittest

import numpy as np
import pandas as pd
import polars as pl

SITE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SITE / 'scripts'))
from check_polars import cell_source, read_source

HELPER = SITE / 'scripts/polars_tf_support.py'
PATH = 'Courses/Coursera/Deep Learning AI course/TensorFlow Deployment/Course 3 - TensorFlow Datasets/Week 2/Examples/feature_columns.ipynb'
HEART = SITE / 'tests/fixtures/real/polars/heart.csv'


class PolarsTFSupportTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if HELPER.exists():
            spec = importlib.util.spec_from_file_location('polars_tf_support', HELPER)
            cls.helper = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(cls.helper)

    def setUp(self):
        self.assertTrue(HELPER.exists(), 'shared TensorFlow parity support is missing')

    def frames(self):
        return pd.read_csv(HEART), pl.read_csv(HEART)

    def dataset_functions(self):
        functions = []
        for original in (True, False):
            scope = {'tf': self.helper.recording_tf()}
            exec(cell_source(read_source(PATH, original=original), 13), scope)
            functions.append(scope['df_to_dataset'])
        return functions

    def test_recorder_retains_raw_values_and_call_order(self):
        value = ({'kind': np.array(['a', 'b'])}, np.array([1, 0], dtype=np.int64))
        dataset = self.helper.recording_tf().data.Dataset.from_tensor_slices(value)
        self.assertIs(dataset.value, value)
        self.assertEqual(dataset.calls, [])
        self.assertIs(dataset.batch(3).shuffle(buffer_size=2).batch(7), dataset)
        self.assertEqual(dataset.calls, [('batch', 3), ('shuffle', {'buffer_size': 2}), ('batch', 7)])

    def test_typed_arrays_preserve_numeric_nan_string_and_empty_values(self):
        for before, after in (
                (np.array([True, False]), np.array([True, False])),
                (np.array([2, 1], dtype=np.int64), np.array([2, 1], dtype=np.int64)),
                (np.array([np.nan, 1.5]), np.array([np.nan, 1.5])),
                (np.array([], dtype=np.float64), np.array([], dtype=np.float64)),
                (np.array(['b', 'a'], dtype=object), np.array(['b', 'a'])),
                (np.array([], dtype=object), np.array([], dtype=str))):
            with self.subTest(dtype=before.dtype):
                self.helper.assert_arrays(self, before, after)

    def test_array_assertion_rejects_dtype_order_missingness_and_non_arrays(self):
        for before, after in (
                (np.array([1], dtype=np.int64), np.array([1.0])),
                (np.array([1, 2]), np.array([2, 1])),
                (np.array([np.nan]), np.array([0.0])),
                (np.array(['a', 'b'], dtype=object), np.array(['b', 'a'])),
                (np.array(['1'], dtype=object), np.array([1])),
                (np.array([1]), [1])):
            with self.subTest(after=after), self.assertRaises(AssertionError):
                self.helper.assert_arrays(self, before, after)

    def test_real_prescribed_split_records_order_and_defaults(self):
        codes = [cell_source(read_source(PATH, original=old), 11) for old in (True, False)]
        self.helper.assert_prescribed_splits(self, codes, self.frames())

    def test_split_verification_rejects_changed_defaults_and_row_order(self):
        codes = [cell_source(read_source(PATH, original=old), 11) for old in (True, False)]
        with self.assertRaises(AssertionError):
            self.helper.assert_prescribed_splits(self,
                [codes[0], codes[1].replace('test_size=0.2', 'test_size=0.3')], self.frames())
        before, after = self.frames()
        with self.assertRaises(AssertionError):
            self.helper.assert_prescribed_splits(self, codes, (before, after.reverse()))

    def test_real_dataset_boundary_handles_reordered_empty_and_numeric_null_frames(self):
        before, after = self.frames()
        missing_before = before.iloc[:3].copy()
        missing_before.loc[0, 'oldpeak'] = np.nan
        missing_after = after[:3].with_columns(pl.Series('oldpeak',
            [None, after['oldpeak'][1], after['oldpeak'][2]], dtype=pl.Float64))
        cases = [(before, after), (before.iloc[[4, 1, 2]], after[[4, 1, 2]]),
                 (before.iloc[:0], after[:0]), (missing_before, missing_after)]
        self.helper.assert_dataset_boundaries(self, self.dataset_functions(), cases,
                                              pd.testing.assert_frame_equal)

    def test_boundary_assertion_rejects_input_mutation_and_feature_or_call_drift(self):
        baseline, converted = self.dataset_functions()
        for defect in ('mutation', 'target', 'index', 'row_id', 'order', 'dtype', 'calls', 'labels'):
            def corrupt(frame, **kwargs):
                dataset = converted(frame, **kwargs)
                features, labels = dataset.value
                if defect == 'mutation':
                    frame.drop_in_place('thal')
                elif defect in ('target', 'index', 'row_id'):
                    features[defect] = labels
                elif defect == 'order':
                    dataset.value = (dict(reversed(list(features.items()))), labels)
                elif defect == 'dtype':
                    features['age'] = features['age'].astype(np.float64)
                elif defect == 'calls':
                    dataset.calls.reverse()
                    dataset.calls.append(('batch', 99))
                else:
                    dataset.value = (features, labels[::-1])
                return dataset
            with self.subTest(defect=defect), self.assertRaises(AssertionError):
                self.helper.assert_dataset_boundaries(self, (baseline, corrupt), [self.frames()],
                                                      pd.testing.assert_frame_equal)


if __name__ == '__main__':
    unittest.main()
