"""Shared parity assertions for selected TensorFlow tabular teaching boundaries."""
from types import SimpleNamespace

import numpy as np


class RecordedDataset:
    """Capture raw boundary values and calls without implementing dataset behavior."""
    def __init__(self, value):
        self.value = value
        self.calls = []

    def shuffle(self, **kwargs):
        self.calls.append(('shuffle', kwargs))
        return self

    def batch(self, size):
        self.calls.append(('batch', size))
        return self


def recording_tf():
    return SimpleNamespace(data=SimpleNamespace(Dataset=SimpleNamespace(
        from_tensor_slices=RecordedDataset)))


def assert_arrays(test, before, after):
    test.assertIsInstance(after, np.ndarray)
    if before.dtype.kind in 'biuf':
        test.assertEqual(after.dtype, before.dtype)
        np.testing.assert_allclose(after, before, equal_nan=True)
    else:
        test.assertIn(after.dtype.kind, 'OU')
        np.testing.assert_array_equal(after, before)


def assert_prescribed_splits(test, codes, frames):
    """Compare the two actual random-split snippets on prescribed heart row positions."""
    results, calls = [], []
    positions = [np.random.RandomState(23).permutation(303),
                 np.random.RandomState(29).permutation(242)]
    for baseline, (code, frame) in zip((True, False), zip(codes, frames)):
        seen = []

        def split(rows, **kwargs):
            test.assertEqual(kwargs, {'test_size': 0.2}, 'retain original default randomness')
            i = len(seen)
            test.assertLess(i, 2)
            test.assertEqual(len(rows), len(positions[i]))
            ids = rows.index.to_numpy() if baseline else np.asarray(rows)
            seen.append(ids.copy())
            n_test = int(np.ceil(len(rows) * kwargs['test_size']))
            train_positions, test_positions = positions[i][n_test:], positions[i][:n_test]
            if baseline:
                return rows.iloc[train_positions], rows.iloc[test_positions]
            return ids[train_positions].tolist(), ids[test_positions].tolist()

        scope = {'dataframe': frame, 'train_test_split': split, 'print': lambda *args: None}
        exec(code, scope)
        test.assertEqual(len(seen), 2)
        results.append([scope[name] for name in ('train', 'val', 'test')])
        calls.append(seen)
    for old_call, new_call in zip(*calls):
        np.testing.assert_array_equal(old_call, new_call)
    test.assertEqual([len(frame) for frame in results[1]], [193, 49, 61])
    first_train = positions[0][61:]
    ids = [first_train[positions[1][49:]], first_train[positions[1][:49]], positions[0][:61]]
    test.assertEqual(sorted(np.concatenate(ids)), list(range(303)))
    for old, new, expected_ids in zip(*results, ids):
        np.testing.assert_array_equal(old.index.to_numpy(), expected_ids)
        test.assertEqual(new.columns, list(old.columns))
        for name in old.columns:
            assert_arrays(test, old[name].to_numpy(), new[name].to_numpy())


def assert_dataset_boundaries(test, functions, cases, assert_original_frame):
    """Check actual selected functions' values, calls and immutable frame inputs."""
    for frames in cases:
        for shuffle in (False, True):
            records = []
            for baseline, (function, frame) in zip((True, False), zip(functions, frames)):
                saved = frame.copy(deep=True) if baseline else frame.clone()
                dataset = function(frame, shuffle=shuffle, batch_size=7)
                expected = [('shuffle', {'buffer_size': len(frame)})] if shuffle else []
                test.assertEqual(dataset.calls, expected + [('batch', 7)])
                if baseline:
                    assert_original_frame(frame, saved)
                else:
                    test.assertTrue(frame.equals(saved))
                records.append(dataset.value)
            (old_features, old_labels), (features, labels) = records
            test.assertEqual(list(features), [name for name in frames[0].columns if name != 'target'])
            test.assertNotIn('target', features)
            test.assertNotIn('index', features)
            test.assertNotIn('row_id', features)
            for name in old_features:
                assert_arrays(test, np.asarray(old_features[name]), features[name])
            assert_arrays(test, np.asarray(old_labels), labels)
