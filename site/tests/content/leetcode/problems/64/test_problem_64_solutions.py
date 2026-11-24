"""Exercise both path-sum approaches and the code shown by their traces."""

from pathlib import Path
from unittest import TestCase

from scripts.curriculum import _ENROLLED
from scripts.curriculum_evidence import array, digest, integer
from scripts.curriculum_trace import JsonValue, run_enrolled

_SOURCE = Path("content/leetcode/problems/64/solutions.py")
_CASES = (
    ([[2], [0], [7], [1]], 10),
    ([[1, 9, 1, 1], [2, 2, 8, 1], [9, 1, 1, 1]], 8),
    ([[0]], 0),
    ([[1, 1, 1], [1, 1, 1]], 4),
)
_STATEMENTS = {
    "memoized-grid": "saved[row][column] = total",
    "row-storage": "costs[column] = total",
}


class MinimumPathSumSolutionsTest(TestCase):
    def test_curated_results_frames_and_unchanged_input(self) -> None:
        for approach, statement in _STATEMENTS.items():
            key = (64, approach)
            self.assertIn(key, _ENROLLED)
            enrollment = _ENROLLED[key]
            source = _SOURCE.read_bytes()
            self.assertEqual(digest(source), enrollment.sha256)
            lines = source.decode().splitlines()
            for grid, expected in _CASES:
                with self.subTest(approach=approach, grid=grid):
                    case: JsonValue = {"grid": [list(row) for row in grid]}
                    run = run_enrolled(source, enrollment.adapter, case)
                    self.assertEqual(run.result, expected)
                    self.assertEqual(run.post_state, {"grid": grid})
                    self.assertEqual(len(run.frames), len(grid) * len(grid[0]))
                    enrollment.verify(case, run)
                    for frame in run.frames:
                        references = array(frame["codeLines"], "code lines")
                        self.assertEqual(len(references), 1)
                        line = integer(references[0], 1, len(lines), "code line")
                        self.assertEqual(lines[line - 1].strip(), statement)

    def test_published_maximum_height_and_width(self) -> None:
        source = _SOURCE.read_bytes()
        grids = ([[200] for _ in range(200)], [[200] * 200])
        for approach in _STATEMENTS:
            enrollment = _ENROLLED[64, approach]
            self.assertEqual(digest(source), enrollment.sha256)
            for grid in grids:
                with self.subTest(
                    approach=approach, dimensions=(len(grid), len(grid[0]))
                ):
                    case: JsonValue = {"grid": [list(row) for row in grid]}
                    run = run_enrolled(source, enrollment.adapter, case)
                    self.assertEqual(run.result, 40_000)
                    self.assertEqual(run.post_state, {"grid": grid})
                    self.assertEqual(len(run.frames), 200)
                    enrollment.verify(case, run)
