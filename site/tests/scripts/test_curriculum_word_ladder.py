"""Reject inaccurate Word Ladder evidence and invalid dictionary inputs."""

from dataclasses import replace
from pathlib import Path
from unittest import TestCase

from scripts.curriculum import _ENROLLED, inventory
from scripts.curriculum_evidence import EvidenceError, digest
from scripts.curriculum_trace import JsonValue, run_enrolled

_SOURCE = Path("content/leetcode/problems/127/solutions.py")
_CASE: dict[str, JsonValue] = {
    "beginWord": "aaa",
    "endWord": "bbb",
    "wordList": ["aba", "aab", "abb", "baa", "bba", "bbb"],
}


class WordLadderEvidenceTest(TestCase):
    def test_oracles_reject_forged_transitions_and_outcomes(self) -> None:
        for approach in ("queue-bfs", "two-frontier-bfs"):
            with self.subTest(approach=approach):
                key = (127, approach)
                self.assertIn(key, _ENROLLED)
                enrollment = _ENROLLED[key]
                source = _SOURCE.read_bytes()
                self.assertEqual(digest(source), enrollment.sha256)
                run = run_enrolled(source, enrollment.adapter, _CASE)
                enrollment.verify(_CASE, run)
                altered: tuple[tuple[str, JsonValue], ...] = (
                    ("stepId", "wrong-step"),
                    ("state", {"kind": "queue", "items": ["aaa"]}),
                    ("highlights", []),
                    ("codeLines", [1]),
                    ("explanation", "This step discovers the target."),
                )
                for field, wrong in altered:
                    frames = list(run.frames)
                    frames[1] = {**frames[1], field: wrong}
                    with (
                        self.subTest(field=field),
                        self.assertRaisesRegex(EvidenceError, "frame 2"),
                    ):
                        enrollment.verify(_CASE, replace(run, frames=frames))
                with self.assertRaisesRegex(EvidenceError, "frame count"):
                    enrollment.verify(_CASE, replace(run, frames=run.frames[:-1]))
                with self.assertRaisesRegex(EvidenceError, "result"):
                    enrollment.verify(_CASE, replace(run, result=5))
                with self.assertRaisesRegex(EvidenceError, "mutated"):
                    enrollment.verify(_CASE, replace(run, post_state={}))

    def test_oracle_rejects_invalid_words_and_dictionary(self) -> None:
        key = (127, "queue-bfs")
        self.assertIn(key, _ENROLLED)
        enrollment = _ENROLLED[key]
        source = _SOURCE.read_bytes()
        self.assertEqual(digest(source), enrollment.sha256)
        run = run_enrolled(source, enrollment.adapter, _CASE)
        invalid: tuple[tuple[str, JsonValue, str], ...] = (
            ("beginWord", "", "beginWord"),
            ("beginWord", "a" * 11, "length"),
            ("endWord", "aaa", "distinct endpoints"),
            ("endWord", "bb", "equal length"),
            ("wordList", [], "dictionary size"),
            ("wordList", ["bbb", "bbb"], "distinct words"),
            ("wordList", ["bβb"], "lowercase English"),
            ("wordList", ["bb"], "equal length"),
        )
        for field, value, error in invalid:
            with (
                self.subTest(field=field, value=value),
                self.assertRaisesRegex(EvidenceError, error),
            ):
                enrollment.verify({**_CASE, field: value}, run)

    def test_pilot_is_a_private_draft(self) -> None:
        statuses = inventory(Path("."))
        self.assertIsNotNone(statuses)
        assert statuses is not None
        self.assertIn(127, statuses["draft"])
        self.assertNotIn(127, statuses["verified"])
