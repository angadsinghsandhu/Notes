"""Admit bounded, portable evidence before comparing it with execution."""

import hashlib
import json
import math
import os
import re
import stat
from collections.abc import Iterator
from contextlib import ExitStack, contextmanager
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import cast

from .curriculum_trace import JsonValue

TRACE_BYTES = 1_048_576
EVIDENCE_BYTES = 25 * TRACE_BYTES
SAFE_INTEGER = (1 << 53) - 1
_SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
_DIRECTORY_FLAGS = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
_PATH = re.compile(r"(?:[a-z0-9_-][a-z0-9._-]*/)*[a-z0-9_-][a-z0-9._-]*")


class EvidenceError(ValueError):
    """The curriculum could not substantiate its evidence."""


@contextmanager
def open_curriculum(site: Path) -> Iterator[int | None]:
    # Keep all reads anchored to the same open curriculum directory.
    with ExitStack() as opened:
        parent = os.open(site, _DIRECTORY_FLAGS)
        opened.callback(os.close, parent)
        for part in ("content", "leetcode"):
            try:
                parent = os.open(part, _DIRECTORY_FLAGS, dir_fd=parent)
            except FileNotFoundError:
                yield None
                return
            except OSError as exc:
                raise EvidenceError(
                    f"{part}: cannot open curriculum directory: {exc}"
                ) from exc
            opened.callback(os.close, parent)
        yield parent


def read_bytes(root: int, path: str, limit: int) -> bytes:
    if len(path) > 280 or not _PATH.fullmatch(path):
        raise EvidenceError(f"{path!r} is not a normalized evidence path")
    try:
        with ExitStack() as opened:
            parent = root
            parts = path.split("/")
            for part in parts[:-1]:
                parent = os.open(part, _DIRECTORY_FLAGS, dir_fd=parent)
                opened.callback(os.close, parent)
            file = os.open(
                parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent
            )
            opened.callback(os.close, file)
            info = os.fstat(file)
            if not stat.S_ISREG(info.st_mode):
                raise EvidenceError(f"{path} must be a regular file")
            if info.st_size > limit:
                raise EvidenceError(f"{path} exceeds its {limit}-byte limit")
            with open(file, "rb", closefd=False) as handle:
                data = handle.read(limit + 1)
            if len(data) > limit:
                raise EvidenceError(f"{path} exceeds its {limit}-byte limit")
            return data
    except OSError as exc:
        raise EvidenceError(f"{path}: cannot read contained evidence: {exc}") from exc


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def obj(value: JsonValue, label: str) -> dict[str, JsonValue]:
    if not isinstance(value, dict):
        raise EvidenceError(f"{label} must be an object")
    return value


def fields(value: JsonValue, label: str, *keys: str) -> dict[str, JsonValue]:
    record = obj(value, label)
    if record.keys() != set(keys):
        raise EvidenceError(f"{label} has invalid fields")
    return record


def array(value: JsonValue, label: str) -> list[JsonValue]:
    if not isinstance(value, list):
        raise EvidenceError(f"{label} must be an array")
    return value


def text(value: JsonValue, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise EvidenceError(f"{label} must be nonblank text")
    return value


def slug(value: JsonValue, label: str) -> str:
    if not isinstance(value, str) or not _SLUG.fullmatch(value):
        raise EvidenceError(f"{label} must be a slug")
    return value


def integer(value: JsonValue, low: int, high: int, label: str) -> int:
    if (
        not isinstance(value, int)
        or isinstance(value, bool)
        or not low <= value <= high
    ):
        raise EvidenceError(f"{label} must be an integer in {low}–{high}")
    return value


def _members(pairs: list[tuple[str, JsonValue]]) -> dict[str, JsonValue]:
    record: dict[str, JsonValue] = {}
    for key, value in pairs:
        if key in record:
            raise EvidenceError(f"duplicate JSON member {key!r}")
        record[key] = value
    return record


def _integer(raw: str) -> int:
    value = int(raw)
    if abs(value) > SAFE_INTEGER:
        raise EvidenceError(
            "unsafe JSON integer; encode larger exact integers as strings"
        )
    return value


def _decimal(raw: str) -> int | float:
    value = float(raw)
    if not math.isfinite(value) or Decimal(raw) != Decimal(str(value)):
        raise EvidenceError(f"nonportable JSON number {raw}")
    return _integer(str(int(value))) if value.is_integer() else value


def require_portable(value: JsonValue) -> None:
    if isinstance(value, str):
        value.encode("utf-8")
    elif isinstance(value, int):
        _integer(str(int(value)))
    elif isinstance(value, float):
        _decimal(str(value))
    elif isinstance(value, list):
        for item in value:
            require_portable(item)
    elif isinstance(value, dict):
        for key, item in value.items():
            key.encode("utf-8")
            require_portable(item)


def parse_json(raw: bytes) -> JsonValue:
    try:
        value = cast(
            JsonValue,
            json.loads(
                raw.decode("utf-8"),
                object_pairs_hook=_members,
                parse_int=_integer,
                parse_float=_decimal,
                parse_constant=_decimal,
            ),
        )
        require_portable(value)
    except EvidenceError:
        raise
    except (InvalidOperation, ValueError, RecursionError) as exc:
        raise EvidenceError(f"invalid portable JSON: {exc}") from exc
    return value


def equal_json(left: JsonValue, right: JsonValue) -> bool:
    if isinstance(left, bool) or isinstance(right, bool):
        return left is right
    if isinstance(left, list) and isinstance(right, list):
        return len(left) == len(right) and all(
            equal_json(a, b) for a, b in zip(left, right, strict=True)
        )
    if isinstance(left, dict) and isinstance(right, dict):
        return left.keys() == right.keys() and all(
            equal_json(value, right[key]) for key, value in left.items()
        )
    return left == right


def source_line_count(source: bytes) -> int:
    # Match playback normalization; a terminal newline does not add a line.
    normalized = source.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
    return normalized.count("\n") + int(
        bool(normalized) and not normalized.endswith("\n")
    )


def _number_text(value: float) -> str:
    if value.is_integer():
        return str(int(value))
    if abs(value) >= 1e-6:
        return format(Decimal(str(value)), "f")
    mantissa, exponent = str(value).split("e")
    return f"{mantissa}e{int(exponent)}"


def _compact_bytes(value: JsonValue) -> int:
    # Use the playback byte count, where JS writes 1e-7 and 0.000001.
    if isinstance(value, float):
        return len(_number_text(value))
    if isinstance(value, list):
        return 2 + max(0, len(value) - 1) + sum(map(_compact_bytes, value))
    if isinstance(value, dict):
        return (
            2
            + max(0, len(value) - 1)
            + sum(
                _compact_bytes(key) + 1 + _compact_bytes(item)
                for key, item in value.items()
            )
        )
    return len(json.dumps(value, ensure_ascii=False).encode("utf-8"))


def validate_trace(value: JsonValue, lines: int) -> None:
    trace = fields(
        value,
        "v1 trace",
        "version",
        "problemId",
        "approachId",
        "exampleId",
        "implementationSha256",
        "result",
        "frames",
    )
    integer(trace["version"], 1, 1, "trace version")
    frames = array(trace["frames"], "frames")
    if not 1 <= len(frames) <= 2000:
        raise EvidenceError("trace requires 1 to 2000 frames")
    try:
        require_portable(trace)
        if _compact_bytes(trace) > TRACE_BYTES:
            raise EvidenceError("trace exceeds the 1 MiB compact limit")
    except EvidenceError:
        raise
    except (ValueError, RecursionError) as exc:
        raise EvidenceError("trace is not portable JSON") from exc
    steps: set[str] = set()
    for item in frames:
        frame = fields(
            item, "frame", "stepId", "codeLines", "explanation", "state", "highlights"
        )
        step_id = slug(frame["stepId"], "step ID")
        if step_id in steps:
            raise EvidenceError(f"duplicate step ID {step_id}")
        steps.add(step_id)
        code_lines = [
            integer(line, 1, lines, "code lines")
            for line in array(frame["codeLines"], "code lines")
        ]
        if not code_lines or len(code_lines) != len(set(code_lines)):
            raise EvidenceError(f"{step_id} requires distinct code lines")
        text(frame["explanation"], "explanation")
        # The production build's TypeScript validator owns renderer payloads.
        obj(frame["state"], "frame state")
        array(frame["highlights"], "highlights")
