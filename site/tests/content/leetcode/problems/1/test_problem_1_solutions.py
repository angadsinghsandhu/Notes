"""Check the pinned Two Sum implementations through the bounded runner."""

from itertools import combinations, product
from pathlib import Path
from unittest import TestCase

from scripts.curriculum import _ENROLLED
from scripts.curriculum_evidence import array, digest, integer, text
from scripts.curriculum_trace import Frame, run_enrolled

_SOURCE = Path("content/leetcode/problems/1/solutions.py")
_APPROACH_IDS = ("pair-enumeration", "sorted-two-pointers", "complement-hash")


class TwoSumTest(TestCase):
    def setUp(self) -> None:
        self.source = _SOURCE.read_bytes()
        for approach in _APPROACH_IDS:
            self.assertEqual(digest(self.source), _ENROLLED[1, approach].sha256)

    def check_case(self, nums: list[int], target: int, expected: list[int]) -> None:
        for approach in _APPROACH_IDS:
            enrollment = _ENROLLED[1, approach]
            case = {"nums": list(nums), "target": target}
            run = run_enrolled(self.source, enrollment.adapter, case)
            self.assertEqual(run.result, expected)
            self.assertEqual(run.post_state, case)
            enrollment.verify(case, run)

    def test_duplicate_requires_distinct_positions(self) -> None:
        self.check_case([6, 1, 6], 12, [0, 2])

    def test_two_int_extremes_and_reversed_sorted_positions(self) -> None:
        self.check_case([10**9, -(10**9)], 0, [0, 1])

    def test_repeated_non_answer_values_do_not_prevent_solution(self) -> None:
        self.check_case([3, 3, -4, 8, 6], 2, [2, 4])

    def test_frame_references_identify_the_executed_statements(self) -> None:
        source = self.source.decode().splitlines()
        statements = {
            "pair-enumeration": {"compare": "total = nums[left] + nums[right]"},
            "sorted-two-pointers": {
                "sort": "ordered = sorted((value, index) for index, value in enumerate(nums))",
                "compare": "total = low + high",
                "Drop the left endpoint.": "left += 1",
                "Drop the right endpoint.": "right -= 1",
            },
            "complement-hash": {
                "lookup": "earlier = seen.get(needed)",
                "record": "seen[value] = index",
            },
        }
        for approach, lines in statements.items():
            adapter = _ENROLLED[1, approach].adapter
            frames: list[Frame] = []
            for nums, target in (([-4, 8, 1, 6], 2), ([6, 1, 6], 12)):
                frames.extend(
                    run_enrolled(
                        self.source, adapter, {"nums": list(nums), "target": target}
                    ).frames
                )
            for frame in frames:
                step = text(frame["stepId"], "step ID").split("-")[0]
                if step == "move":
                    step = text(frame["explanation"], "explanation").split(". ", 1)[1]
                references = array(frame["codeLines"], "code lines")
                self.assertEqual(len(references), 1)
                line = integer(references[0], 1, len(source), "code line")
                self.assertEqual(source[line - 1].strip(), lines[step])

    def test_small_exhaustive_unique_pair_targets(self) -> None:
        cases = 0
        for length in (2, 3):
            for values in product((-1, 0, 1), repeat=length):
                pairs_by_sum: dict[int, list[list[int]]] = {}
                for left, right in combinations(range(length), 2):
                    pairs_by_sum.setdefault(values[left] + values[right], []).append(
                        [left, right]
                    )
                for target, pairs in pairs_by_sum.items():
                    if len(pairs) == 1:
                        self.check_case(list(values), target, pairs[0])
                        cases += 1
        self.assertEqual(cases, 45)
