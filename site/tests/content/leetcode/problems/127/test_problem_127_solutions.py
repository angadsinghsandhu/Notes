"""Exercise reviewed Word Ladder code and its displayed source lines."""

from itertools import islice, product
from pathlib import Path
from unittest import TestCase

from scripts.curriculum import _ENROLLED
from scripts.curriculum_evidence import array, digest, integer, obj, parse_json, text
from scripts.curriculum_trace import Frame, JsonValue, run_enrolled

_ROOT = Path("content/leetcode/problems/127")
_CASES: tuple[tuple[str, str, str, list[JsonValue], int], ...] = (
    ("target-absent", "mint", "mist", ["mind", "mild", "mile"], 0),
    ("target-unreachable", "mare", "tune", ["care", "cane", "tone", "tune", "mare"], 0),
    ("one-change", "i", "a", ["a"], 2),
    ("competing-paths", "aaa", "bbb", ["aba", "aab", "abb", "baa", "bba", "bbb"], 4),
)
_STEPS = {
    "queue-bfs": {
        "absent": "if end not in remaining:",
        "visit": "word, length = queue.popleft()",
        "exhausted": "return 0",
    },
    "two-frontier-bfs": {
        "absent": "if end not in dictionary:",
        "expand": "for word in active:",
        "meet": "if candidate in other_distances:",
        "exhausted": "return 0",
    },
}


def _items(frame: Frame) -> list[JsonValue]:
    return array(obj(frame["state"], "state")["items"], "items")


class WordLadderSolutionsTest(TestCase):
    def test_curated_cases_preserve_input_and_highlight_real_statements(self) -> None:
        self.assertTrue(
            (_ROOT / "examples.json").is_file(), "missing Word Ladder examples"
        )
        examples: list[dict[str, JsonValue]] = []
        for example_id, begin, end, words, expected in _CASES:
            case: JsonValue = {"beginWord": begin, "endWord": end, "wordList": words}
            examples.append(
                {"id": example_id, "input": case, "result": expected, "postState": case}
            )
        self.assertEqual(
            parse_json((_ROOT / "examples.json").read_bytes()),
            {"version": 1, "examples": examples},
        )
        source = (_ROOT / "solutions.py").read_bytes()
        lines = source.decode().splitlines()
        for approach, statements in _STEPS.items():
            enrollment = _ENROLLED[127, approach]
            self.assertEqual(digest(source), enrollment.sha256)
            for example in examples:
                case = example["input"]
                with self.subTest(approach=approach, example=example["id"]):
                    run = run_enrolled(source, enrollment.adapter, case)
                    self.assertEqual(run.result, example["result"])
                    self.assertEqual(run.post_state, case)
                    self.assertGreater(len(run.frames), 0)
                    for frame in run.frames:
                        step = text(frame["stepId"], "step ID").split("-")[0]
                        (line,) = array(frame["codeLines"], "code lines")
                        offset = integer(line, 1, len(lines), "source line") - 1
                        self.assertEqual(lines[offset].strip(), statements[step])
                    enrollment.verify(case, run)

    def test_queue_enqueues_shared_neighbors_once_and_frontiers_swap(self) -> None:
        _, begin, end, words, _ = _CASES[-1]
        case: JsonValue = {"beginWord": begin, "endWord": end, "wordList": words}
        source = (_ROOT / "solutions.py").read_bytes()
        self.assertEqual(digest(source), _ENROLLED[127, "queue-bfs"].sha256)
        self.assertEqual(digest(source), _ENROLLED[127, "two-frontier-bfs"].sha256)
        queue = run_enrolled(source, _ENROLLED[127, "queue-bfs"].adapter, case)
        self.assertEqual(
            [_items(frame)[0] for frame in queue.frames],
            ["aaa", "baa", "aba", "aab", "bba", "abb", "bbb"],
        )
        two_frontier = run_enrolled(
            source, _ENROLLED[127, "two-frontier-bfs"].adapter, case
        )
        self.assertEqual(
            [_items(frame) for frame in two_frontier.frames],
            [
                ["aaa", "|", "bbb"],
                ["bbb", "|", "aab", "aba", "baa"],
                ["abb", "bba", "|", "aab", "aba", "baa"],
                ["abb", "aab"],
            ],
        )

    def test_both_searches_take_the_dictionary_detour(self) -> None:
        case: JsonValue = {
            "beginWord": "aaa",
            "endWord": "bba",
            "wordList": ["aac", "abc", "bbc", "bba"],
        }
        for approach in _STEPS:
            with self.subTest(approach=approach):
                self.assertIn((127, approach), _ENROLLED)
                enrollment = _ENROLLED[127, approach]
                source = (_ROOT / "solutions.py").read_bytes()
                self.assertEqual(digest(source), enrollment.sha256)
                run = run_enrolled(source, enrollment.adapter, case)
                self.assertEqual(run.result, 5)
                enrollment.verify(case, run)

    def test_maximum_dictionary_and_word_width_stay_in_the_bounded_runner(self) -> None:
        words: list[JsonValue] = [
            "".join(letters) + "aaaa"
            for letters in islice(product("abcde", repeat=6), 4999)
        ]
        words.append("zzzzzzzzzz")
        case: JsonValue = {
            "beginWord": "aaaaaaaaaa",
            "endWord": "zzzzzzzzzz",
            "wordList": words,
        }
        for approach in _STEPS:
            with self.subTest(approach=approach):
                self.assertIn((127, approach), _ENROLLED)
                enrollment = _ENROLLED[127, approach]
                source = (_ROOT / "solutions.py").read_bytes()
                self.assertEqual(digest(source), enrollment.sha256)
                run = run_enrolled(source, enrollment.adapter, case)
                self.assertEqual(run.result, 0)
                self.assertEqual(run.post_state, case)
                self.assertEqual(run.frames, [])
                enrollment.verify(case, run)
