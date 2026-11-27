"""Reject forged LRU evidence and out-of-contract operations."""

from dataclasses import replace
from pathlib import Path
from unittest import TestCase

from scripts.curriculum import _ENROLLED, inventory
from scripts.curriculum_evidence import EvidenceError
from scripts.curriculum_trace import JsonValue, run_enrolled

_KEY = (146, "linked-recency")
_CASE: dict[str, JsonValue] = {
    "capacity": 1,
    "operations": [{"op": "put", "key": 1, "value": 10}, {"op": "get", "key": 1}],
}


class LruCacheEvidenceTest(TestCase):
    def test_oracle_rejects_forged_run(self) -> None:
        self.assertIn(_KEY, _ENROLLED)
        enrollment = _ENROLLED[_KEY]
        source = Path("content/leetcode/problems/146/solutions.py").read_bytes()
        run = run_enrolled(source, enrollment.adapter, _CASE)
        enrollment.verify(_CASE, run)
        wrong: tuple[tuple[str, JsonValue], ...] = (
            ("stepId", "get-9"),
            ("codeLines", [1]),
            ("explanation", "Get missed."),
            ("highlights", []),
            ("state", {"kind": "array", "items": ["1=11"]}),
        )
        for field, value in wrong:
            frames = [run.frames[0], {**run.frames[1], field: value}]
            with (
                self.subTest(field=field),
                self.assertRaisesRegex(EvidenceError, "frame 2"),
            ):
                enrollment.verify(_CASE, replace(run, frames=frames))
        with self.assertRaisesRegex(EvidenceError, "frame count"):
            enrollment.verify(_CASE, replace(run, frames=run.frames[:-1]))
        with self.assertRaisesRegex(EvidenceError, "result"):
            enrollment.verify(_CASE, replace(run, result=[None, -1]))
        with self.assertRaisesRegex(EvidenceError, "mutated"):
            enrollment.verify(_CASE, replace(run, post_state={}))

    def test_oracle_validates_operation_shape_and_bounds(self) -> None:
        self.assertIn(_KEY, _ENROLLED)
        enrollment = _ENROLLED[_KEY]
        source = Path("content/leetcode/problems/146/solutions.py").read_bytes()
        run = run_enrolled(source, enrollment.adapter, _CASE)
        invalid: tuple[tuple[JsonValue, str], ...] = (
            ({"capacity": 0, "operations": []}, "capacity"),
            ({**_CASE, "operations": []}, "operation count"),
            ({**_CASE, "operations": [{"op": "delete", "key": 0}]}, "operation name"),
            ({**_CASE, "operations": [{"op": "get", "key": True}]}, "key"),
            ({**_CASE, "operations": [{"op": "put", "key": 1}]}, "invalid fields"),
            (
                {**_CASE, "operations": [{"op": "put", "key": 1, "value": 100001}]},
                "value",
            ),
        )
        for case, error in invalid:
            with self.subTest(case=case), self.assertRaisesRegex(EvidenceError, error):
                enrollment.verify(case, run)

    def test_pilot_is_verified(self) -> None:
        statuses = inventory(Path("."))
        self.assertIsNotNone(statuses)
        assert statuses is not None
        self.assertIn(146, statuses["verified"])
        self.assertNotIn(146, statuses["draft"])
