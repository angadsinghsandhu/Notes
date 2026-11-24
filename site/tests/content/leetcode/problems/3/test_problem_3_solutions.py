"""Check both sliding-window approaches in the bounded adapter."""

from ast import FunctionDef, parse
from pathlib import Path
from unittest import TestCase

from scripts.curriculum import _ENROLLED
from scripts.curriculum_evidence import array, digest, integer, text
from scripts.curriculum_trace import JsonValue, run_enrolled

_SOURCE = Path("content/leetcode/problems/3/solutions.py")


class LongestSubstringTest(TestCase):
    def test_inside_repeat_shrinks_across_multiple_characters(self) -> None:
        self.assertIn((3, "set-eviction"), _ENROLLED)
        enrollment = _ENROLLED[3, "set-eviction"]
        case: JsonValue = {"s": "cabbde"}
        run = run_enrolled(_SOURCE.read_bytes(), enrollment.adapter, case)
        self.assertEqual(run.result, 3)
        events = {
            frame["stepId"]: frame["highlights"]
            for frame in run.frames
            if isinstance(frame["stepId"], str)
        }
        self.assertEqual(events["evict-3-0"], [{"index": 1}, {"index": 2}])
        self.assertEqual(events["evict-3-1"], [{"index": 2}])
        self.assertEqual(events["evict-3-2"], [])
        self.assertEqual(events["accept-3"], [{"index": 3}])

    def test_curated_cases_and_executed_lines(self) -> None:
        statements = {
            "evict": "left += 1",
            "jump": "left = previous + 1",
            "accept": "best = max(best, right - left + 1)",
            "finish": "return best",
        }
        source = _SOURCE.read_bytes()
        lines = source.decode().splitlines()
        functions = {
            node.name: node
            for node in parse(source).body
            if isinstance(node, FunctionDef)
        }
        for approach in ("set-eviction", "last-seen-jump"):
            self.assertIn((3, approach), _ENROLLED)
            enrollment = _ENROLLED[3, approach]
            self.assertEqual(digest(source), enrollment.sha256)
            function = functions[approach.replace("-", "_")]
            assert function.end_lineno is not None
            for value, expected in (("", 0), ("cabbde", 3), ("abba", 2), (" !1! 2", 4)):
                with self.subTest(approach=approach, value=value):
                    case: JsonValue = {"s": value}
                    run = run_enrolled(source, enrollment.adapter, case)
                    self.assertEqual(run.result, expected)
                    self.assertEqual(run.post_state, case)
                    enrollment.verify(case, run)
                    for frame in run.frames:
                        step = text(frame["stepId"], "step ID").split("-")[0]
                        references = array(frame["codeLines"], "code lines")
                        self.assertEqual(len(references), 1)
                        line = integer(
                            references[0],
                            function.lineno,
                            function.end_lineno,
                            "code line",
                        )
                        self.assertEqual(lines[line - 1].strip(), statements[step])
                    if value == "abba":
                        self.assertEqual(
                            run.frames[-2]["highlights"], [{"index": 2}, {"index": 3}]
                        )
