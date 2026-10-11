"""Full real pageviews CPU parity; never import cuDF or execute GPU cells."""
import ast
import csv
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

import nbformat
import numpy as np
import pandas as pd
import polars as pl

SITE = next(parent for parent in Path(__file__).resolve().parents if parent.name == 'site')
sys.path.insert(0, str(SITE / 'scripts'))
from check_polars import ROOT, cell_source, read_source, selected_expression

PATH = 'Tutorials/GPU/nv-gpu-workshop/6.0_cuDF.ipynb'
DATA = ROOT / 'Tutorials/GPU/nv-gpu-workshop/pageviews_small.csv'
FIXTURES = SITE / 'tests/fixtures/real/polars'
ORIGINAL_HASH = '9240ecd16cf5f58cbc4b8c64d42fc3ff2187206d7aecbbc86836a6f330c934f1'
DATA_HASH = 'ee688aedeace7a623213194ba0c8754c61c4dc6cb2ff5cb55f322dd02f2fc2ff'
COLUMNS = ['en.m', 'Article_51', '1', '0']
# Baseline Pandas default tokens, also exercised through the original reader below.
NA_TOKENS = ['', '#N/A', '#N/A N/A', '#NA', '-1.#IND', '-1.#QNAN',
             '-NaN', '-nan', '1.#IND', '1.#QNAN', '<NA>', 'N/A', 'NA',
             'NULL', 'NaN', 'None', 'n/a', 'nan', 'null']


def cpu_read(notebook, path):
    """Only CPU imports and cell 5, adapting the CSV path in test memory."""
    scope = {}
    exec(compile(cell_source(notebook, 4), '<CPU import cell 4>', 'exec'), scope)
    tree = ast.parse(cell_source(notebook, 5))
    read = tree.body[0].value
    assert isinstance(read, ast.Call) and read.func.attr == 'read_csv'
    assert isinstance(read.args[0], ast.Constant)
    read.args[0].value = str(path)
    exec(compile(ast.Module(body=[tree.body[0]], type_ignores=[]),
                 '<CPU read cell 5; test-memory path only>', 'exec'), scope)
    head = eval(selected_expression(cell_source(notebook, 5), 1), scope)
    return scope['df'], head


class CuDFCPUTest(unittest.TestCase):
    def assert_parity(self, before, after):
        self.assertIsInstance(after, pl.DataFrame, 'CPU read still returns Pandas')
        self.assertEqual(after.columns, list(before.columns))
        self.assertEqual(after.shape, before.shape)
        for name in after.columns:
            expected, actual = before[name], after[name]
            mask = expected.isna().to_numpy()
            np.testing.assert_array_equal(actual.is_null().to_numpy(), mask)
            values = actual.to_numpy()
            if actual.dtype.is_numeric():
                np.testing.assert_allclose(values, expected.to_numpy(), equal_nan=True)
                if actual.dtype.is_float():
                    np.testing.assert_array_equal(actual.is_nan().fill_null(False).to_numpy(),
                                                  np.zeros(len(actual), dtype=bool))
            else:
                np.testing.assert_array_equal(values[~mask], expected.to_numpy()[~mask])

    def test_polars_cpu_contract_and_exact_dependent_path(self):
        notebook = read_source(PATH)
        self.assertEqual(cell_source(notebook, 4), 'import polars as pl\n')
        read = cell_source(notebook, 5)
        self.assertIn('pl.read_csv(', read)
        self.assertNotIn('pd.', read)
        tree = ast.parse(read)
        call = tree.body[0].value
        self.assertEqual(call.args[0].value, './pageviews_small.csv')
        keywords = {item.arg: ast.literal_eval(item.value) for item in call.keywords}
        self.assertEqual(keywords, {'separator': ' ', 'infer_schema_length': None,
                                    'null_values': NA_TOKENS})
        self.assertEqual(cell_source(notebook, 6),
                         'pageviews = cudf.read_csv("./pageviews_small.csv", sep=" ")\npageviews.head()\n')
        self.assertFalse((DATA.parent / 'data/pageviews_small.csv').exists())
        self.assertIn('first physical row', cell_source(notebook, 3))
        self.assertIn('Polars', cell_source(notebook, 3))
        for index in (4, 5, 6):
            compile(cell_source(notebook, index), f'<changed cell {index}>', 'exec')

    def test_full_actual_data_values_order_dtypes_null_and_nan_masks(self):
        raw = DATA.read_bytes()
        self.assertEqual(len(raw), 34132641)
        self.assertEqual(hashlib.sha256(raw).hexdigest(), DATA_HASH)
        self.assertEqual(len(raw.splitlines()), 1119000)
        original = read_source(PATH, original=True)
        self.assertEqual(hashlib.sha256(original.encode()).hexdigest(), ORIGINAL_HASH)
        before, old_head = cpu_read(original, DATA)
        after, new_head = cpu_read(read_source(PATH), DATA)
        self.assert_parity(before, after)
        self.assert_parity(old_head, new_head)
        self.assertEqual(after.shape, (1118999, 4))
        self.assertEqual(after.columns, COLUMNS)
        self.assertEqual([str(dtype) for dtype in before.dtypes], ['str', 'str', 'int64', 'int64'])
        self.assertEqual(after.dtypes, [pl.String, pl.String, pl.Int64, pl.Int64])
        self.assertEqual(after.null_count().row(0), (0, 12, 0, 0))
        self.assertEqual(before.isna().sum().tolist(), [0, 12, 0, 0])
        self.assertEqual(after.row(0), ('ja', 'エレファモン', 1, 0))
        self.assertEqual(after.row(-1), ('pt', 'Fabián_Chávez', 1, 0))
        self.assertTrue(before['Article_51'].isna().iloc[754611])
        self.assertIsNone(after['Article_51'][754611])
        # The measured real discrepancy is the literal page title None at physical line 754613.
        self.assertEqual(raw.splitlines()[754612], b'fr.m None 1 0')
        for name in ('1', '0'):
            self.assertEqual(after[name].to_numpy().dtype, before[name].to_numpy().dtype)
            self.assertFalse(np.isnan(after[name].to_numpy()).any())

    def test_real_prefix_exact_first_257_physical_lines_and_provenance(self):
        raw = DATA.read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), DATA_HASH)
        fixture = FIXTURES / 'pageviews_head.csv'
        self.assertEqual(fixture.read_bytes(), b''.join(raw.splitlines(keepends=True)[:257]))
        self.assertEqual(len(fixture.read_bytes().splitlines()), 257)
        record, = [entry for entry in json.loads((FIXTURES / 'provenance.json').read_text())['inputs']
                   if entry['filename'] == fixture.name]
        self.assertEqual(record['sha256'], hashlib.sha256(fixture.read_bytes()).hexdigest())
        self.assertEqual(record['parent_sha256'], DATA_HASH)
        before, _ = cpu_read(read_source(PATH, original=True), fixture)
        after, _ = cpu_read(read_source(PATH), fixture)
        self.assert_parity(before, after)
        self.assertEqual(after.shape, (256, 4))
        self.assertEqual(after.columns, COLUMNS)

    def test_synthetic_default_na_quoted_empty_unicode_numeric_missing_and_header(self):
        original, converted = read_source(PATH, original=True), read_source(PATH)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'synthetic.csv'
            with path.open('w', encoding='utf-8', newline='') as stream:
                writer = csv.writer(stream, delimiter=' ')
                writer.writerow(['en.m', 'Article_51', '1', '0'])
                writer.writerow(['ja', 'エレファモン', 1, 0])
                for token in NA_TOKENS:
                    writer.writerow(['fr', token, 2, 0])
                stream.write('fr "" 2 0\n')
                writer.writerow(['pt', 'Fabián_Chávez', 'NaN', 'NULL'])
                writer.writerow(['en', 'not_missing', 4, 0])
            before, _ = cpu_read(original, path)
            after, _ = cpu_read(converted, path)
            self.assert_parity(before, after)
            self.assertEqual(after.columns, COLUMNS)
            self.assertEqual(after.height, len(NA_TOKENS) + 4)
            self.assertEqual(after['Article_51'].null_count(), len(NA_TOKENS) + 1)
            self.assertEqual(after['1'].null_count(), 1)
            self.assertEqual(after['0'].null_count(), 1)
            np.testing.assert_array_equal(after['1'].to_numpy().dtype, before['1'].to_numpy().dtype)
            path.write_text('en.m Article_51 1 0\n', encoding='utf-8')
            before, _ = cpu_read(original, path)
            after, _ = cpu_read(converted, path)
            self.assert_parity(before, after)
            self.assertEqual(after.shape, (0, 4))
            path.write_text('', encoding='utf-8')
            for notebook, error in ((original, pd.errors.EmptyDataError),
                                    (converted, pl.exceptions.NoDataError)):
                with self.assertRaises(error):
                    cpu_read(notebook, path)
            for notebook in (original, converted):
                with self.assertRaises(FileNotFoundError):
                    cpu_read(notebook, Path(directory) / 'missing.csv')

    def test_original_reversal_preserves_all_other_cells_gpu_history_and_repairs(self):
        original = read_source(PATH, original=True)
        converted = read_source(PATH)
        old, new = json.loads(original), json.loads(converted)
        nbformat.validate(new)
        self.assertEqual(len(old['cells']), len(new['cells']))
        for index, (left, right) in enumerate(zip(old['cells'], new['cells'])):
            if index in (3, 4, 5, 6):
                self.assertEqual({k: v for k, v in left.items() if k != 'source'},
                                 {k: v for k, v in right.items() if k != 'source'})
            else:
                self.assertEqual(left, right, f'unapproved cell {index}')
        self.assertEqual({k: v for k, v in old.items() if k != 'cells'},
                         {k: v for k, v in new.items() if k != 'cells'})
        self.assertEqual(cell_source(converted, 6),
                         cell_source(original, 6).replace('./data/pageviews_small.csv',
                                                          './pageviews_small.csv'))
        for index in (0, 15, 29):
            self.assertEqual(cell_source(converted, index), cell_source(original, index))
        self.assertEqual(hashlib.sha256(original.encode()).hexdigest(), ORIGINAL_HASH)


if __name__ == '__main__':
    unittest.main()
