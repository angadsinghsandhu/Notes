"""Stdlib archive boundary loading and exact original reconstruction checks."""
import ast
from contextlib import redirect_stderr
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

HELPER = Path(__file__).resolve().parents[2] / 'scripts/check_polars.py'


class CheckPolarsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if HELPER.exists():
            spec = importlib.util.spec_from_file_location('check_polars', HELPER)
            cls.helper = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(cls.helper)

    def setUp(self):
        self.assertTrue(HELPER.exists(), 'shared stdlib check_polars helper is missing')

    def test_exact_reversal_preserves_unrelated_bytes_and_rejects_tamper(self):
        old = b'prefix\r\nold source\nuntouched output \xc3\xa9\n'
        new = old.replace(b'old source', b'new source')
        record = {'path': 'example.py', 'original_sha256': hashlib.sha256(old).hexdigest(),
                  'converted_sha256': hashlib.sha256(new).hexdigest(),
                  'replacements': [{'old': 'old source', 'new': 'new source', 'intent': 'source'}]}
        self.assertEqual(self.helper.reverse_deltas(new, record), old)
        for altered in [new + b'!', new.replace(b'output', b'OUTPUT')]:
            with self.assertRaisesRegex(ValueError, 'converted hash'):
                self.helper.reverse_deltas(altered, record)
        record['original_sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'original hash'):
            self.helper.reverse_deltas(new, record)

    def test_ambiguous_or_missing_delta_fails(self):
        for current in [b'new new', b'absent']:
            record = {'path': 'example.py', 'original_sha256': '0' * 64,
                      'converted_sha256': hashlib.sha256(current).hexdigest(),
                      'replacements': [{'old': 'old', 'new': 'new'}]}
            with self.assertRaisesRegex(ValueError, 'unique'):
                self.helper.reverse_deltas(current, record)

    def test_source_loading_exact_path_and_unknown_original_rejected(self):
        self.assertEqual(self.helper.read_source('site/tests/requirements-polars.txt'),
                         (HELPER.parents[2] / 'site/tests/requirements-polars.txt').read_text())
        with self.assertRaisesRegex(ValueError, 'original record'):
            self.helper.read_source('site/tests/requirements-polars.txt', original=True)
        with self.assertRaisesRegex(ValueError, 'outside repository'):
            self.helper.read_source('../outside.py')

    def test_selected_statements_do_not_execute_other_imports_or_side_effects(self):
        source = 'import package_that_must_not_be_imported\nraise RuntimeError("side effect")\nvalue = 7\nvalue + 1\n'
        scope = {}
        exec(self.helper.selected_code(source, [2]), scope)
        self.assertEqual(scope['value'], 7)
        self.assertNotIn('package_that_must_not_be_imported', scope)
        self.assertEqual(eval(self.helper.selected_expression(source, 3), scope), 8)
        with self.assertRaises(IndexError):
            self.helper.selected_code(source, [7])
        with self.assertRaisesRegex(ValueError, 'expression'):
            self.helper.selected_expression(source, 2)

    def test_notebook_cell_source_preserves_string_and_list_representation(self):
        notebook = json.dumps({'cells': [{'source': ['a\n', 'b']}, {'source': 'c'}]})
        self.assertEqual(self.helper.cell_source(notebook, 0), 'a\nb')
        self.assertEqual(self.helper.cell_source(notebook, 1), 'c')

    def test_explicit_runner_rejects_duplicate_names_and_propagates_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            paths = [root / 'a/test_same.py', root / 'b/test_same.py']
            for path in paths:
                path.parent.mkdir()
                path.write_text('import unittest\nclass Test(unittest.TestCase):\n def test_bad(self): self.fail("intentional failure")\n')
            with self.assertRaisesRegex(ValueError, 'duplicate'):
                self.helper.load_suite(paths)
            suite = self.helper.load_suite(paths[:1])
            result = unittest.TestResult()
            suite.run(result)
            self.assertEqual(len(result.failures), 1)
            self.assertFalse(result.wasSuccessful())
            for expected in [1, 0]:
                if expected == 0:
                    paths[0].write_text('import unittest\nclass Test(unittest.TestCase):\n def test_ok(self): self.assertTrue(True)\n')
                completed = subprocess.run([sys.executable, '-B', str(HELPER), str(paths[0])],
                                           capture_output=True, text=True)
                self.assertEqual(completed.returncode, expected, completed.stderr)

    def test_batch_mirrors_are_registered_explicitly(self):
        self.assertEqual(self.helper.TEST_FILES, [
            'site/tests/scripts/test_check_polars.py',
            'site/tests/Books/Programming PyTorch for Deep Learning - Ian Pointer/Chapter 2 - Image Clasification with Pytorch/test_download.py',
            'site/tests/Courses/Coursera/Deep Learning AI course/Advanced TensorFlow/Extending Keras/Week 4 - Models and Callbacks/test_ExploringCallbacks.py',
            'site/tests/Courses/Coursera/tf deployment/Course 3/Week 2/test_2_input_pipelines_custom.py',
            'site/tests/Interview/Applied Science/breadth/test_11_practical.py',
            'site/tests/Courses/Coursera/Deep Learning AI course/TensorFlow Deployment/Course 3 - TensorFlow Datasets/Week 2/Examples/test_data.py',
            'site/tests/Courses/Coursera/Deep Learning AI course/TensorFlow Deployment/Course 3 - TensorFlow Datasets/Week 2/Examples/test_feature_columns.py',
            'site/tests/Courses/Coursera/Deep Learning AI course/TensorFlow Deployment/Course 3 - TensorFlow Datasets/Week 2/Exercises/test_TFDS_Week2_Exercise.py',
            'site/tests/Courses/Coursera/tf deployment/Course 3/Week 2/test_1_input_pipelines.py',
        ])

    def test_isolated_environment_required_with_raw_nonzero_exit(self):
        diagnostics = io.StringIO()
        with patch.object(self.helper.sys, 'prefix', sys.base_prefix), redirect_stderr(diagnostics):
            self.assertEqual(self.helper.main([]), 1)
        self.assertIn('isolated Polars verification venv', diagnostics.getvalue())
        completed = subprocess.run([sys._base_executable, '-B', str(HELPER)],
                                   capture_output=True, text=True)
        self.assertEqual(completed.returncode, 1)
        self.assertIn('isolated Polars verification venv', completed.stderr)
        self.assertEqual(completed.stdout, '')


if __name__ == '__main__':
    unittest.main()
