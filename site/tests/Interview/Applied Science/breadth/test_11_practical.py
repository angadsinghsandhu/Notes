"""Synthetic caller frames at the sklearn boundary; no classifier is fitted."""
import ast
import hashlib
from pathlib import Path
import sys
import unittest

import numpy as np
import pandas as pd
import polars as pl

SITE = next(parent for parent in Path(__file__).resolve().parents if parent.name == 'site')
sys.path.insert(0, str(SITE / 'scripts'))
from check_polars import read_source

PATH = 'Interview/Applied Science/breadth/11-practical.md'
ORIGINAL_HASH = 'f7c9b998b9f09de962cf7f1a9a22e2166ad9cfa6c90635775eba0c99d89743a7'


def domain_code(source):
    start = source.index('# Domain classifier\n')
    return source[start:source.index('\n```', start)]


def boundary(source, train, production, features):
    calls = []
    classifier = object()

    def record(model, x, y):
        calls.append((model, x, y))
        return np.array([0.5])

    scope = {'pd': pd, 'train': train, 'production': production, 'features': features,
             'RandomForestClassifier': lambda: classifier, 'cross_val_score': record}
    exec(compile(domain_code(source), '<domain classifier data boundary>', 'exec'), scope)
    assert len(calls) == 1 and calls[0][0] is classifier
    return scope['combined'], calls[0][1:]


class PracticalTest(unittest.TestCase):
    def test_polars_source_and_explicit_numpy_boundary(self):
        code = domain_code(read_source(PATH))
        self.assertIn('import polars as pl', code)
        self.assertNotIn('pd.', code)
        self.assertIn('combined.select(features).to_numpy()', code)
        self.assertIn('combined["source"].to_numpy()', code)
        ast.parse(code)

    def test_only_domain_fence_changes_and_frontmatter_survives(self):
        original = read_source(PATH, original=True)
        current = read_source(PATH)
        self.assertEqual(hashlib.sha256(original.encode()).hexdigest(), ORIGINAL_HASH)
        self.assertEqual(original.replace(domain_code(original), domain_code(current), 1), current)
        self.assertEqual(current.split('# Domain classifier\n')[0], original.split('# Domain classifier\n')[0])
        self.assertEqual(current.count('TODO'), original.count('TODO'))

    def test_order_labels_features_types_missingness_and_input_immutability(self):
        original = read_source(PATH, original=True)
        features = ['b', 'a']
        # Different incidental schemas and an existing source column must not reach sklearn.
        cases = [
            ({'a': [1, 2], 'b': [3.0, None], 'target': [9, 8], 'source': [7, 7]},
             {'a': [4.5], 'b': [float('nan')], 'metadata': ['unused'], 'source': [7]}),
            ({'a': [1, 2], 'b': [3, 4]}, {'a': [], 'b': []}),
            ({'a': [], 'b': []}, {'a': [1.5], 'b': [2.5]}),
        ]
        for left, right in cases:
            with self.subTest(left=left, right=right):
                before_train, before_production = pd.DataFrame(left), pd.DataFrame(right)
                # Pandas infers empty numeric lists as Float64; supply identical empty types.
                train = pl.DataFrame(left, schema_overrides={key: pl.Float64 for key, values in left.items() if not values})
                production = pl.DataFrame(right, schema_overrides={key: pl.Float64 for key, values in right.items() if not values})
                snapshots = train.clone(), production.clone()
                before, expected = boundary(original, before_train, before_production, features)
                after, actual = boundary(read_source(PATH), train, production, features)
                self.assertIsInstance(after, pl.DataFrame)
                self.assertEqual(after.columns, features + ['source'])
                self.assertEqual(after.height, len(before))
                self.assertEqual(after['source'].dtype, pl.Int64)
                self.assertIsInstance(actual[0], np.ndarray)
                self.assertIsInstance(actual[1], np.ndarray)
                np.testing.assert_allclose(actual[0], expected[0].to_numpy(), equal_nan=True)
                np.testing.assert_array_equal(actual[1], expected[1].to_numpy())
                self.assertEqual(actual[0].shape, (len(before), 2))
                self.assertEqual(actual[0].dtype, expected[0].to_numpy().dtype)
                self.assertEqual(actual[1].dtype, expected[1].to_numpy().dtype)
                self.assertTrue(train.equals(snapshots[0]))
                self.assertTrue(production.equals(snapshots[1]))
                self.assertEqual(list(before_train.columns), list(left))
                self.assertEqual(list(before_production.columns), list(right))


if __name__ == '__main__':
    unittest.main()
