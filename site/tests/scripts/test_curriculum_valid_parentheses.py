"""Independent evidence checks for the bracket stack."""

from dataclasses import replace
from pathlib import Path
from unittest import TestCase

from scripts.curriculum import _ENROLLED
from scripts.curriculum_evidence import EvidenceError
from scripts.curriculum_trace import JsonValue, run_enrolled


class ValidParenthesesEvidenceTest(TestCase):
    def test_corrupted_intermediate_stack_fails_with_correct_final_result(self) -> None:
        key = (20, "unmatched-openings")
        self.assertIn(key, _ENROLLED, "the bracket stack has no reviewed enrollment")
        enrollment = _ENROLLED[key]
        source = Path("content/leetcode/problems/20/solutions.py").read_bytes()
        case: JsonValue = {"s": "{[()]}"}
        run = run_enrolled(source, enrollment.adapter, case)
        self.assertIs(run.result, True)
        enrollment.verify(case, run)
        frames = list(run.frames)
        frames[1] = {**frames[1], "state": {"kind": "stack", "items": ["[", "{"]}}
        with self.assertRaisesRegex(EvidenceError, "frame 2"):
            enrollment.verify(case, replace(run, frames=frames))

    def test_oracle_rejects_wrong_boolean(self) -> None:
        key = (20, "unmatched-openings")
        self.assertIn(key, _ENROLLED, "the bracket stack has no reviewed enrollment")
        enrollment = _ENROLLED[key]
        source = Path("content/leetcode/problems/20/solutions.py").read_bytes()
        case: JsonValue = {"s": "(()"}
        run = run_enrolled(source, enrollment.adapter, case)
        with self.assertRaisesRegex(EvidenceError, "result"):
            enrollment.verify(case, replace(run, result=True))
