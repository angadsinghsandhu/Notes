"""Complete UCI wine parity, selected cells only; training and models never execute."""
import ast
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

import nbformat
import numpy as np
import pandas as pd
import polars as pl

SITE = next(p for p in Path(__file__).resolve().parents if p.name == 'site')
sys.path.insert(0, str(SITE / 'scripts'))
from check_polars import cell_source, read_source, selected_code
from polars_wine_support import (HistogramRecorder, SplitRecorder, assert_frame,
                                 assert_model_arrays)

BASE = 'Courses/Coursera/Deep Learning AI course/Advanced TensorFlow/Extending Keras/Week 1 - Functional API/'
FIXTURES = SITE / 'tests/fixtures/real/polars'
FEATURES = ['fixed acidity', 'volatile acidity', 'citric acid', 'residual sugar', 'chlorides',
            'free sulfur dioxide', 'total sulfur dioxide', 'density', 'pH', 'sulphates', 'alcohol']


class WineAnswerTest(unittest.TestCase):
    PATH = BASE + 'exercise-answer.ipynb'
    HASH = 'f4f562896ca209a43d294571efeb46a712994e1d67cc4fa22e3897714a4dde81'

    def codes(self, source, converted):
        # Source-specific explicit boundary: no model cells, imports or whole notebook.
        return {i: cell_source(source, i) for i in (6, 7, 8, 9, 11, 12, 15, 17, 18, 20,
                                                   22, 23, 25, 29, 30, 32, 33)}

    def test_polars_contract_syntax_todos_and_exact_raw_notebook_preservation(self):
        source, old = read_source(self.PATH), read_source(self.PATH, original=True)
        self.assertEqual(hashlib.sha256(old.encode()).hexdigest(), self.HASH)
        self.assertIn('import polars as pl', cell_source(source, 4))
        self.assertNotIn('import pandas', source)
        self.assertEqual(old.count('# YOUR CODE HERE'), source.count('# YOUR CODE HERE'))
        self.assertIn('source_row', cell_source(source, 7))
        self.assertIn('source_row', cell_source(source, 9))
        for code in self.codes(source, True).values():
            ast.parse(code)
        ast.parse(cell_source(source, 4).replace('  %tensorflow_version 2.x', '  pass'))
        before, after = json.loads(old), json.loads(source)
        nbformat.validate(after)
        self.assertEqual(len(before['cells']), len(after['cells']))
        allowed = {4, 5, 6, 7, 8, 9, 11, 12, 13, 15, 17, 18, 20, 22, 23, 24, 25, 28, 29, 31, 32}
        for i, (a, b) in enumerate(zip(before['cells'], after['cells'])):
            if i in allowed:
                self.assertEqual({k: v for k, v in a.items() if k != 'source'}, {k: v for k, v in b.items() if k != 'source'})
            else:
                self.assertEqual(a, b, f'unapproved cell {i}')
        self.assertEqual({k: v for k, v in before.items() if k != 'cells'}, {k: v for k, v in after.items() if k != 'cells'})
        for i in (1, *range(34, 59)):
            self.assertEqual(before['cells'][i], after['cells'][i], f'license/model/TODO cell {i}')

    def load_wines(self, converted, paths=None):
        codes = self.codes(read_source(self.PATH, original=not converted), converted)
        scope = {'pd': pd, 'pl': pl, 'np': np}
        for cell, color in ((6, 'white'), (8, 'red')):
            scope['URL'] = str((paths or {}).get(color, FIXTURES / f'winequality-{color}.csv'))
            exec(selected_code(codes[cell], [1, 2, 3]), scope)
        return scope, codes

    def test_full_actual_wine_dedup_source_labels_histograms_splits_and_model_arrays(self):
        for name, digest in [('winequality-red.csv', '4a402cf041b025d4566d954c3b9ba8635a3a8a01e039005d97d6a710278cf05e'),
                             ('winequality-white.csv', '76c3f809815c17c07212622f776311faeb31e87610d52c26d87d6e361b169836')]:
            self.assertEqual(hashlib.sha256((FIXTURES / name).read_bytes()).hexdigest(), digest)
        with self.assertRaisesRegex(pl.exceptions.ComputeError, '40.5'):
            pl.read_csv(FIXTURES / 'winequality-red.csv', separator=';')
        old, a = self.load_wines(False)
        new, b = self.load_wines(True)
        self.assertIsInstance(new['red_df'], pl.DataFrame, 'wine ingestion still returns Pandas')
        for color, count in (('red', 1359), ('white', 3961)):
            before, after = old[f'{color}_df'], new[f'{color}_df']
            self.assertEqual(len(after), count)
            np.testing.assert_array_equal(after['source_row'].to_numpy(), before.index.to_numpy())
            assert_frame(self, before, after.drop('source_row'))
        self.assertEqual(new['red_df']['free sulfur dioxide'].dtype, pl.Float64)
        self.assertIn(40.5, new['red_df']['free sulfur dioxide'].to_list())
        for cell, expected in ((7, [8.8, 9.1]), (9, [9.4, 10.2]), (12, [9.4, 9.5]), (18, [9.4, 10.9])):
            if cell == 12:
                exec(a[11], old); exec(b[11], new)
                assert_frame(self, old['df'], new['df'])
                self.assertEqual(new['df'].shape, (5320, 13))
            if cell == 18:
                exec(a[17], old); exec(b[17], new)
                assert_frame(self, old['df'], new['df'])
                self.assertEqual(new['df'].shape, (4931, 13))
            recorded = []
            for codes, scope in ((a, old), (b, new)):
                values = []; scope['print'] = values.append
                exec(codes[cell], scope)
                self.assertEqual(values, expected)
                recorded.append(values)
            np.testing.assert_array_equal(*recorded)
            if cell in (12, 18):
                histogram_cell = 15 if cell == 12 else 20
                before_plot, after_plot = HistogramRecorder(), HistogramRecorder()
                with patch.object(pd.Series, 'hist', lambda series, **kwargs: before_plot.hist(series.to_numpy(), **kwargs)):
                    exec(a[histogram_cell], old)
                new['plt'] = after_plot
                exec(b[histogram_cell], new)
                self.assertEqual(before_plot.calls[0][1], {'bins': 20})
                self.assertEqual(after_plot.calls[0][1], {'bins': 20})
                np.testing.assert_array_equal(before_plot.calls[0][0], after_plot.calls[0][0])
                self.assertEqual(len(after_plot.calls[0][0]), 5320 if cell == 12 else 4931)
        positions = [np.random.RandomState(23).permutation(4931), np.random.RandomState(29).permutation(3944)]
        for codes, scope in ((a, old), (b, new)):
            scope['train_test_split'] = SplitRecorder(self, positions)
            exec(codes[22], scope)
            self.assertEqual(len(scope['train_test_split'].calls), 2)
        for name, count in (('train', 3155), ('val', 789), ('test', 987)):
            assert_frame(self, old[name], new[name]); self.assertEqual(len(new[name]), count)
        values = []; new['print'] = values.append
        exec(b[23], new); self.assertEqual(values, [41015, 12831, 10257])
        saved = {name: new[name].clone() for name in ('train', 'val', 'test')}
        for codes, scope in ((a, old), (b, new)):
            for cell in (25, 29, 30, 32, 33): exec(codes[cell], scope)
        self.assertEqual(new['FEATURES'], FEATURES)
        assert_model_arrays(self, old, new, FEATURES, ['train', 'val', 'test'])
        for name in saved: self.assertTrue(new[name].equals(saved[name]), 'outputs/norm mutated source features')
        self.assertFalse(np.allclose(list(new['train_stats']['mean'].values()), new['df'].select(FEATURES).mean().row(0)))

    def test_synthetic_missing_duplicate_and_normalization_edges(self):
        original, a = self.load_wines(False)
        converted, b = self.load_wines(True)
        self.assertIsInstance(converted['red_df'], pl.DataFrame, 'wine ingestion still returns Pandas')
        # CSV-supplied NaN and blank represent missing numeric values; first duplicate survives.
        header = ';'.join(FEATURES + ['quality']) + '\n'
        row = ['1.0'] * 11 + ['5']
        nan = row.copy(); nan[0] = 'NaN'
        blank = row.copy(); blank[0] = ''
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'synthetic-wine.csv'
            path.write_text(header + '\n'.join(';'.join(r) for r in (row, row, nan, blank)) + '\n')
            old, _ = self.load_wines(False, {'red': path, 'white': path})
            new, _ = self.load_wines(True, {'red': path, 'white': path})
            for color in ('red', 'white'):
                before, after = old[f'{color}_df'], new[f'{color}_df']
                self.assertEqual(after['source_row'].to_list(), [0, 2])
                assert_frame(self, before, after.drop('source_row'))
            # Missing targets, boundary qualities and duplicate missingness are synthetic.
            rows = [row[:-1] + [quality] for quality in ('', 'NaN', '4', '5', '7', '8')]
            path.write_text(header + '\n'.join(';'.join(r) for r in rows) + '\n')
            old, _ = self.load_wines(False, {'red': path, 'white': path})
            new, _ = self.load_wines(True, {'red': path, 'white': path})
            for cell in (11, 17):
                exec(a[cell], old); exec(b[cell], new)
                assert_frame(self, old['df'], new['df'])
            self.assertEqual(new['df']['quality'].to_list(), [5., 7., 5., 7.])
        edge = original['red_df'].iloc[:5].copy()
        edge.iloc[0, 0] = np.nan; edge.iloc[1, 1] = np.nan
        edge['citric acid'] = 1.0
        frame = pl.DataFrame({n: edge[n].to_numpy() for n in edge}).with_columns(
            pl.when(pl.int_range(pl.len()) == 0).then(None).otherwise(pl.col('fixed acidity')).alias('fixed acidity'))
        original['train'], converted['train'] = edge.copy(), frame
        for codes, scope in ((a, original), (b, converted)):
            for cell in (25, 29, 32): exec(codes[cell], scope)
        labels = original['format_output'](original['train'])
        for before, after in zip(labels, converted['format_output'](frame)):
            np.testing.assert_array_equal(before, after)
        with np.errstate(invalid='ignore', divide='ignore'):
            np.testing.assert_allclose(converted['norm'](frame), original['norm'](original['train']).to_numpy(), equal_nan=True)
        self.assertEqual(converted['norm'](frame[:0]).shape, (0, 11))
        self.assertTrue(frame.equals(converted['train']))


if __name__ == '__main__':
    unittest.main()
