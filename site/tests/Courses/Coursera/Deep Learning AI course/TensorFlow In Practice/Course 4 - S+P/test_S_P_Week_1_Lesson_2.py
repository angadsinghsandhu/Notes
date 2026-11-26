"""Selected time-series cells: real Pandas oracle, recorded plotting boundaries."""
import ast
from datetime import date
import hashlib
import json
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import warnings

import numpy as np
import pandas as pd
import polars as pl

SITE = next(p for p in Path(__file__).resolve().parents if p.name == 'site')
sys.path.insert(0, str(SITE / 'scripts'))
from check_polars import cell_source, read_source, selected_code

PATH = 'Courses/Coursera/Deep Learning AI course/TensorFlow In Practice/Course 4 - S+P/S+P_Week_1_Lesson_2.ipynb'
HASH = '45e8c5fb46b384d680342f9536667d3d674c70d3c01ca325054f32e9fdebd5cb'
FIXTURE = SITE / 'tests/fixtures/real/polars/sunspots.csv'
FIXTURE_HASH = '0ef4cf0379879a9be0043885d8de1c1907ae852c903a0fcbbc58ba813efb3f10'
VALUE = 'Monthly Mean Total Sunspot Number'


class RecordingAxis:
    def __init__(self):
        self.calls = []

    def __getattr__(self, name):
        if name not in {'set_xlim', 'set_ylim', 'axhline', 'set_xlabel',
                        'set_ylabel', 'plot', 'legend', 'grid', 'figure',
                        'axis', 'show'}:
            raise AttributeError(name)
        def record(*args, **kwargs):
            self.calls.append((name, args, kwargs))
        return record


def original_text():
    current = read_source(PATH)
    return current if hashlib.sha256(current.encode()).hexdigest() == HASH else read_source(PATH, original=True)


def plotting_oracle(axis):
    # Execute installed Pandas arithmetic, adapting only its Matplotlib boundary.
    path = Path(pd.__file__).parent / 'plotting/_matplotlib/misc.py'
    tree = ast.parse(path.read_text())
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'autocorrelation_plot')
    imports = [n for n in fn.body if isinstance(n, ast.Import)]
    assert len(imports) == 1
    assert [(n.name, n.asname) for n in imports[0].names] == [('matplotlib.pyplot', 'plt')]
    fn.body.remove(imports[0])
    fn.returns = None
    for arg in fn.args.args:
        arg.annotation = None
    scope = {'np': np, 'plt': SimpleNamespace(gca=lambda: axis)}
    exec(compile(ast.fix_missing_locations(ast.Module(body=[fn], type_ignores=[])), str(path), 'exec'), scope)
    return scope['autocorrelation_plot']


class TimeSeriesTest(unittest.TestCase):
    def setUp(self):
        self.old = original_text()
        self.new = read_source(PATH)
        self.warnings = warnings.catch_warnings()
        self.warnings.__enter__()
        warnings.simplefilter('ignore', RuntimeWarning)
        self.addCleanup(self.warnings.__exit__, None, None, None)

    def code(self, index, original=False):
        return cell_source(self.old if original else self.new, index)

    def scope(self):
        self.assertIn('import polars as pl', self.code(35), 'F10 tabular/ACF conversion missing')
        axis = RecordingAxis()
        scope = {'np': np, 'plt': SimpleNamespace(gca=lambda: axis, **{
            name: getattr(axis, name) for name in ('figure', 'plot', 'axis', 'show')})}
        tree = ast.parse(self.code(35))
        tree.body = [n for n in tree.body if not isinstance(n, ast.Expr)]
        exec(compile(tree, '<F10 definitions only>', 'exec'), scope)
        exec(selected_code(self.code(37), [0]), scope)
        scope['axis'] = axis
        return scope

    def old_monthly(self):
        tree = ast.parse(self.code(37, True))
        aliases = [n for n in ast.walk(tree) if isinstance(n, ast.Constant) and n.value == '1M']
        self.assertEqual(len(aliases), 1)
        self.assertEqual(aliases[0].lineno, 2)
        aliases[0].value = '1ME'  # TEST-MEMORY only: Pandas3 removed the original month-end alias.
        def read(path, **kwargs):
            self.assertEqual(path, 'sunspots.csv')
            return pd.read_csv(FIXTURE, **kwargs)
        scope = {'pd': SimpleNamespace(read_csv=read)}
        exec(compile(tree, '<original cell37 alias adapter>', 'exec'), scope)
        return scope['series']

    def new_monthly(self, scope):
        reader = pl.read_csv
        def read(path, **kwargs):
            self.assertEqual(path, 'sunspots.csv')
            return reader(FIXTURE, **kwargs)
        with patch.object(pl, 'read_csv', read):
            exec(selected_code(self.code(37), [1, 2, 3]), scope)
        return scope['series']

    def frame_equal(self, frame, expected):
        self.assertEqual(frame.columns, ['Date', VALUE])
        self.assertEqual(frame.schema, {'Date': pl.Date, VALUE: pl.Float64})
        self.assertEqual(frame['Date'].to_list(), [d.date() for d in expected.index])
        np.testing.assert_allclose(frame[VALUE].to_numpy(), expected.to_numpy(), rtol=1e-12, atol=1e-12, equal_nan=True)

    def plot_equal(self, values, scope):
        expected = RecordingAxis()
        plotting_oracle(expected)(pd.Series(values, dtype=float), label='oracle')
        scope['axis'].calls.clear()
        self.assertIs(scope['autocorrelation_plot'](values, label='oracle'), scope['axis'])
        self.assertEqual(len(scope['axis'].calls), len(expected.calls))
        for actual, wanted in zip(scope['axis'].calls, expected.calls):
            self.assertEqual((actual[0], actual[2]), (wanted[0], wanted[2]))
            if actual[0] == 'plot':
                np.testing.assert_array_equal(actual[1][0], wanted[1][0])
                np.testing.assert_allclose(actual[1][1], wanted[1][1], rtol=1e-11, atol=1e-12, equal_nan=True)
            else:
                self.assertEqual(actual[1], wanted[1])

    def test_source_contract_and_preserved_fields(self):
        self.scope()
        self.assertNotIn('pandas', ''.join(self.code(i) for i in [35, *range(37, 50)]))
        self.assertEqual(hashlib.sha256(self.old.encode()).hexdigest(), HASH)
        old, new = json.loads(self.old), json.loads(self.new)
        allowed = {35, *range(37, 45), 46, 47, 48, 49}
        self.assertEqual(len(new['cells']), 50)
        self.assertEqual(new['metadata'], old['metadata'])
        for i, (before, after) in enumerate(zip(old['cells'], new['cells'])):
            if i not in allowed:
                self.assertEqual(after, before, f'protected cell {i}')
            else:
                for key in set(before) | set(after):
                    if key == 'source' or (i == 35 and key in {'outputs', 'execution_count'}) or (i == 47 and key in {'cell_type', 'outputs', 'execution_count'}):
                        continue
                    self.assertEqual(after.get(key), before.get(key), (i, key))
                if i != 47:
                    compile(self.code(i), f'<converted cell {i}>', 'exec')
        self.assertEqual(new['cells'][35]['outputs'], [])
        self.assertIsNone(new['cells'][35]['execution_count'])
        self.assertEqual(new['cells'][47]['cell_type'], 'markdown')
        self.assertIn('https://docs.pola.rs/api/python/stable/reference/api/polars.read_csv.html', self.code(47))
        self.assertIn('positional', self.code(48))
        self.assertIn('aligned', self.code(49))

    def test_actual_original_baseline_and_indexed_subtraction_defect(self):
        old = self.old_monthly()
        self.assertEqual(len(old), 3235)
        np.testing.assert_array_equal(old.iloc[:3], [96.7, 104.3, 116.7])
        double = old.diff(1)[1:].diff(11 * 12)[11 * 12 + 1:]
        self.assertEqual((len(double), double.index[0].date()), (3101, date(1760, 3, 31)))
        self.assertAlmostEqual(double.iloc[0], 12.9)
        self.assertAlmostEqual(double.iloc[-1], -8.1)
        scope = {'series': old, 'autocorrelation_plot': lambda values: None}
        exec(selected_code(self.code(48, True), [1, 2]), scope)
        bad = scope['series_diff']
        self.assertEqual(len(bad), 3235)
        self.assertEqual(bad.isna().sum(), 2)
        self.assertTrue((bad.iloc[1:-1] == 0).all())
        scope['pd'] = pd
        exec(selected_code(self.code(49, True), [1, 2]), scope)
        self.assertTrue(np.isnan(scope['autocorrs']).all())
        small = pd.Series([1., 3., 8., 15., 24.], index=pd.date_range('2020-01-31', periods=5, freq='ME'))
        np.testing.assert_array_equal(small[1:] - small[:-1], [np.nan, 0., 0., 0., np.nan])

    def test_actual_fixture_monthly_and_all_dependent_plot_boundaries(self):
        scope = self.scope()
        self.assertEqual(hashlib.sha256(FIXTURE.read_bytes()).hexdigest(), FIXTURE_HASH)
        record = next(r for r in json.loads((FIXTURE.parent / 'provenance.json').read_text())['inputs'] if r['filename'] == FIXTURE.name)
        self.assertEqual(record['sha256'], FIXTURE_HASH)
        self.assertIn('historical', record['evidence'])
        old, frame = self.old_monthly(), self.new_monthly(scope)
        self.assertEqual(old.index.name, 'Date')
        self.frame_equal(frame, old)
        self.assertEqual(len(frame), 3235)
        self.assertEqual(frame['Date'][0], date(1749, 1, 31))
        self.assertEqual(frame['Date'][-1], date(2018, 7, 31))
        expected = {38: old, 39: old['1995-01-01':], 40: old.diff(1)}
        for i, series in expected.items():
            scope['axis'].calls.clear()
            exec(compile(self.code(i), f'<plot cell{i}>', 'exec'), scope)
            plot = next(args for name, args, kw in scope['axis'].calls if name == 'plot')
            np.testing.assert_array_equal(plot[0], series.index.to_numpy().astype('datetime64[D]'))
            np.testing.assert_allclose(plot[1], series.to_numpy(), equal_nan=True)
            self.assertIn(('set_xlabel', ('Date',), {}), scope['axis'].calls)
            if i == 38:
                self.assertIn(('figure', (), {'figsize': (12, 5)}), scope['axis'].calls)
            if i == 40:
                self.assertIn(('axis', ([0, 100, -50, 50],), {}), scope['axis'].calls)
        inputs = {41: old, 42: old.diff(1)[1:], 43: old.diff(1)[1:].diff(132)[133:], 44: old.diff(1)[1:]}
        for i, series in inputs.items():
            recorded = []
            actual_plot = scope['autocorrelation_plot']
            scope['autocorrelation_plot'] = lambda values: recorded.append(values)
            exec(compile(self.code(i), f'<ACF cell{i}>', 'exec'), scope)
            scope['autocorrelation_plot'] = actual_plot
            np.testing.assert_allclose(recorded[0].to_numpy(), series.to_numpy(), equal_nan=True)
            if i == 42:
                self.assertIn('series_diff1', scope, 'retain Date through first difference')
                self.frame_equal(scope['series_diff1'], series)
            if i == 43:
                self.assertIn('double_diff', scope, 'retain Date through exact double lag')
                self.frame_equal(scope['double_diff'], series)
                self.assertEqual((len(scope['double_diff']), scope['double_diff']['Date'][0]),
                                 (3101, frame['Date'][134]))
                self.assertIn(('axis', ([0, 500, -0.1, 0.1],), {}), scope['axis'].calls)
            if i == 44:
                self.assertIn(('axis', ([0, 50, -0.1, 0.1],), {}), scope['axis'].calls)
            self.plot_equal(recorded[0], scope)
        self.assertIn('[0, 500, -0.1, 0.1]', self.code(43))
        self.assertIn('[0, 50, -0.1, 0.1]', self.code(44))
        actual = eval(compile(ast.Expression(ast.parse(self.code(46)).body[0].value), '<cell46>', 'eval'), scope)
        np.testing.assert_allclose(actual, [old.autocorr(lag) for lag in range(1, 50)], rtol=1e-12, atol=1e-12)
        self.assertEqual(len(actual), 49)

    def test_actual_generated_series_plotting_oracle(self):
        scope = self.scope()
        generated = {'np': np, 'time': np.arange(4 * 365 + 1)}
        for i in [29, 31]:
            exec(compile(self.code(i, True), '<original generation definition>', 'exec'), generated)
        exec(selected_code(self.code(33, True), [0, 1]), generated)
        self.assertEqual(len(generated['series']), 1461)
        self.plot_equal(generated['series'], scope)

    def test_synthetic_calendars_keep_original_labels_gaps_bounds_and_duplicates(self):
        scope = self.scope()
        cases = [(['2020-01-15', '2020-01-31', '2020-02-15', '2020-03-31', '2020-04-15'], [15., 31., 215., 331., 415.]),
                 (['2019-12-31', '2020-02-29', '2020-04-30'], [12., 2., 4.]),
                 (['2020-01-15', '2020-03-15'], [1., 3.]),
                 (['2020-01-05', '2020-01-15'], [5., 15.]),
                 (['2020-03-31', '2020-01-15', '2020-01-31'], [3., 15., 1.]),
                 (['2020-01-31', '2020-02-29', '2020-03-31', '2020-04-30'], [1., None, np.nan, np.inf]),
                 ([], [])]
        for dates, values in cases:
            with self.subTest(dates=dates):
                old = pd.Series(values, dtype=float, index=pd.to_datetime(dates)).asfreq('1ME')
                frame = pl.DataFrame({'Date': [date.fromisoformat(d) for d in dates], VALUE: values}, schema={'Date': pl.Date, VALUE: pl.Float64})
                new = scope['monthly_series'](frame)
                self.frame_equal(new, old)
                for lag in [1, 2, 132]:
                    self.frame_equal(new.with_columns(pl.col(VALUE).diff(lag)), old.diff(lag))
        frame = pl.DataFrame({'Date': [date(2020, 1, 31)] * 2 + [date(2020, 2, 29)], VALUE: [1., 2., 3.]})
        with self.assertRaises(ValueError):
            pd.Series(frame[VALUE].to_numpy(), index=pd.to_datetime(frame['Date'].to_list())).asfreq('1ME')
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            scope['monthly_series'](frame)
        # A longer synthetic calendar exercises missingness through both lags.
        dates = pd.date_range('2000-01-31', periods=150, freq='ME')
        values = [float(i * i) for i in range(150)]
        values[2], values[4], values[140] = None, np.nan, np.inf
        frame = pl.DataFrame({'Date': [d.date() for d in dates], VALUE: values},
                             schema={'Date': pl.Date, VALUE: pl.Float64})
        scope['series'] = scope['monthly_series'](frame)
        scope['autocorrelation_plot'] = lambda values: None
        for index in [42, 43]:
            exec(compile(self.code(index), '<synthetic exact double difference>', 'exec'), scope)
        self.frame_equal(scope['double_diff'], pd.Series(values, index=dates, dtype=float).diff(1)[1:].diff(132)[133:])

    def test_synthetic_distinct_acfs_null_nan_infinity_constant_and_short(self):
        scope = self.scope()
        for values in [[1., 2., 4., 8., 16.], [1., 2., None, 8., 16., 32.],
                       [1., 2., np.nan, 8., 16., 32.], [1., 2., np.inf, 8., 16., 32.],
                       [1., -np.inf, 4., 8., 16.], [5.] * 5, [], [1.], [1., 2.]]:
            with self.subTest(values=values):
                series = pl.Series(VALUE, values, dtype=pl.Float64)
                old = pd.Series(values, dtype=float)
                actual = [scope['overlap_autocorr'](series, lag) for lag in range(1, 8)]
                np.testing.assert_allclose(actual, [old.autocorr(lag) for lag in range(1, 8)], rtol=1e-12, atol=1e-12, equal_nan=True)
                self.plot_equal(series, scope)
        axis = RecordingAxis()
        plotting_oracle(axis)(pd.Series([1., 2., 4., 8., 16.]))
        plotted = next(args for name, args, kw in axis.calls if name == 'plot')
        self.assertEqual(plotted[0].tolist(), [1, 2, 3, 4, 5])
        self.assertEqual(plotted[1][-1], 0.)
        self.assertNotAlmostEqual(plotted[1][0], 1.)
        self.assertAlmostEqual(scope['overlap_autocorr'](pl.Series([1., 2., np.inf, 8., 16., 32.]), 4), 1.)
        # Supplying an axis preserves Pandas' absence of automatic limit calls.
        actual_axis, expected_axis = RecordingAxis(), RecordingAxis()
        scope['autocorrelation_plot']([1., 2., 4.], ax=actual_axis)
        plotting_oracle(expected_axis)(pd.Series([1., 2., 4.]), ax=expected_axis)
        self.assertEqual([c[0] for c in actual_axis.calls], [c[0] for c in expected_axis.calls])
        self.assertNotIn('set_xlim', [c[0] for c in actual_axis.calls])

    def test_intentional_positional_corrections_dates_lengths_and_lag_ranges(self):
        scope = self.scope()
        old = self.old_monthly()
        frame = self.new_monthly(scope)
        scope['autocorrelation_plot'] = lambda values: None
        exec(compile(self.code(48), '<corrected cell48>', 'exec'), scope)
        expected = old
        for lag in range(50):
            expected = expected.diff(1)[1:]
        self.frame_equal(scope['series_diff'], expected)
        self.assertEqual(len(scope['series_diff']), 3185)
        self.assertEqual(scope['series_diff']['Date'][0], frame['Date'][50])
        exec(compile(self.code(49), '<corrected cell49>', 'exec'), scope)
        self.frame_equal(scope['series_diff1'], old.diff(1)[1:])
        np.testing.assert_allclose(scope['autocorrs'], [old.diff(1)[1:].autocorr(lag) for lag in range(1, 60)], rtol=1e-12, atol=1e-12)
        self.assertEqual(len(scope['autocorrs']), 59)
        plot = next(args for name, args, kw in scope['axis'].calls if name == 'plot')
        self.assertEqual(len(plot), 1)  # Preserve implicit x positions 0–58.
        for values in [[], [1.], [1., None, 3., np.nan, np.inf], [5.] * 60]:
            with self.subTest(short_or_missing=values):
                dates = pd.date_range('2020-01-31', periods=len(values), freq='ME')
                expected = pd.Series(values, index=dates, dtype=float)
                scope['series'] = pl.DataFrame({'Date': [d.date() for d in dates], VALUE: values},
                                              schema={'Date': pl.Date, VALUE: pl.Float64})
                exec(compile(self.code(48), '<edge corrected cell48>', 'exec'), scope)
                for lag in range(50):
                    expected = expected.diff(1)[1:]
                self.frame_equal(scope['series_diff'], expected)
                exec(compile(self.code(49), '<edge corrected cell49>', 'exec'), scope)
                self.frame_equal(scope['series_diff1'], pd.Series(values, index=dates, dtype=float).diff(1)[1:])


if __name__ == '__main__':
    unittest.main()
