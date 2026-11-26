"""Run the LRU cache through its pinned bounded adapter."""

from pathlib import Path
from unittest import TestCase

from scripts.curriculum import _ENROLLED
from scripts.curriculum_evidence import array, digest, integer, text
from scripts.curriculum_trace import JsonValue, TraceRun, run_enrolled

_KEY = (146, "linked-recency")
_SOURCE = Path("content/leetcode/problems/146/solutions.py")


class LruCacheTest(TestCase):
    def run_cache(self, case: JsonValue) -> TraceRun:
        self.assertIn(_KEY, _ENROLLED, "the LRU cache has no reviewed enrollment")
        enrollment = _ENROLLED[_KEY]
        source = _SOURCE.read_bytes()
        self.assertEqual(digest(source), enrollment.sha256)
        run = run_enrolled(source, enrollment.adapter, case)
        enrollment.verify(case, run)
        self.assertEqual(run.post_state, case)
        lines = source.decode().splitlines()
        statements = {
            "get": "result = cache.get(key)",
            "put": 'evicted = cache.put(key, operation["value"])',
        }
        for frame in run.frames:
            step = text(frame["stepId"], "step ID").split("-")[0]
            (line,) = array(frame["codeLines"], "code lines")
            self.assertEqual(
                lines[integer(line, 1, len(lines), "line") - 1].strip(),
                statements[step],
            )
        return run

    def test_overwrite_refreshes_oldest_before_eviction(self) -> None:
        case: JsonValue = {
            "capacity": 2,
            "operations": [
                {"op": "put", "key": 1, "value": 10},
                {"op": "put", "key": 2, "value": 20},
                {"op": "put", "key": 1, "value": 11},
                {"op": "put", "key": 3, "value": 30},
                {"op": "get", "key": 2},
                {"op": "get", "key": 1},
            ],
        }
        run = self.run_cache(case)
        self.assertEqual(run.result, [None, None, None, None, -1, 11])
        self.assertEqual(
            run.frames[2]["state"], {"kind": "array", "items": ["2=20", "1=11"]}
        )
        self.assertEqual(run.frames[3]["state"], run.frames[4]["state"])

    def test_hit_refreshes_oldest_and_zero_is_a_value(self) -> None:
        case: JsonValue = {
            "capacity": 2,
            "operations": [
                {"op": "put", "key": 0, "value": 0},
                {"op": "put", "key": 1, "value": 5},
                {"op": "get", "key": 0},
                {"op": "put", "key": 2, "value": 6},
                {"op": "get", "key": 1},
                {"op": "get", "key": 0},
            ],
        }
        self.assertEqual(self.run_cache(case).result, [None, None, 0, None, -1, 0])

    def test_capacity_one_replaces_previous_entry(self) -> None:
        case: JsonValue = {
            "capacity": 1,
            "operations": [
                {"op": "get", "key": 4},
                {"op": "put", "key": 4, "value": 40},
                {"op": "put", "key": 4, "value": 41},
                {"op": "put", "key": 5, "value": 50},
                {"op": "get", "key": 4},
                {"op": "get", "key": 5},
            ],
        }
        self.assertEqual(self.run_cache(case).result, [-1, None, None, None, -1, 50])
