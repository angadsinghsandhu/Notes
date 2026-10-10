"""Notebook metadata parity and selected builder readers; TODOs stay unfilled."""
import ast
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest

import nbformat
import numpy as np
import pandas as pd
import polars as pl

SITE = next(p for p in Path(__file__).resolve().parents if p.name == 'site')
sys.path.insert(0, str(SITE / 'scripts'))
from check_polars import cell_source, read_source

MIRROR = SITE / 'tests/Courses/Coursera/tf deployment/Course 3/Week 4/test_publish_datasets.py'
spec = importlib.util.spec_from_file_location('metadata_source_mirror', MIRROR)
metadata = importlib.util.module_from_spec(spec)
spec.loader.exec_module(metadata)


class TFDSWeek4ExerciseTest(metadata.PublishDatasetsTest):
    PATH = 'Courses/Coursera/Deep Learning AI course/TensorFlow Deployment/Course 3 - TensorFlow Datasets/Week 4/Exercises/TFDS_Week4_Exercise.ipynb'
    HASH = '59140dc0281b017b0e0911f00a3b8063fd96f6136567819871ca4f81716b39b5'

    def frame_source(self, source):
        return cell_source(source, 30)

    def count_source(self, source):
        return cell_source(source, 32)

    def test_polars_contract_and_exact_original_preservation(self):
        source, old = read_source(self.PATH), read_source(self.PATH, original=True)
        self.assertEqual(hashlib.sha256(old.encode()).hexdigest(), self.HASH)
        self.assertIn('import polars as pl', cell_source(source, 5))
        self.assertNotIn('import pandas', source)
        before, after = json.loads(old), json.loads(source)
        nbformat.validate(after)
        self.assertEqual(len(before['cells']), len(after['cells']))
        self.assertEqual({k: v for k, v in before.items() if k != 'cells'}, {k: v for k, v in after.items() if k != 'cells'})
        for i, (a, b) in enumerate(zip(before['cells'], after['cells'])):
            if i in [5, 29, 30, 31, 32, 43]:
                self.assertEqual({k: v for k, v in a.items() if k != 'source'}, {k: v for k, v in b.items() if k != 'source'})
            else:
                self.assertEqual(a, b)
        for token in ['# YOUR CODE HERE', '# Create a', '# Put the name', '# EXERCISE:', 'Licensed under the Apache License']:
            self.assertEqual(source.count(token), old.count(token))
        self.assertEqual(cell_source(source, 43).split('  def _generate_examples')[0], cell_source(old, 43).split('  def _generate_examples')[0])
        for i in [30, 32]:
            ast.parse(cell_source(source, i))
        self.assertIn('is_null()', cell_source(source, 32))
        self.assertIn('is_nan()', cell_source(source, 32))

    def builder_records(self, values, original=False):
        """Complete only metadata TODOs in test memory; no builder or image calls."""
        source = cell_source(read_source(self.PATH, original=original), 43)
        text = source.split('  def _generate_examples(self, image_dir, metadata):\n')[1]
        text = text.split('      # Get the image shape')[0]
        # All original exercise assignments remain incomplete on disk.
        imports = ('pd', pd) if original else ('pl', pl)
        text = text.replace(f'    {imports[0]} = # YOUR CODE HERE', f'    {imports[0]} = tabular')
        names = {'dobs': 'dob', 'genders': 'gender', 'face_locations': 'face_location',
                 'photo_taken_years': 'photo_taken', 'face_scores': 'face_score',
                 'second_face_scores': 'second_face_score', 'celeb_id': 'celeb_id'}
        frame = self.frame(values, original)
        for name, key in names.items():
            text = text.replace(f'    {name} = # YOUR CODE HERE', f'    {name} = completed["{key}"]')
        text = text.replace('    df = # YOUR CODE HERE', '    df = completed_frame', 1)
        # First exercise filter is face_score>1; the remaining exercise is identity
        # here so meaningful second-face absence is not silently discarded.
        text = text.replace('    df = # YOUR CODE HERE', "    df = df[df['face_scores'] > 1.0]" if original else "    df = df.filter(pl.col('face_scores').is_not_null() & ~pl.col('face_scores').is_nan() & (pl.col('face_scores') > 1.0))", 1)
        text = text.replace('    df = # YOUR CODE HERE', '    df = df', 1)
        text = text.replace('    df.genders = # YOUR CODE HERE', "    df.genders = df.genders.astype(int)") if original else text.replace('    df = # YOUR CODE HERE', "    df = df.with_columns(pl.col('genders').cast(pl.Int64))", 1)
        rename = {'full_path': 'image_names', 'dob': 'dobs', 'gender': 'genders',
                  'face_location': 'face_locations', 'photo_taken': 'photo_taken_years',
                  'face_score': 'face_scores', 'second_face_score': 'second_face_scores', 'celeb_id': 'celeb_ids'}
        built = frame.rename(columns=rename) if original else frame.rename(rename)
        # Execute actual string extraction, missing-gender filter and row readers.
        bbox_code = source.split('      # Normalize the bounding boxes')[1].split('      # Yield a feature dictionary')[0]
        bbox_code = bbox_code[bbox_code.index('      bbox ='):]
        text += bbox_code
        text += "      records.append((filename, gender, dob, photo_taken, face_score, second_face_score, celeb_id, bbox))\n" if original else "      records.append((filename, gender, dob, photo_taken, face_score, second_face_score, celeb_id, bbox))\n"
        text = '\n'.join(line[4:] if line.startswith('    ') else line for line in text.splitlines())
        def record_bbox(box, width, height):
            self.assertEqual((width, height), (320, 240))
            return list(box)

        scope = {'self': SimpleNamespace(_get_bounding_box_values=record_bbox),
                 'image_width': 320, 'image_height': 240, 'tabular': imports[1], 'completed': {k: frame[k].tolist() if original else frame[k].to_list() for k in values},
                 'completed_frame': built,
                 'os': os, 'image_dir': '/metadata-only', '_DATASET_ROOT_DIR': 'imdb_crop', 'records': []}
        # Keep original numeric/scalar wrappers rather than changing loadmat options.
        root = np.empty((1, 1), dtype=[(k, object) for k in values])
        for k, v in values.items():
            root[k][0, 0] = np.array([v])
        scope['metadata'] = root
        exec(compile(ast.parse(text), '<selected exercise readers, test-memory TODOs>', 'exec'), scope)
        return scope

    def test_builder_named_rows_normalized_readers_unknown_gender_before_cast(self):
        source = cell_source(read_source(self.PATH), 43)
        self.assertIn('for row in df.iter_rows(named=True):', source)
        self.assertNotIn('iterrows', source)
        self.assertIn('pl = # YOUR CODE HERE', source)
        self.assertIn("row['image_names'])", source)
        self.assertIn("row['face_locations'],", source)
        self.assertIn("pl.col('genders').is_null() | pl.col('genders').is_nan()", source)
        values = self.values()
        old, new = self.builder_records(values, True), self.builder_records(values)
        self.assertEqual(len(new['records']), 4)
        self.assertEqual(new['image_names'], [str(v[0]) for v in values['full_path']])
        self.assertEqual(new['df'].schema['genders'], pl.Int64)
        self.assertEqual(new['df']['genders'].to_list(), [1, 1, 0, 0])
        for a, b in zip(old['records'], new['records']):
            self.assertEqual(a[0], b[0])
            np.testing.assert_array_equal(a[1:7], b[1:7])
            np.testing.assert_array_equal(a[7], b[7])
        self.assertEqual(sum(np.isnan(row[5]) for row in new['records']), 2)
        # Synthetic null/NaN gender removed before strict integer casting.
        for key in ['gender', 'face_score']:
            values[key] = values[key].astype(object)
        values['gender'][0], values['gender'][1] = None, np.nan
        values['face_score'][2], values['face_score'][3] = np.nan, np.inf
        edge = self.builder_records(values)
        self.assertEqual(edge['df']['genders'].to_list(), [0])
        self.assertTrue(np.isposinf(edge['records'][0][4]))
        self.assertTrue(np.isnan(edge['records'][0][5]))
        self.assertEqual(self.builder_records({k: v[:0] for k, v in values.items()})['records'], [])


if __name__ == '__main__':
    unittest.main()
