"""Run explicit archive parity tests without importing whole course programs."""
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
DELTAS = ROOT / 'site/tests/fixtures/real/polars/source-deltas.json'
TEST_FILES = [
    'site/tests/scripts/test_check_polars.py',
    'site/tests/scripts/test_polars_tf_support.py',
    'site/tests/Books/Programming PyTorch for Deep Learning - Ian Pointer/Chapter 2 - Image Clasification with Pytorch/test_download.py',
    'site/tests/Courses/Coursera/Deep Learning AI course/Advanced TensorFlow/Extending Keras/Week 4 - Models and Callbacks/test_ExploringCallbacks.py',
    'site/tests/Courses/Coursera/tf deployment/Course 3/Week 2/test_2_input_pipelines_custom.py',
    'site/tests/Interview/Applied Science/breadth/test_11_practical.py',
    'site/tests/Courses/Coursera/Deep Learning AI course/TensorFlow Deployment/Course 3 - TensorFlow Datasets/Week 2/Examples/test_data.py',
    'site/tests/Courses/Coursera/Deep Learning AI course/TensorFlow Deployment/Course 3 - TensorFlow Datasets/Week 2/Examples/test_feature_columns.py',
    'site/tests/Courses/Coursera/Deep Learning AI course/TensorFlow Deployment/Course 3 - TensorFlow Datasets/Week 2/Exercises/test_TFDS_Week2_Exercise.py',
    'site/tests/Courses/Coursera/tf deployment/Course 3/Week 2/test_1_input_pipelines.py',
]


def reverse_deltas(content, record):
    """Reject unapproved bytes, then reconstruct the exact pre-conversion file."""
    if hashlib.sha256(content).hexdigest() != record['converted_sha256']:
        raise ValueError(f"converted hash mismatch: {record['path']}")
    for delta in reversed(record['replacements']):
        old, new = delta['old'].encode('utf-8'), delta['new'].encode('utf-8')
        if not new or content.count(new) != 1:
            raise ValueError(f"delta must be unique: {record['path']}")
        content = content.replace(new, old, 1)
    if hashlib.sha256(content).hexdigest() != record['original_sha256']:
        raise ValueError(f"original hash mismatch: {record['path']}")
    return content


def read_source(path, *, original=False):
    target = (ROOT / path).resolve()
    if not target.is_relative_to(ROOT):
        raise ValueError('source path outside repository')
    content = target.read_bytes()
    if original:
        records = json.loads(DELTAS.read_text(encoding='utf-8'))['files']
        matches = [record for record in records if record['path'] == path]
        if len(matches) != 1:
            raise ValueError(f'expected one original record: {path}')
        content = reverse_deltas(content, matches[0])
    return content.decode('utf-8')


def cell_source(notebook, index):
    source = json.loads(notebook)['cells'][index]['source']
    return ''.join(source) if isinstance(source, list) else source


def selected_code(source, indices):
    """Compile only caller-selected top-level nodes; callers own their boundary."""
    tree = ast.parse(source)
    selected = ast.Module(body=[tree.body[index] for index in indices], type_ignores=[])
    return compile(selected, '<selected archive statements>', 'exec')


def selected_expression(source, index):
    node = ast.parse(source).body[index]
    if not isinstance(node, ast.Expr):
        raise ValueError('selected node is not an expression')
    return compile(ast.Expression(node.value), '<selected archive expression>', 'eval')


def load_suite(paths):
    paths = [Path(path) for path in paths]
    names = [path.stem for path in paths]
    if len(names) != len(set(names)):
        raise ValueError('duplicate parity test basenames')
    suite = unittest.TestSuite()
    for path in paths:
        spec = importlib.util.spec_from_file_location(path.stem, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(module))
    return suite


def main(paths=None):
    if sys.prefix == sys.base_prefix:
        print('Activate the isolated Polars verification venv before running parity checks.', file=sys.stderr)
        return 1
    suite = load_suite(paths if paths is not None else [ROOT / path for path in TEST_FILES])
    return 0 if unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(main([ROOT / path for path in sys.argv[1:]] or None))
