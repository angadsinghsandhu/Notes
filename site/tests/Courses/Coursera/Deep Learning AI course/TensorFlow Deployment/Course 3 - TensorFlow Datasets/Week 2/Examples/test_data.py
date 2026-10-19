"""Synthetic Titanic column boundary only; authentic Titanic bytes unavailable."""
import ast
import hashlib
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest

import nbformat
import numpy as np
import pandas as pd
import polars as pl

SITE = next(parent for parent in Path(__file__).resolve().parents if parent.name == 'site')
sys.path.insert(0, str(SITE / 'scripts'))
from check_polars import cell_source, read_source, selected_code

PATH = 'Courses/Coursera/Deep Learning AI course/TensorFlow Deployment/Course 3 - TensorFlow Datasets/Week 2/Examples/data.ipynb'
ORIGINAL_HASH = '1e8902a0116e83a44dba7260131a4a0ea08ce156bb864bf8e3fa3cfbdf110597'


class DataTest(unittest.TestCase):
    def test_polars_contract_and_changed_code_syntax(self):
        source = read_source(PATH)
        self.assertIn('import polars as pl', cell_source(source, 9))
        self.assertNotIn('import pandas', cell_source(source, 9))
        self.assertIn('Polars', cell_source(source, 74))
        self.assertIn('https://www.tensorflow.org/tutorials/load_data/pandas_dataframe',
                      cell_source(source, 74))
        for i in (9, 76, 78):
            ast.parse(cell_source(source, i))

    def test_synthetic_schema_arrays_are_recorded_without_model_execution(self):
        original = read_source(PATH, original=True)
        source = read_source(PATH)
        self.assertEqual(hashlib.sha256(original.encode()).hexdigest(), ORIGINAL_HASH)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'synthetic_titanic.csv'
            path.write_text('survived,sex,age,n_siblings_spouses,parch,fare,class,deck,embark_town,alone\n'
                            '0,male,22.0,1,0,7.25,Third,unknown,Southampton,n\n'
                            '1,female,38.0,1,0,71.2833,First,C,Cherbourg,n\n'
                            '1,female,,0,0,7.925,Third,unknown,Southampton,y\n')
            recorded = []
            for notebook in (original, source):
                arrays = []
                tf = SimpleNamespace(data=SimpleNamespace(Dataset=SimpleNamespace(
                    from_tensor_slices=lambda value: arrays.append(value))))
                scope = {'pd': pd, 'pl': pl, 'tf': tf, 'titanic_file': str(path)}
                exec(selected_code(cell_source(notebook, 76), [0]), scope)
                exec(selected_code(cell_source(notebook, 78), [0]), scope)
                # The oracle records Series; the converted boundary must pass actual arrays.
                if notebook == source:
                    self.assertIsInstance(scope['df'], pl.DataFrame)
                    self.assertTrue(all(isinstance(value, np.ndarray) for value in arrays[0].values()))
                recorded.append({key: np.asarray(value) for key, value in arrays[0].items()})
        before, after = recorded
        self.assertEqual(list(after), list(before))
        self.assertIn('survived', after, 'raw dictionary demonstration retains every column')
        self.assertNotIn('index', after)
        for key in before:
            if before[key].dtype.kind in 'biuf':
                self.assertEqual(after[key].dtype, before[key].dtype)
                np.testing.assert_allclose(after[key], before[key], equal_nan=True)
            else:
                self.assertIn(after[key].dtype.kind, 'OU')
                np.testing.assert_array_equal(after[key], before[key])
        self.assertTrue(np.isnan(after['age'][2]))

    def test_exact_notebook_preservation(self):
        old = json.loads(read_source(PATH, original=True))
        new = json.loads(read_source(PATH))
        nbformat.validate(new)
        self.assertEqual(len(old['cells']), len(new['cells']))
        for i, (before, after) in enumerate(zip(old['cells'], new['cells'])):
            if i in (9, 74, 76, 78):
                self.assertEqual({k: v for k, v in before.items() if k != 'source'},
                                 {k: v for k, v in after.items() if k != 'source'})
            else:
                self.assertEqual(before, after, f'unapproved cell {i}')
        self.assertEqual({k: v for k, v in old.items() if k != 'cells'},
                         {k: v for k, v in new.items() if k != 'cells'})


if __name__ == '__main__':
    unittest.main()
