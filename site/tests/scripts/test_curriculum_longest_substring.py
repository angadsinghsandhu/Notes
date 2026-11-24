"""Check that the independent oracle rejects false sliding-window evidence."""

from dataclasses import replace
from pathlib import Path
from unittest import TestCase

from scripts.curriculum import _ENROLLED
from scripts.curriculum_evidence import EvidenceError
from scripts.curriculum_trace import JsonValue, run_enrolled


class LongestSubstringEvidenceTest(TestCase):
    def test_corrupted_intermediate_window_fails_with_correct_final_result(
        self,
    ) -> None:
        source_path = Path("content/leetcode/problems/3/solutions.py")
        case: JsonValue = {"s": "cabbde"}
        for approach, step in (
            ("set-eviction", "evict-3-0"),
            ("last-seen-jump", "jump-3"),
        ):
            with self.subTest(approach=approach):
                self.assertIn((3, approach), _ENROLLED)
                enrollment = _ENROLLED[3, approach]
                run = run_enrolled(source_path.read_bytes(), enrollment.adapter, case)
                self.assertEqual(run.result, 3)
                enrollment.verify(case, run)
                frames = list(run.frames)
                position = next(
                    index
                    for index, frame in enumerate(frames)
                    if frame["stepId"] == step
                )
                frames[position] = {**frames[position], "highlights": [{"index": 0}]}
                with self.assertRaisesRegex(EvidenceError, f"frame {position + 1}"):
                    enrollment.verify(case, replace(run, frames=frames))
                with self.assertRaisesRegex(EvidenceError, "result"):
                    enrollment.verify(case, replace(run, result=4))
