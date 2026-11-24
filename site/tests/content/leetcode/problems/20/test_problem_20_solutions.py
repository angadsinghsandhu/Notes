"""Exercise the bracket stack using its pinned bounded adapter."""

from pathlib import Path
from unittest import TestCase

from scripts.curriculum import _ENROLLED
from scripts.curriculum_evidence import array, digest, integer, text
from scripts.curriculum_trace import JsonValue, run_enrolled

_SOURCE = Path("content/leetcode/problems/20/solutions.py")
_KEY = (20, "unmatched-openings")
_CASES = (("(()", False), ("]()", False), ("([)]", False), ("{[()]}", True))


class ValidParenthesesTest(TestCase):
    def setUp(self) -> None:
        self.assertIn(_KEY, _ENROLLED, "the bracket stack has no reviewed enrollment")
        self.enrollment = _ENROLLED[_KEY]
        self.source = _SOURCE.read_bytes()
        self.assertEqual(digest(self.source), self.enrollment.sha256)

    def test_unfinished_stack_returns_false(self) -> None:
        case: JsonValue = {"s": "(()"}
        run = run_enrolled(self.source, self.enrollment.adapter, case)
        self.assertIs(run.result, False)
        self.assertEqual(run.frames[-1]["state"], {"kind": "stack", "items": ["("]})

    def test_curated_cases_and_executed_lines(self) -> None:
        lines = self.source.decode().splitlines()
        statements = {
            "push": "stack.append(bracket)",
            "reject": "if not stack or stack[-1] != opening:",
            "pop": "stack.pop()",
            "finish": "balanced = not stack",
        }
        for value, expected in _CASES:
            with self.subTest(value=value):
                case: JsonValue = {"s": value}
                run = run_enrolled(self.source, self.enrollment.adapter, case)
                self.assertIs(run.result, expected)
                self.assertEqual(run.post_state, case)
                self.enrollment.verify(case, run)
                for frame in run.frames:
                    step = text(frame["stepId"], "step ID").split("-")[0]
                    references = array(frame["codeLines"], "code lines")
                    self.assertEqual(len(references), 1)
                    line = integer(references[0], 1, len(lines), "code line")
                    self.assertEqual(lines[line - 1].strip(), statements[step])
