"""Check that the independent SQL oracle rejects altered evidence."""

from dataclasses import replace
from pathlib import Path
from unittest import TestCase

from scripts.curriculum import _ENROLLED, inventory
from scripts.curriculum_evidence import EvidenceError
from scripts.curriculum_trace import JsonValue, run_enrolled

_KEY = (175, "left-join")
_CASE: list[JsonValue] = [
    [[8, "Chen", "Ira"], [2, "Diaz", "Ari"]],
    [[5, 2, "Tacoma", "WA"], [2, 2, "Seattle", "WA"]],
]


class CombineTwoTablesEvidenceTest(TestCase):
    def test_oracle_rejects_changed_result_and_table_frame(self) -> None:
        self.assertIn(_KEY, _ENROLLED)
        enrollment = _ENROLLED[_KEY]
        source = Path("content/leetcode/problems/175/solution.sql").read_bytes()
        run = run_enrolled(source, enrollment.adapter, _CASE)
        enrollment.verify(_CASE, run)
        wrong_result = {
            "columns": ["firstName", "lastName", "city", "state"],
            "rows": [
                ["Ira", "Chen", None, None],
                ["Ari", "Diaz", "Seattle", "WA"],
                ["Ari", "Diaz", "Tacoma", "WA"],
            ],
        }
        with self.assertRaisesRegex(EvidenceError, "result"):
            enrollment.verify(_CASE, replace(run, result=wrong_result))
        with self.assertRaisesRegex(EvidenceError, "frame"):
            enrollment.verify(
                _CASE, replace(run, frames=[{**run.frames[0], "codeLines": [2]}])
            )
        with self.assertRaisesRegex(EvidenceError, "input"):
            enrollment.verify(_CASE, replace(run, post_state=[]))

    def test_pilot_is_private(self) -> None:
        statuses = inventory(Path("."))
        assert statuses is not None
        self.assertIn(175, statuses["draft"])
        self.assertNotIn(175, statuses["verified"])
