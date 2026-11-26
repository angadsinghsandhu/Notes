"""Exercise the reviewed LEFT JOIN with SQLite and the independent oracle."""

from pathlib import Path
from unittest import TestCase

from scripts.curriculum import _ENROLLED
from scripts.curriculum_evidence import digest
from scripts.curriculum_trace import JsonValue, TraceRun, run_enrolled

_KEY = (175, "left-join")
_SOURCE = Path("content/leetcode/problems/175/solution.sql")


class CombineTwoTablesTest(TestCase):
    def run_query(self, case: JsonValue) -> TraceRun:
        self.assertIn(_KEY, _ENROLLED)
        enrollment = _ENROLLED[_KEY]
        source = _SOURCE.read_bytes()
        self.assertEqual(digest(source), enrollment.sha256)
        run = run_enrolled(source, enrollment.adapter, case)
        enrollment.verify(case, run)
        return run

    def test_null_extension_duplicates_orphans_and_order(self) -> None:
        people: list[JsonValue] = [[8, "Chen", "Ira"], [2, "Diaz", "Ari"]]
        addresses: list[JsonValue] = [
            [53, 2, "Tacoma", "WA"],
            [40, 2, None, "OR"],
            [21, 77, "Portland", "OR"],
            [30, 2, "Tacoma", "WA"],
            [22, None, "Salem", "OR"],
        ]
        expected = {
            "columns": ["firstName", "lastName", "city", "state"],
            "rows": [
                ["Ari", "Diaz", "Tacoma", "WA"],
                ["Ari", "Diaz", None, "OR"],
                ["Ari", "Diaz", "Tacoma", "WA"],
                ["Ira", "Chen", None, None],
            ],
        }
        run = self.run_query([people, addresses])
        self.assertEqual(run.result, expected)
        self.assertEqual(
            self.run_query([people[::-1], addresses[::-1]]).frames, run.frames
        )
        self.assertEqual(run.frames[0]["state"], {"kind": "table", **expected})
        self.assertEqual(run.frames[0]["codeLines"], [2, 3, 4, 6])
        lines = _SOURCE.read_text().splitlines()
        self.assertEqual(
            [lines[index] for index in (1, 2, 3, 5)],
            [
                "SELECT p.firstName, p.lastName, a.city, a.state",
                "FROM Person AS p",
                "LEFT JOIN Address AS a ON a.personId = p.personId",
                "ORDER BY p.personId, a.addressId;",
            ],
        )

    def test_empty_left_table_produces_no_rows(self) -> None:
        run = self.run_query([[], [[1, 7, "Tacoma", "WA"]]])
        self.assertEqual(
            run.result,
            {"columns": ["firstName", "lastName", "city", "state"], "rows": []},
        )
