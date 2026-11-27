"""Exercise both BST approaches and each highlighted source statement."""

from pathlib import Path
from unittest import TestCase

from scripts.curriculum import _ENROLLED
from scripts.curriculum_evidence import digest, parse_json
from scripts.curriculum_trace import JsonValue, TraceRunError, run_enrolled

_ROOT = Path("content/leetcode/problems/98")
_STATEMENTS = {
    "recursive-bounds": "within = (lower is None or lower < value) and (upper is None or value < upper)",
    "iterative-inorder": "increasing = previous is None or previous < value",
}


class ValidateBinarySearchTreeSolutionsTest(TestCase):
    def test_curated_cases_preserve_input_and_expose_exact_visits(self) -> None:
        cases: list[tuple[JsonValue, bool, list[list[int]]]] = [
            (
                [[10, 1, 2], [4, None, 3], [15, None, None], [11, None, None]],
                False,
                [[0, 1, 3], [1, 3, 0]],
            ),
            ([[8, None, 1], [8, None, None]], False, [[0, 1], [0, 1]]),
            (
                [[0, 1, 2], [-2147483648, None, None], [2147483647, None, None]],
                True,
                [[0, 1, 2], [1, 0, 2]],
            ),
            (
                [[4, 1, None], [3, 2, None], [2, 3, None], [1, None, None]],
                True,
                [[0, 1, 2, 3], [3, 2, 1, 0]],
            ),
        ]
        self.assertTrue((_ROOT / "examples.json").is_file(), "missing BST examples")
        evidence = parse_json((_ROOT / "examples.json").read_bytes())
        self.assertEqual(
            evidence,
            {
                "version": 1,
                "examples": [
                    {
                        "id": example,
                        "input": {"tree": tree},
                        "result": expected,
                        "postState": {"tree": tree},
                    }
                    for example, (tree, expected, _) in zip(
                        (
                            "ancestor-bound",
                            "duplicate",
                            "signed-extremes",
                            "left-skewed",
                        ),
                        cases,
                        strict=True,
                    )
                ],
            },
        )
        source = (_ROOT / "solutions.py").read_bytes()
        lines = source.decode().splitlines()
        for index, (approach, statement) in enumerate(_STATEMENTS.items()):
            enrollment = _ENROLLED[98, approach]
            self.assertEqual(digest(source), enrollment.sha256)
            for tree, expected, orders in cases:
                with self.subTest(approach=approach, tree=tree):
                    case: JsonValue = {"tree": tree}
                    run = run_enrolled(source, enrollment.adapter, case)
                    self.assertIs(run.result, expected)
                    self.assertEqual(run.post_state, case)
                    self.assertEqual(
                        [frame["stepId"] for frame in run.frames],
                        [f"check-{node}" for node in orders[index]],
                    )
                    line = lines.index(f"        {statement}") + 1
                    for frame in run.frames:
                        self.assertEqual(frame["codeLines"], [line])
                    enrollment.verify(case, run)

    def test_maximum_skew_uses_the_iterative_call_path_without_tracing(self) -> None:
        key = (98, "iterative-inorder")
        self.assertIn(key, _ENROLLED)
        enrollment = _ENROLLED[key]
        source = (_ROOT / "solutions.py").read_bytes()
        self.assertEqual(digest(source), enrollment.sha256)
        for left_skew in (False, True):
            with self.subTest(left_skew=left_skew):
                tree: list[JsonValue] = []
                for index in range(10_000):
                    child = index + 1 if index < 9_999 else None
                    tree.append(
                        [9_999 - index, child, None]
                        if left_skew
                        else [index, None, child]
                    )
                case: JsonValue = {"tree": tree}
                run = run_enrolled(source, enrollment.adapter, case)
                self.assertIs(run.result, True)
                self.assertEqual(run.post_state, case)
                self.assertEqual(run.frames, [])
                enrollment.verify(case, run)

    def test_recursive_size_limit_depends_on_depth(self) -> None:
        key = (98, "recursive-bounds")
        self.assertIn(key, _ENROLLED)
        enrollment = _ENROLLED[key]
        source = (_ROOT / "solutions.py").read_bytes()
        self.assertEqual(digest(source), enrollment.sha256)

        balanced: list[JsonValue] = []

        def append_subtree(start: int, stop: int) -> int | None:
            if start == stop:
                return None
            value = (start + stop) // 2
            index = len(balanced)
            balanced.append(None)
            balanced[index] = [
                value,
                append_subtree(start, value),
                append_subtree(value + 1, stop),
            ]
            return index

        append_subtree(0, 10_000)
        case: JsonValue = {"tree": balanced}
        run = run_enrolled(source, enrollment.adapter, case)
        self.assertIs(run.result, True)
        self.assertEqual(run.post_state, case)
        self.assertEqual(run.frames, [])
        enrollment.verify(case, run)

        skew: list[JsonValue] = [
            [index, None, index + 1 if index < 9_999 else None]
            for index in range(10_000)
        ]
        with self.assertRaisesRegex(TraceRunError, "RecursionError"):
            run_enrolled(source, enrollment.adapter, {"tree": skew})
