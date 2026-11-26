"""Run only source bytes the curriculum registry has reviewed and enrolled."""

import base64
import importlib
import json
import math
import os
import random
import sqlite3
import subprocess
import sys
import tempfile
from collections.abc import Callable
from contextlib import closing
from dataclasses import asdict, dataclass
from pathlib import Path
from types import ModuleType
from typing import BinaryIO, cast

from .curriculum_isolation import IsolationError, confine

# Warm the standard-library modules available to the curated snippets before
# isolation. An uncached import cannot read its module from disk once confined.
_PYTHON_MODULES = (
    "__future__",
    "bisect",
    "collections",
    "functools",
    "heapq",
    "itertools",
    "socket",
)
_TRACE_BYTES = 1_048_576
_MESSAGE_BYTES = 2 * _TRACE_BYTES
_MAX_FRAMES = 2000
_MAX_SQL_ROWS = 10_000
_SQL_PROGRESS_INTERVAL = 1000
_SQL_PROGRESS_BUDGET = 2000

type JsonValue = (
    bool | int | float | str | None | list[JsonValue] | dict[str, JsonValue]
)
type Frame = dict[str, JsonValue]


class TraceRunError(RuntimeError):
    """An enrolled implementation could not produce bounded execution evidence."""


@dataclass(frozen=True)
class PythonAdapter:
    entrypoint: str


@dataclass(frozen=True)
class SqlAdapter:
    setup: tuple[str, ...]
    inserts: tuple[str, ...]
    code_lines: tuple[int, ...]
    explanation: str
    functions: tuple[str, ...] = ()


@dataclass(frozen=True)
class TraceRun:
    result: JsonValue
    frames: list[Frame]
    post_state: JsonValue


def run_enrolled(
    source: bytes,
    adapter: PythonAdapter | SqlAdapter,
    case: JsonValue,
    *,
    timeout: float = 3.0,
) -> TraceRun:
    """Execute reviewed bytes and return evidence for the caller to verify."""
    if not math.isfinite(timeout) or not 0 < timeout <= 10:
        raise TraceRunError("timeout must be between 0 and 10 seconds")
    if isinstance(adapter, PythonAdapter):
        language = "python"
    elif isinstance(adapter, SqlAdapter):
        language = "sql"
    else:
        raise TraceRunError("unknown execution adapter")
    try:
        _require_portable(case)
        request = _encode(
            {
                "source": base64.b64encode(source).decode("ascii"),
                "language": language,
                "adapter": asdict(adapter),
                "case": case,
            }
        )
    except (TypeError, ValueError, RecursionError) as exc:
        raise TraceRunError("could not encode execution request") from exc
    if len(request) > _MESSAGE_BYTES:
        raise TraceRunError("execution request exceeds byte limit")
    try:
        with (
            tempfile.TemporaryDirectory(prefix="curriculum-trace-") as cwd,
            tempfile.TemporaryFile() as evidence,
            tempfile.TemporaryFile() as stderr,
        ):
            process = subprocess.run(
                [sys.executable, "-B", "-P", "-S", "-m", "scripts.curriculum_trace"],
                input=request,
                stdout=evidence,
                stderr=stderr,
                env={
                    "PYTHONHASHSEED": "0",
                    "PYTHONPATH": str(Path(__file__).resolve().parents[1]),
                    "LC_ALL": "C",
                    "TZ": "UTC",
                },
                cwd=cwd,
                timeout=timeout,
                check=False,
            )
            if process.returncode:
                stderr.seek(0)
                detail = stderr.read(512).decode("utf-8", "replace").strip()
                raise TraceRunError(
                    f"execution failed ({process.returncode}): {detail}"
                )
            evidence.seek(0)
            response = evidence.read(_MESSAGE_BYTES + 1)
    except subprocess.TimeoutExpired as exc:
        raise TraceRunError("execution timed out") from exc
    except OSError as exc:
        raise TraceRunError("could not launch isolated execution") from exc
    if len(response) > _MESSAGE_BYTES:
        raise TraceRunError("execution response exceeds byte limit")
    try:
        decoded = json.loads(response)
        if not isinstance(decoded, dict) or decoded.keys() != {
            "result",
            "frames",
            "post_state",
        }:
            raise TraceRunError("invalid execution response fields")
        if not isinstance(decoded["frames"], list) or any(
            not isinstance(frame, dict) for frame in decoded["frames"]
        ):
            raise TraceRunError("invalid execution response frames")
        result, frames = decoded["result"], decoded["frames"]
        if len(frames) > _MAX_FRAMES:
            raise TraceRunError("frame count exceeds limit")
        _check_trace_bytes(result, frames)
        return TraceRun(
            result=result,
            frames=frames,
            post_state=decoded["post_state"],
        )
    except (ValueError, RecursionError) as exc:
        raise TraceRunError("invalid execution response") from exc


def _encode(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, allow_nan=False, separators=(",", ":")
    ).encode("utf-8")


def _check_trace_bytes(result: JsonValue, frames: list[Frame]) -> None:
    if len(_encode({"result": result, "frames": frames})) > _TRACE_BYTES:
        raise TraceRunError("trace evidence exceeds byte limit")


def _require_portable(value: object) -> None:
    if value is None or isinstance(value, (bool, str, int, float)):
        return
    if isinstance(value, list):
        for item in value:
            _require_portable(item)
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise TraceRunError("JSON object keys must be strings")
            _require_portable(item)
        return
    raise TraceRunError("execution evidence must be portable JSON")


class _Frames:
    def __init__(self) -> None:
        self.frames: list[Frame] = []
        self.bytes = 0
        self.error: Exception | None = None

    def emit(self, frame: Frame) -> None:
        if self.error is not None:
            raise self.error
        try:
            if len(self.frames) >= _MAX_FRAMES:
                raise TraceRunError("frame count exceeds limit")
            if not isinstance(frame, dict):
                raise TraceRunError("frame must be an object")
            _require_portable(frame)
            encoded = _encode(frame)
            self.bytes += len(encoded) + 1
            if self.bytes > _TRACE_BYTES:
                raise TraceRunError("frames exceed byte limit")
            # Copy now, before the implementation can mutate the supplied state.
            self.frames.append(json.loads(encoded))
        except (
            TraceRunError,
            ValueError,
            TypeError,
            RecursionError,
            MemoryError,
        ) as exc:
            self.error = exc
            raise


def _run_python(
    source: bytes, adapter: PythonAdapter, case: JsonValue, frames: _Frames
) -> JsonValue:
    module = ModuleType("__curriculum_lesson__")
    sys.modules[module.__name__] = module
    # Execute only registry-enrolled source after the OS restrictions are active.
    exec(  # noqa: S102
        compile(source, "<curriculum lesson>", "exec", dont_inherit=True),
        vars(module),
    )
    entrypoint = vars(module).get(adapter.entrypoint)
    if not callable(entrypoint):
        raise TraceRunError("reviewed Python entry point is missing")
    return cast(JsonValue, entrypoint(case, frames.emit))


def _run_sql(
    source: bytes, adapter: SqlAdapter, case: JsonValue, frames: _Frames
) -> JsonValue:
    if not isinstance(case, list) or len(case) != len(adapter.inserts):
        raise TraceRunError("SQL fixture groups must match the reviewed inserts")
    work = _SQL_PROGRESS_BUDGET

    def limit_work() -> int:
        nonlocal work
        work -= 1
        return int(work <= 0)

    with closing(sqlite3.connect(":memory:")) as connection:
        connection.setlimit(sqlite3.SQLITE_LIMIT_LENGTH, _TRACE_BYTES)
        connection.setlimit(sqlite3.SQLITE_LIMIT_SQL_LENGTH, _TRACE_BYTES)
        connection.execute("PRAGMA temp_store = MEMORY")
        for statement in adapter.setup:
            connection.execute(statement)
        for statement, rows in zip(adapter.inserts, case, strict=True):
            if not isinstance(rows, list) or any(
                not isinstance(row, list) for row in rows
            ):
                raise TraceRunError("SQL fixtures require lists of rows")
            connection.executemany(statement, cast(list[list[JsonValue]], rows))
        connection.set_authorizer(_sql_authorizer(adapter.functions))
        connection.set_progress_handler(limit_work, _SQL_PROGRESS_INTERVAL)
        cursor = connection.execute(source.decode("utf-8"))
        if cursor.description is None:
            raise TraceRunError("SQL implementation must return a table")
        columns: list[JsonValue] = [column[0] for column in cursor.description]
        results: list[JsonValue] = []
        size = len(_encode(columns))
        for row in cursor:
            if len(results) >= _MAX_SQL_ROWS:
                raise TraceRunError("SQL row count exceeds limit")
            values: list[JsonValue] = list(row)
            size += len(_encode(values)) + 1
            if size > _TRACE_BYTES:
                raise TraceRunError("SQL result exceeds byte limit")
            results.append(values)
    table: dict[str, JsonValue] = {"columns": columns, "rows": results}
    frames.emit(
        {
            "stepId": "query-result",
            "codeLines": list(adapter.code_lines),
            "explanation": adapter.explanation,
            "state": {"kind": "table", **table},
            "highlights": [],
        }
    )
    return table


def _sql_authorizer(
    functions: tuple[str, ...],
) -> Callable[[int, str | None, str | None, str | None, str | None], int]:
    def authorize(
        action: int,
        _first: str | None,
        second: str | None,
        _db: str | None,
        _origin: str | None,
    ) -> int:
        if action in {sqlite3.SQLITE_SELECT, sqlite3.SQLITE_READ}:
            return sqlite3.SQLITE_OK
        if (
            action == sqlite3.SQLITE_FUNCTION
            and second in functions
            and second != "load_extension"
        ):
            return sqlite3.SQLITE_OK
        return sqlite3.SQLITE_DENY

    return authorize


def _child(evidence: BinaryIO) -> int:
    try:
        for module in _PYTHON_MODULES:
            importlib.import_module(module)
        random.seed(0)
        # Resolve the backend and confine before decoding/compiling lesson inputs.
        confine(_MESSAGE_BYTES)
    except IsolationError as exc:
        print(f"isolation unavailable: {exc}", file=sys.stderr)
        return 1
    try:
        raw = sys.stdin.buffer.read(_MESSAGE_BYTES + 1)
        if len(raw) > _MESSAGE_BYTES:
            raise TraceRunError("execution request exceeds byte limit")
        request = json.loads(raw)
        source = base64.b64decode(request["source"], validate=True)
        case = request["case"]
        frames = _Frames()
        if request["language"] == "python":
            result = _run_python(
                source, PythonAdapter(**request["adapter"]), case, frames
            )
        elif request["language"] == "sql":
            result = _run_sql(source, SqlAdapter(**request["adapter"]), case, frames)
        else:
            raise TraceRunError("unsupported execution language")
        if frames.error is not None:
            raise frames.error
        _require_portable(result)
        _require_portable(case)
        _check_trace_bytes(result, frames.frames)
        output = _encode(
            {"result": result, "frames": frames.frames, "post_state": case}
        )
        if len(output) > _MESSAGE_BYTES:
            raise TraceRunError("execution response exceeds byte limit")
        evidence.write(output)
        evidence.flush()
    # Report ordinary lesson failures through the bounded diagnostics stream.
    except Exception as exc:  # noqa: BLE001
        print(f"{type(exc).__name__}: {str(exc)[:256]}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    # Reserve the original stdout file for evidence before confining this child.
    with os.fdopen(os.dup(sys.stdout.fileno()), "wb") as evidence:
        os.dup2(sys.stderr.fileno(), sys.stdout.fileno())
        raise SystemExit(_child(evidence))
