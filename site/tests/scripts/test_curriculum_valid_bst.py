"""Reject inaccurate BST intermediate evidence and malformed lesson trees."""

from dataclasses import replace
from pathlib import Path
from unittest import TestCase

from scripts.curriculum import _ENROLLED, inventory
from scripts.curriculum_evidence import EvidenceError, digest
from scripts.curriculum_trace import JsonValue, run_enrolled


class ValidateBinarySearchTreeEvidenceTest(TestCase):
    def test_oracle_rejects_an_incorrect_intermediate_state(self) -> None:
        case: JsonValue = {"tree": [[4, 1, 2], [3, None, None], [6, None, None]]}
        for approach in ("recursive-bounds", "iterative-inorder"):
            with self.subTest(approach=approach):
                key = (98, approach)
                self.assertIn(key, _ENROLLED)
                enrollment = _ENROLLED[key]
                source = Path("content/leetcode/problems/98/solutions.py").read_bytes()
                self.assertEqual(digest(source), enrollment.sha256)
                run = run_enrolled(source, enrollment.adapter, case)
                enrollment.verify(case, run)

                for field, wrong in (
                    ("stepId", "check-9"),
                    ("state", {"kind": "tree", "nodes": [], "edges": []}),
                    ("highlights", [{"nodeId": "node-9"}]),
                    ("codeLines", [1]),
                    ("explanation", "The values pass a different comparison."),
                ):
                    frames = [
                        {**frame, field: wrong} if index == 1 else frame
                        for index, frame in enumerate(run.frames)
                    ]
                    with (
                        self.subTest(field=field),
                        self.assertRaisesRegex(EvidenceError, "frame 2"),
                    ):
                        enrollment.verify(case, replace(run, frames=frames))
                with self.assertRaisesRegex(EvidenceError, "frame count"):
                    enrollment.verify(case, replace(run, frames=run.frames[:-1]))
                with self.assertRaisesRegex(EvidenceError, "result"):
                    enrollment.verify(case, replace(run, result=False))
                with self.assertRaisesRegex(EvidenceError, "mutated"):
                    enrollment.verify(case, replace(run, post_state={"tree": []}))

    def test_oracle_rejects_invalid_input_shape_or_value(self) -> None:
        key = (98, "iterative-inorder")
        self.assertIn(key, _ENROLLED)
        enrollment = _ENROLLED[key]
        source = Path("content/leetcode/problems/98/solutions.py").read_bytes()
        self.assertEqual(digest(source), enrollment.sha256)
        run = run_enrolled(source, enrollment.adapter, {"tree": [[0, None, None]]})
        invalid: list[tuple[JsonValue, str]] = [
            ([], "node count"),
            ([[True, None, None]], "node value"),
            ([[2147483648, None, None]], "node value"),
            ([[0, 1, None]], "child index"),
            ([[0, 0, None]], "repeated node"),
            ([[1, 1, 1], [0, None, None]], "repeated node"),
            ([[1, None, None], [0, None, None]], "unreachable node"),
        ]
        for tree, problem in invalid:
            with (
                self.subTest(tree=tree),
                self.assertRaisesRegex(EvidenceError, problem),
            ):
                enrollment.verify({"tree": tree}, run)

    def test_pilot_is_a_private_draft(self) -> None:
        statuses = inventory(Path("."))
        self.assertIsNotNone(statuses)
        assert statuses is not None
        self.assertIn(98, statuses["draft"])
        self.assertNotIn(98, statuses["verified"])
