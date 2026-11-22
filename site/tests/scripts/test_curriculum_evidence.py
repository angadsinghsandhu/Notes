import json
import os
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.curriculum_evidence import (
    EvidenceError,
    equal_json,
    open_curriculum,
    parse_json,
    read_bytes,
    source_line_count,
    validate_trace,
)


def trace() -> dict:
    return {
        "version": 1,
        "problemId": "leetcode:64",
        "approachId": "in-place",
        "exampleId": "small",
        "implementationSha256": "a" * 64,
        "result": 8,
        "frames": [
            {
                "stepId": "cell-0",
                "codeLines": [1],
                "explanation": "Visit the origin.",
                "state": {"kind": "grid", "rows": [[8]]},
                "highlights": [{"row": 0, "column": 0}],
            }
        ],
    }


class EvidenceTests(unittest.TestCase):
    def test_read_rejects_traversal_symlinks_and_fifo(self) -> None:
        with TemporaryDirectory() as directory:
            site = Path(directory)
            root = site / "content/leetcode"
            root.mkdir(parents=True)
            (root / "valid.json").write_bytes(b"{}")
            (root / "link.json").symlink_to(root / "valid.json")
            os.mkfifo(root / "pipe.json")
            with open_curriculum(site) as fd:
                assert fd is not None
                self.assertEqual(read_bytes(fd, "valid.json", 2), b"{}")
                for name, limit in [
                    ("../valid.json", 2),
                    ("link.json", 2),
                    ("pipe.json", 2),
                    ("valid.json", 1),
                    (".", 2),
                    ("missing.json", 2),
                ]:
                    with self.subTest(name=name), self.assertRaises(EvidenceError):
                        read_bytes(fd, name, limit)

    def test_open_directory_remains_anchored_if_path_is_replaced(self) -> None:
        with TemporaryDirectory() as directory:
            site = Path(directory)
            root = site / "content/leetcode"
            root.mkdir(parents=True)
            (root / "manifest.json").write_bytes(b"original")
            foreign = site / "foreign"
            foreign.mkdir()
            (foreign / "manifest.json").write_bytes(b"foreign")
            with open_curriculum(site) as fd:
                assert fd is not None
                root.rename(root.with_name("moved"))
                root.symlink_to(foreign, target_is_directory=True)
                self.assertEqual(read_bytes(fd, "manifest.json", 8), b"original")
            with (
                self.assertRaisesRegex(EvidenceError, "leetcode"),
                open_curriculum(site),
            ):
                self.fail("replacement path was accepted")

    def test_raw_numbers_and_duplicate_nested_members(self) -> None:
        for raw in (
            b'{"outer":{"x":1,"x":2}}',
            b"NaN",
            b"1e400",
            b"9007199254740992",
            b"9007199254740992.0",
            b"1e-500",
            b"0e-99999999999999999999999999",
            b'"\\ud800"',
        ):
            with self.subTest(raw=raw), self.assertRaises(EvidenceError):
                parse_json(raw)
        self.assertEqual(
            parse_json(b'{"num":9007199254740991}'), {"num": 9007199254740991}
        )
        self.assertEqual(parse_json(b'"9007199254740992"'), "9007199254740992")
        self.assertFalse(equal_json([True], [1]))
        self.assertFalse(equal_json({"x": [None]}, {"x": [False]}))
        self.assertTrue(equal_json({"x": 1, "y": 2}, {"y": 2.0, "x": 1.0}))

    def test_source_line_endings_match_display(self) -> None:
        self.assertEqual(source_line_count(b"\r\nstart\rmiddle\nfinish\r"), 4)
        self.assertEqual(source_line_count(b"start\r\nfinish"), 2)
        self.assertEqual(source_line_count(b""), 0)

    def test_trace_boundaries_and_source_line_invariants(self) -> None:
        payload = trace()
        frames = payload["frames"]
        frames.extend({**frames[0], "stepId": f"cell-{i}"} for i in range(1, 2000))
        validate_trace(payload, 1)
        frames.append({**frames[0], "stepId": "cell-2000"})
        with self.assertRaisesRegex(EvidenceError, "2000 frames"):
            validate_trace(payload, 1)
        payload = trace()
        size = len(json.dumps(payload, separators=(",", ":")).encode())
        payload["result"] = "x" * (1_048_576 - size - 1)
        validate_trace(payload, 1)
        payload["result"] += "x"
        with self.assertRaisesRegex(EvidenceError, "1 MiB"):
            validate_trace(payload, 1)

    def test_malformed_frames(self) -> None:
        for updates, message in [
            ({"codeLines": [2]}, "code lines"),
            ({"codeLines": [True]}, "code lines"),
            ({"codeLines": [1, 1]}, "code lines"),
            ({"explanation": " "}, "explanation"),
            ({"highlights": None}, "highlights"),
            ({"state": "grid"}, "frame state"),
        ]:
            with (
                self.subTest(updates=updates),
                self.assertRaisesRegex(EvidenceError, message),
            ):
                payload = trace()
                payload["frames"][0].update(updates)
                validate_trace(payload, 1)
        payload = trace()
        payload["frames"].append(payload["frames"][0].copy())
        with self.assertRaisesRegex(EvidenceError, "duplicate step"):
            validate_trace(payload, 1)
