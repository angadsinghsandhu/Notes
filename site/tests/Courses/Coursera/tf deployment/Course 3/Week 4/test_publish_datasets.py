"""Actual wrapped MATLAB metadata parity; selected frame code only."""
import ast
import hashlib
import json
from pathlib import Path
import sys
import unittest

import numpy as np
import pandas as pd
import polars as pl
from scipy.io import loadmat

SITE = next(p for p in Path(__file__).resolve().parents if p.name == 'site')
sys.path.insert(0, str(SITE / 'scripts'))
from check_polars import read_source

FIXTURE = SITE / 'tests/fixtures/real/polars/imdb_crop_records.mat'
FIXTURE_HASH = '709850e373490be8084502701c2e2e05cedc66ab7c90cf18e409a4c40324fe8f'
SOURCE_IDS = [0, 3, 5, 6, 30, 504, 505, 506]
SCHEMA = {'dob': pl.Int32, 'photo_taken': pl.UInt16, 'full_path': pl.String,
          'gender': pl.Float64, 'name': pl.String, 'face_location': pl.List(pl.Float64),
          'face_score': pl.Float64, 'second_face_score': pl.Float64, 'celeb_id': pl.UInt16}


class PublishDatasetsTest(unittest.TestCase):
    PATH = 'Courses/Coursera/tf deployment/Course 3/Week 4/publish_datasets.py'
    HASH = '2dd607b0afd7167a970c67dafa23c11c14aea1caf4556b546ef0a86d268a8deb'

    def frame_source(self, source):
        return source.split('# dataframe\n')[1].split('# FIXME')[0]

    def count_source(self, source):
        return self.frame_source(source)

    def frame(self, values, original=False):
        code = ast.parse(self.frame_source(read_source(self.PATH, original=original)))
        code.body = [node for node in code.body if not isinstance(node, ast.Expr)]
        scope = {'values': values, 'names': list(values), 'pl': pl, 'pd': pd}
        exec(compile(code, '<selected MATLAB frame>', 'exec'), scope)
        return scope['df']

    def counts(self, frame, original=False):
        code = ast.parse(self.count_source(read_source(self.PATH, original=original)))
        expr = code.body[-1]
        self.assertIsInstance(expr, ast.Expr)
        return eval(compile(ast.Expression(expr.value), '<selected missingness>', 'eval'), {'df': frame, 'pl': pl, 'names': list(frame.columns), 'schema': SCHEMA})

    def values(self):
        root = loadmat(FIXTURE)['imdb'][0, 0]
        return {key: root[key][0] for key in root.dtype.names if key != 'celeb_names'}

    def test_polars_contract_and_exact_original_preservation(self):
        source, old = read_source(self.PATH), read_source(self.PATH, original=True)
        self.assertEqual(hashlib.sha256(old.encode()).hexdigest(), self.HASH)
        self.assertIn('import polars as pl', source)
        self.assertNotIn('import pandas', source)
        ast.parse(source)
        prefix = '# dataframe\n'
        self.assertEqual(source.split(prefix)[0].replace('import polars as pl', 'import pandas as pd'), old.split(prefix)[0])
        self.assertEqual(source.split('# FIXME')[1], old.split('# FIXME')[1])
        self.assertEqual(source.count('FIXME'), old.count('FIXME'))
        # The standalone exploration's misassigned fields are preserved, not executed.
        self.assertIn('gender = root["dob"][0]', source)

    def test_actual_default_wrappers_schema_records_and_missingness(self):
        self.assertEqual(hashlib.sha256(FIXTURE.read_bytes()).hexdigest(), FIXTURE_HASH)
        provenance = json.loads((FIXTURE.parent / 'provenance.json').read_text())
        record = next(r for r in provenance['inputs'] if r['filename'] == FIXTURE.name)
        self.assertEqual(record['source_ids_zero_based'], SOURCE_IDS)
        self.assertEqual(record['sha256'], FIXTURE_HASH)
        self.assertEqual(record['parent_sha256'], 'be67a7d84df5f90893884cd7f206c8c935ceeaa2afc09b6a96076fd7f982a035')
        self.assertEqual(record['parent_payload_range_inclusive'], [6989163520, 7012099163])
        self.assertEqual(record['recursive_comparison_count'], 20329)
        meta = loadmat(FIXTURE)['imdb']
        self.assertEqual(meta.shape, (1, 1))
        root = meta[0, 0]
        self.assertEqual(root['celeb_names'].shape, (1, 20284))
        for key in SCHEMA:
            self.assertEqual(root[key].shape, (1, 8))
        self.assertEqual(root['full_path'][0, 0].shape, (1,))
        self.assertEqual(root['face_location'][0, 0].shape, (1, 4))
        self.assertEqual(root['face_location'][0, 4].dtype, np.dtype('uint16'))
        values = self.values()
        old, new = self.frame(values, True), self.frame(values)
        self.assertIsInstance(new, pl.DataFrame, 'metadata frame still uses Pandas')
        self.assertEqual(new.shape, (8, 9))
        self.assertEqual(new.schema, SCHEMA)
        self.assertEqual(new.columns, list(old.columns))
        for key in SCHEMA:
            expected = old[key].tolist()
            if key in ('full_path', 'name'):
                expected = [str(v[0]) for v in expected]
                self.assertEqual(new[key].to_list(), expected)
            elif key == 'face_location':
                np.testing.assert_array_equal(new[key].to_list(), [v[0].astype(float) for v in expected])
            else:
                np.testing.assert_array_equal(new[key].to_numpy(), old[key].to_numpy())
        np.testing.assert_array_equal(new['gender'].is_nan().to_numpy(), pd.isna(old['gender']))
        np.testing.assert_array_equal(new['second_face_score'].is_nan().to_numpy(), pd.isna(old['second_face_score']))
        self.assertEqual(new.null_count().row(0), (0,) * 9)
        self.assertEqual(self.counts(new).row(0), tuple(self.counts(old, True)))
        self.assertEqual(new['second_face_score'].is_nan().sum(), 5)
        self.assertEqual(new['gender'].is_nan().sum(), 3)
        self.assertEqual(new['face_score'].to_list()[4:6], [-np.inf, -np.inf])

    def test_synthetic_null_nan_and_empty_typed_metadata(self):
        self.assertIn('import polars as pl', read_source(self.PATH))
        values = self.values()
        for key in ('full_path', 'name', 'face_location'):
            values[key][0] = None
        for key in ('gender', 'face_score', 'second_face_score'):
            values[key] = values[key].astype(object)
            values[key][0], values[key][1] = None, np.nan
        old, new = self.frame(values, True), self.frame(values)
        self.assertEqual(new.schema, SCHEMA)
        for key in ('full_path', 'name', 'face_location'):
            self.assertIsNone(new[key][0])
        self.assertEqual(self.counts(new).row(0), tuple(self.counts(old, True)))
        for key in ('gender', 'face_score', 'second_face_score'):
            expected = pd.isna(old[key]).to_numpy()
            np.testing.assert_array_equal((new[key].is_null() | new[key].is_nan()).to_numpy(), expected)
            self.assertIsNone(new[key][0])
            self.assertTrue(np.isnan(new[key][1]))
        empty = self.frame({key: value[:0] for key, value in values.items()})
        self.assertEqual(empty.shape, (0, 9))
        self.assertEqual(empty.schema, SCHEMA)
        self.assertEqual(self.counts(empty).row(0), (0,) * 9)


if __name__ == '__main__':
    unittest.main()
