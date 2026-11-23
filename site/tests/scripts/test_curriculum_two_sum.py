"""The Two Sum evidence checks must reject impossible execution."""

from unittest import TestCase

from scripts.curriculum_evidence import EvidenceError
from scripts.curriculum_trace import Frame, TraceRun
from scripts.curriculum_two_sum import verify_hash, verify_pairs, verify_sorted


class TwoSumEvidenceTest(TestCase):
    def test_rejects_wrong_pair_and_post_state(self) -> None:
        for verify in (verify_pairs, verify_sorted, verify_hash):
            with self.assertRaisesRegex(EvidenceError, "unique pair"):
                verify(
                    {"nums": [6, 1, 6], "target": 12},
                    TraceRun([0, 0], [], {"nums": [6, 1, 6], "target": 12}),
                )
            with self.assertRaisesRegex(EvidenceError, "mutated"):
                verify(
                    {"nums": [6, 1, 6], "target": 12},
                    TraceRun([0, 2], [], {"nums": [6, 6, 1], "target": 12}),
                )

    def test_rejects_missing_actual_steps(self) -> None:
        for verify in (verify_pairs, verify_sorted, verify_hash):
            with self.assertRaisesRegex(EvidenceError, "frame count"):
                verify(
                    {"nums": [6, 1, 6], "target": 12},
                    TraceRun([0, 2], [], {"nums": [6, 1, 6], "target": 12}),
                )

    def test_rejects_incorrect_frame_state_even_with_correct_result(self) -> None:
        frame: Frame = {
            "stepId": "compare-0-1",
            "codeLines": [1],
            "explanation": "The values are different from the executed comparison.",
            "state": {"kind": "array", "items": [6, 6]},
            "highlights": [{"index": 0}, {"index": 1}],
        }
        with self.assertRaisesRegex(EvidenceError, "frame 1"):
            verify_pairs(
                {"nums": [6, 6], "target": 12},
                TraceRun([0, 1], [frame], {"nums": [6, 6], "target": 12}),
            )
