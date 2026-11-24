"""Reject path-sum evidence that misstates a computed cell or caller state."""

from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from unittest import TestCase

from scripts.curriculum import _ENROLLED
from scripts.curriculum_evidence import EvidenceError, array, obj
from scripts.curriculum_trace import JsonValue, run_enrolled


class MinimumPathSumEvidenceTest(TestCase):
    def test_oracle_rejects_incorrect_evidence_for_both_approaches(self) -> None:
        case: JsonValue = {"grid": [[1, 7, 1], [2, 3, 1]]}
        for approach in ("memoized-grid", "row-storage"):
            with self.subTest(approach=approach):
                key = (64, approach)
                self.assertIn(key, _ENROLLED)
                enrollment = _ENROLLED[key]
                source = Path("content/leetcode/problems/64/solutions.py").read_bytes()
                run = run_enrolled(source, enrollment.adapter, case)
                self.assertEqual(run.result, 7)
                enrollment.verify(case, run)

                frames = deepcopy(run.frames)
                state = obj(frames[0]["state"], "trace state")
                if approach == "memoized-grid":
                    rows = array(state["rows"], "grid rows")
                    array(rows[-1], "last row")[-1] = 0
                else:
                    array(state["items"], "rolling row")[0] = 0
                with self.assertRaisesRegex(EvidenceError, "frame 1"):
                    enrollment.verify(case, replace(run, frames=frames))
                with self.assertRaisesRegex(EvidenceError, "frame count"):
                    enrollment.verify(case, replace(run, frames=run.frames[:-1]))
                with self.assertRaisesRegex(EvidenceError, "result"):
                    enrollment.verify(case, replace(run, result=8))
                with self.assertRaisesRegex(EvidenceError, "mutated"):
                    enrollment.verify(case, replace(run, post_state={"grid": [[7]]}))
