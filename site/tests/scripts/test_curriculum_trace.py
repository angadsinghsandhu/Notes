import io
import json
import socket
import subprocess
import unittest
from typing import BinaryIO
from unittest.mock import patch

from scripts.curriculum_isolation import IsolationError
from scripts.curriculum_trace import (
    JsonValue,
    PythonAdapter,
    SqlAdapter,
    TraceRunError,
    _child,
    run_enrolled,
)

MUTATION = b"""
def solve(case, emit):
    def walk(index):
        if index == len(case):
            return sum(case)
        case[index] *= 2
        emit({
            "stepId": f"visit-{index}",
            "codeLines": [6],
            "explanation": "Double the selected item.",
            "state": {"kind": "array", "items": case},
            "highlights": [{"index": index}],
        })
        total = walk(index + 1)
        case[index] //= 2
        emit({
            "stepId": f"restore-{index}",
            "codeLines": [15],
            "explanation": "Restore the selected item.",
            "state": {"kind": "array", "items": case},
            "highlights": [{"index": index}],
        })
        return total
    return walk(0)
"""
SQL = SqlAdapter(
    setup=("CREATE TABLE scores (value INTEGER)",),
    inserts=("INSERT INTO scores VALUES (?)",),
    code_lines=(1,),
    explanation="Read scores in order.",
)


class CurriculumTraceTests(unittest.TestCase):
    def test_backtracking_frames_are_actual_snapshots(self) -> None:
        case: list[JsonValue] = [2, 3]
        run = run_enrolled(MUTATION, PythonAdapter("solve"), case)
        expected = [[4, 3], [4, 6], [4, 3], [2, 3]]
        self.assertEqual(run.result, 2 * (2 + 3))
        self.assertEqual(run.post_state, [2, 3])
        self.assertEqual(
            [frame["state"] for frame in run.frames],
            [{"kind": "array", "items": items} for items in expected],
        )
        self.assertEqual(run, run_enrolled(MUTATION, PythonAdapter("solve"), case))
        self.assertEqual(case, [2, 3])

    def test_changed_middle_frame_changes_evidence_with_same_result(self) -> None:
        adapter = PythonAdapter("solve")
        alternate = MUTATION.replace(b'"items": case', b'"items": case[::-1]', 1)
        original = run_enrolled(MUTATION, adapter, [2, 3])
        changed = run_enrolled(alternate, adapter, [2, 3])
        self.assertEqual(original.result, changed.result)
        self.assertEqual(original.post_state, changed.post_state)
        self.assertNotEqual(original.frames[1], changed.frames[1])

    def test_preserves_input_mutation_after_return(self) -> None:
        source = (
            b"def solve(case, emit):\n    case['items'].append(3)\n    return None\n"
        )
        case: JsonValue = {"items": [2]}
        run = run_enrolled(source, PythonAdapter("solve"), case)
        self.assertIsNone(run.result)
        self.assertEqual(run.post_state, {"items": [2, 3]})
        self.assertEqual(case, {"items": [2]})

    def test_sql_preserves_names_types_nulls_duplicates_and_order(self) -> None:
        inputs: JsonValue = [[[3], [None], [3], [1]]]
        run = run_enrolled(
            b"SELECT value, value = 3 AS equals_target FROM scores ORDER BY value",
            SQL,
            inputs,
        )
        result = {
            "columns": ["value", "equals_target"],
            "rows": [[None, None], [1, 0], [3, 1], [3, 1]],
        }
        self.assertEqual(run.result, result)
        self.assertIsInstance(run.result, dict)
        assert isinstance(run.result, dict)
        rows = run.result["rows"]
        assert isinstance(rows, list) and isinstance(rows[1], list)
        self.assertIs(type(rows[1][1]), int)
        self.assertEqual(run.frames[0]["state"], {"kind": "table", **result})
        self.assertEqual(run.post_state, inputs)

    def test_sql_left_join_preserves_missing_and_multiple_matches(self) -> None:
        adapter = SqlAdapter(
            setup=(
                "CREATE TABLE people (id INTEGER, name TEXT)",
                "CREATE TABLE addresses (person_id INTEGER, city TEXT)",
            ),
            inserts=(
                "INSERT INTO people VALUES (?, ?)",
                "INSERT INTO addresses VALUES (?, ?)",
            ),
            code_lines=(1,),
            explanation="Preserve people without addresses.",
        )
        run = run_enrolled(
            b"SELECT name, city FROM people LEFT JOIN addresses ON id = person_id "
            b"ORDER BY name, city",
            adapter,
            [[[1, "Ana"], [2, "Bo"]], [[2, "Delhi"], [2, "Pune"]]],
        )
        self.assertEqual(
            run.result,
            {
                "columns": ["name", "city"],
                "rows": [["Ana", None], ["Bo", "Delhi"], ["Bo", "Pune"]],
            },
        )

    def test_sql_rejects_writes_extensions_and_extra_statements(self) -> None:
        for source in (
            b"DELETE FROM scores RETURNING value",
            b"SELECT load_extension('extension')",
            b"SELECT random()",
            b"CREATE TEMP TABLE scratch (value)",
            b"PRAGMA integrity_check",
            b"ATTACH DATABASE ':memory:' AS other",
            b"SELECT value FROM scores; SELECT 9",
        ):
            with self.subTest(source=source), self.assertRaises(TraceRunError):
                run_enrolled(source, SQL, [[]])

    def test_confines_host_read_network_and_process_creation(self) -> None:
        # Confirm the loopback operation works outside confinement in this process.
        with socket.socket() as listener:
            listener.bind(("127.0.0.1", 0))
        source = b"""
import os
import io
import socket

def solve(case, emit):
    def fork_then_reap():
        pid = os.fork()
        if pid == 0:
            os._exit(0)
        os.waitpid(pid, 0)

    denied = []
    for attempt in (
        lambda: open(case, "rb"),
        lambda: os.close(os.open(case, os.O_WRONLY)),
        lambda: socket.socket().bind(("127.0.0.1", 0)),
        fork_then_reap,
    ):
        try:
            attempt()
        except PermissionError:
            denied.append(True)
    return denied
"""
        result = run_enrolled(source, PythonAdapter("solve"), __file__)
        self.assertEqual(result.result, [True, True, True, True])

    def test_wall_clock_timeout(self) -> None:
        source = b"def solve(case, emit):\n    while True: pass\n"
        with self.assertRaisesRegex(TraceRunError, "timed out"):
            run_enrolled(source, PythonAdapter("solve"), None, timeout=0.25)

    def test_cpu_limit_precedes_longer_wall_timeout(self) -> None:
        source = b"def solve(case, emit):\n    while True: pass\n"
        with self.assertRaisesRegex(TraceRunError, r"execution failed \(-"):
            run_enrolled(source, PythonAdapter("solve"), None, timeout=10)

    def test_bounds_raw_output_and_frame_count(self) -> None:
        for body in ("print('x' * 3_000_000)", "for _ in range(2001): emit({})"):
            with self.subTest(body=body), self.assertRaises(TraceRunError):
                run_enrolled(
                    f"def solve(case, emit):\n    {body}\n".encode(),
                    PythonAdapter("solve"),
                    None,
                )

    def test_bounds_sql_rows_and_work(self) -> None:
        inputs: JsonValue = [[[index] for index in range(120)]]
        with self.assertRaisesRegex(TraceRunError, "SQL row count exceeds limit"):
            run_enrolled(
                b"SELECT a.value FROM scores a CROSS JOIN scores b", SQL, inputs
            )
        with self.assertRaisesRegex(TraceRunError, "interrupted"):
            run_enrolled(
                b"SELECT a.value FROM scores a CROSS JOIN scores b CROSS JOIN scores c "
                b"WHERE a.value + b.value + c.value < 0",
                SQL,
                inputs,
            )

    def test_unavailable_isolation_stops_before_receiving_evidence_request(
        self,
    ) -> None:
        with (
            patch(
                "scripts.curriculum_trace.confine", side_effect=IsolationError("test")
            ),
            patch("scripts.curriculum_trace.sys.stdin") as stdin,
            patch(
                "scripts.curriculum_trace.sys.stderr", new_callable=io.StringIO
            ) as stderr,
        ):
            self.assertEqual(_child(io.BytesIO()), 1)
        stdin.buffer.read.assert_not_called()
        self.assertIn("isolation unavailable", stderr.getvalue())

    def test_bounds_frame_bytes(self) -> None:
        source = b"def solve(case, emit):\n    emit({'data': 'x' * 1_048_577})\n"
        with self.assertRaisesRegex(TraceRunError, "frames exceed byte limit"):
            run_enrolled(source, PythonAdapter("solve"), None)

    def test_python_session_adapters_can_use_stdlib_dataclasses(self) -> None:
        source = b"""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Counter:
    value: int

    def increment(self):
        self.value += 1
        return self.value

def solve(case, emit):
    counter = Counter(7)
    return [counter.increment() for _ in case]
"""
        run = run_enrolled(source, PythonAdapter("solve"), [0, 0, 0])
        self.assertEqual(run.result, [8, 9, 10])

    def test_stdout_cannot_supply_evidence_when_child_exits_early(self) -> None:
        source = b"""
import os

def solve(case, emit):
    print('{"result":1,"frames":[],"post_state":null}', flush=True)
    os._exit(0)
"""
        with self.assertRaisesRegex(TraceRunError, "invalid execution response"):
            run_enrolled(source, PythonAdapter("solve"), None)

    def test_normal_stdout_does_not_corrupt_evidence(self) -> None:
        source = b"def solve(case, emit):\n    print('diagnostic')\n    return 7\n"
        actual = run_enrolled(source, PythonAdapter("solve"), None)
        self.assertEqual(actual.result, 7)

    def test_parent_checks_trace_limits_even_when_transport_fits(self) -> None:
        cases: list[tuple[JsonValue, list[JsonValue], str]] = [
            (None, [{}] * 2001, "frame count exceeds limit"),
            ("x" * 1_048_560, [{}], "trace evidence exceeds byte limit"),
        ]
        for result, frames, error in cases:
            response = json.dumps(
                {"result": result, "frames": frames, "post_state": None}
            ).encode()
            with (
                self.subTest(error=error),
                patch("scripts.curriculum_trace.subprocess.run") as process,
                self.assertRaisesRegex(TraceRunError, error),
            ):

                def write_evidence(
                    command: list[str],
                    *,
                    stdout: BinaryIO,
                    payload: bytes = response,
                    **_options: object,
                ) -> subprocess.CompletedProcess[bytes]:
                    stdout.write(payload)
                    return subprocess.CompletedProcess(command, 0)

                process.side_effect = write_evidence
                run_enrolled(b"", PythonAdapter("solve"), None)

    def test_caught_frame_limit_still_rejects_execution(self) -> None:
        source = b"""
def solve(case, emit):
    for _ in range(2001):
        try:
            emit({})
        except RuntimeError:
            break
    return 42
"""
        with self.assertRaisesRegex(TraceRunError, "frame count exceeds limit"):
            run_enrolled(source, PythonAdapter("solve"), None)


if __name__ == "__main__":
    unittest.main()
