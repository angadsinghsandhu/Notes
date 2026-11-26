"""Verify checked-in curriculum evidence using explicitly reviewed implementations.

Examples are a v1 object with an examples array. Each example contains id,
input, result and postState. Approaches may select separate IDs for cases
with different mutation contracts. Each must pass its declared example IDs
and publish at least one trace drawn from those IDs.
"""

import argparse
import json
import re
import sys
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.curriculum_evidence import (
    EVIDENCE_BYTES,
    TRACE_BYTES,
    EvidenceError,
    array,
    digest,
    equal_json,
    fields,
    integer,
    obj,
    open_curriculum,
    parse_json,
    read_bytes,
    require_portable,
    slug,
    source_line_count,
    text,
    validate_trace,
)
from scripts.curriculum_trace import (
    JsonValue,
    PythonAdapter,
    SqlAdapter,
    TraceRun,
    TraceRunError,
    run_enrolled,
)
from scripts.curriculum_two_sum import verify_hash, verify_pairs, verify_sorted

_SITE = Path(__file__).resolve().parents[1]
_LAST_PROBLEM = 2000
_STATUSES = ("planned", "draft", "verified")


@dataclass(frozen=True)
class Enrollment:
    path: str
    sha256: str
    adapter: PythonAdapter | SqlAdapter
    # Receives the unmodified input and actual run, never the declared answers.
    verify: Callable[[JsonValue, TraceRun], None]


type Registry = Mapping[tuple[int, str], Enrollment]
# Add exact source pins and independent checks only after reviewing the implementation.
_TWO_SUM_SHA256 = "b1fde0a1e87d41e1bf480d836c111ccc22b743d53e7dce8a1e0e2b901253f825"
_ENROLLED: Registry = {
    (1, "pair-enumeration"): Enrollment(
        "solutions.py", _TWO_SUM_SHA256, PythonAdapter("pair_enumeration"), verify_pairs
    ),
    (1, "sorted-two-pointers"): Enrollment(
        "solutions.py",
        _TWO_SUM_SHA256,
        PythonAdapter("sorted_two_pointers"),
        verify_sorted,
    ),
    (1, "complement-hash"): Enrollment(
        "solutions.py", _TWO_SUM_SHA256, PythonAdapter("complement_hash"), verify_hash
    ),
}


@dataclass(frozen=True)
class Manifest:
    statuses: dict[str, list[int]]
    lessons: list[int]


def _selection(value: str, prefix: str = "") -> int:
    if not re.fullmatch(r"[1-9][0-9]{0,3}", value) or int(value) > _LAST_PROBLEM:
        raise EvidenceError(f"invalid {prefix}frontend number {value!r}")
    return int(value)


def _distinct[T](items: list[T], label: str) -> list[T]:
    if len(set(items)) != len(items):
        raise EvidenceError(f"duplicate {label}")
    return items


def _manifest(root: int) -> Manifest:
    value = fields(
        parse_json(read_bytes(root, "manifest.json", EVIDENCE_BYTES)),
        "manifest",
        "version",
        "problems",
        "lessons",
        "paths",
    )
    integer(value["version"], 1, 1, "manifest version")
    statuses: dict[str, list[int]] = {status: [] for status in _STATUSES}
    seen: set[int] = set()
    for item in array(value["problems"], "manifest problems"):
        problem = obj(item, "manifest problem")
        number = integer(problem.get("number"), 1, _LAST_PROBLEM, "problem number")
        if number in seen or problem.get("id") != f"leetcode:{number}":
            raise EvidenceError(
                f"invalid or duplicate manifest identity leetcode:{number}"
            )
        status = text(problem.get("status"), "problem status")
        if status not in statuses:
            raise EvidenceError(f"invalid manifest status for leetcode:{number}")
        statuses[status].append(number)
        seen.add(number)
    missing = sorted(set(range(1, _LAST_PROBLEM + 1)) - seen)
    if missing:
        raise EvidenceError(
            f"manifest must list every ID 1–2000; first missing ID {missing[0]}"
        )
    lessons: list[int] = []
    for item in array(value["lessons"], "manifest lessons"):
        identity = text(item, "lesson ID")
        if not identity.startswith("leetcode:"):
            raise EvidenceError(f"invalid lesson identity {identity}")
        lessons.append(_selection(identity.removeprefix("leetcode:"), "lesson "))
    _distinct(lessons, "manifest lesson")
    if set(lessons) != set(statuses["draft"] + statuses["verified"]):
        raise EvidenceError(
            "manifest lesson IDs must match the draft and verified identities"
        )
    return Manifest(
        {status: sorted(numbers) for status, numbers in statuses.items()},
        sorted(lessons),
    )


def inventory(site: Path) -> dict[str, list[int]] | None:
    with open_curriculum(site) as root:
        return None if root is None else _manifest(root).statuses


def _evidence(
    root: int, prefix: str, evidence: dict[str, JsonValue], limit: int
) -> bytes:
    path = text(evidence.get("path"), "evidence path")
    raw = read_bytes(root, prefix + path, limit)
    if digest(raw) != evidence.get("sha256"):
        raise EvidenceError(f"{prefix}{path} does not match its SHA256 evidence")
    return raw


def _verify_example(
    example: dict[str, JsonValue],
    trace: dict[str, JsonValue] | None,
    source: bytes,
    enrollment: Enrollment,
) -> None:
    run = run_enrolled(source, enrollment.adapter, example["input"])
    require_portable(run.result)
    require_portable(run.post_state)
    for frame in run.frames:
        require_portable(frame)
    if not equal_json(run.result, example["result"]):
        raise EvidenceError("executed result differs from example result")
    if not equal_json(run.post_state, example["postState"]):
        raise EvidenceError("executed post-state differs from example post-state")
    if trace is None:
        enrollment.verify(example["input"], run)
        return
    if not equal_json(run.result, trace["result"]):
        raise EvidenceError("executed result differs from trace result")
    frames = array(trace["frames"], "trace frames")
    if len(run.frames) != len(frames):
        raise EvidenceError("executed frame count differs from trace")
    for index, (actual, committed) in enumerate(
        zip(run.frames, frames, strict=True), 1
    ):
        if not equal_json(actual, committed):
            raise EvidenceError(f"executed frame {index} differs from trace")
    enrollment.verify(example["input"], run)


def _check_approach(
    root: int,
    number: int,
    approach_id: str,
    approach: dict[str, JsonValue],
    examples: dict[str, dict[str, JsonValue]],
    examples_digest: str,
    registry: Registry,
) -> None:
    enrollment = registry.get((number, approach_id))
    if enrollment is None:
        raise EvidenceError("no reviewed execution enrollment")
    implementation = fields(
        approach.get("implementation"), "implementation", "path", "sha256", "entryPoint"
    )
    adapter = enrollment.adapter
    language, entry = (
        ("python", adapter.entrypoint)
        if isinstance(adapter, PythonAdapter)
        else ("sql", None)
    )
    extension = ".py" if language == "python" else ".sql"
    if (
        approach.get("language") != language
        or implementation["path"] != enrollment.path
        or not enrollment.path.endswith(extension)
        or implementation["sha256"] != enrollment.sha256
        or implementation["entryPoint"] != entry
    ):
        raise EvidenceError("implementation differs from reviewed execution enrollment")
    prefix = f"problems/{number}/"
    source = _evidence(root, prefix, implementation, TRACE_BYTES)
    lines = source_line_count(source)

    verification = fields(
        approach.get("verification"),
        "verification evidence",
        "implementationSha256",
        "entryPoint",
        "examplesSha256",
        "passedExampleIds",
        "checkedOn",
    )
    if (
        verification["implementationSha256"] != enrollment.sha256
        or verification["entryPoint"] != entry
        or verification["examplesSha256"] != examples_digest
    ):
        raise EvidenceError(
            "verification does not bind current source, entry point and examples"
        )
    passed = _distinct(
        [
            slug(item, "passed example ID")
            for item in array(verification["passedExampleIds"], "passed example IDs")
        ],
        "passed example ID",
    )
    if not passed or not set(passed) <= examples.keys():
        raise EvidenceError(
            "verification must name reviewed examples from examples.json"
        )

    traces: dict[str, dict[str, JsonValue]] = {}
    for item in array(approach.get("traces"), "trace evidence"):
        evidence = fields(
            item,
            "trace evidence",
            "path",
            "sha256",
            "exampleId",
            "implementationSha256",
        )
        example_id = slug(evidence["exampleId"], "trace example ID")
        if (
            example_id in traces
            or example_id not in passed
            or evidence["implementationSha256"] != enrollment.sha256
            or evidence["path"] != f"traces/{approach_id}/{example_id}.json"
        ):
            raise EvidenceError(f"inconsistent trace evidence for {example_id}")
        trace = obj(parse_json(_evidence(root, prefix, evidence, TRACE_BYTES)), "trace")
        validate_trace(trace, lines)
        if (
            trace["problemId"] != f"leetcode:{number}"
            or trace["approachId"] != approach_id
            or trace["exampleId"] != example_id
            or trace["implementationSha256"] != enrollment.sha256
        ):
            raise EvidenceError(
                f"trace identity disagrees with evidence for {example_id}"
            )
        traces[example_id] = trace
    if not traces:
        raise EvidenceError("at least one trace is required")
    for example_id in passed:
        try:
            _verify_example(
                examples[example_id], traces.get(example_id), source, enrollment
            )
        except (TraceRunError, ValueError, RecursionError) as exc:
            raise EvidenceError(f"{example_id}: {exc}") from exc


def _check_lesson(
    root: int, number: int, explicit: bool, verified: bool, registry: Registry
) -> bool:
    prefix = f"problems/{number}/"
    lesson = obj(
        parse_json(read_bytes(root, prefix + "metadata.json", EVIDENCE_BYTES)), "lesson"
    )
    if lesson.get("problemId") != f"leetcode:{number}" or "prose" not in lesson:
        raise EvidenceError("invalid lesson identity or missing prose declaration")
    if lesson["prose"] is not None:
        _evidence(
            root,
            prefix,
            fields(lesson["prose"], "prose", "path", "sha256"),
            EVIDENCE_BYTES,
        )
    elif verified:
        raise EvidenceError("verified lesson requires prose")
    elif not explicit:
        return False
    approaches = [
        obj(item, "approach") for item in array(lesson.get("approaches"), "approaches")
    ]
    ids = _distinct(
        [slug(approach.get("id"), "approach ID") for approach in approaches],
        "approach ID",
    )
    if not ids:
        if explicit or verified:
            raise EvidenceError("no approaches to verify")
        return False
    examples_file = fields(
        lesson.get("examples"), "examples evidence", "path", "sha256"
    )
    if examples_file["path"] != "examples.json":
        raise EvidenceError("examples must use the canonical examples.json path")
    raw = _evidence(root, prefix, examples_file, EVIDENCE_BYTES)
    envelope = fields(parse_json(raw), "examples file", "version", "examples")
    integer(envelope["version"], 1, 1, "examples version")
    examples: dict[str, dict[str, JsonValue]] = {}
    for value in array(envelope["examples"], "examples"):
        example = fields(value, "example", "id", "input", "result", "postState")
        example_id = slug(example["id"], "example ID")
        if example_id in examples:
            raise EvidenceError(f"duplicate example ID {example_id}")
        examples[example_id] = example
    for approach_id, approach in zip(ids, approaches, strict=True):
        try:
            _check_approach(
                root, number, approach_id, approach, examples, digest(raw), registry
            )
        except (ValueError, RecursionError) as exc:
            raise EvidenceError(f"{approach_id}: {exc}") from exc
    return True


def check(
    site: Path, ids: Sequence[int] | None = None, registry: Registry = _ENROLLED
) -> int | None:
    with open_curriculum(site) as root:
        if root is None:
            if ids is not None:
                raise EvidenceError("no curriculum exists for the selected IDs")
            return None
        return _check_lessons(root, ids, registry)


def _check_lessons(root: int, ids: Sequence[int] | None, registry: Registry) -> int:
    manifest = _manifest(root)
    selected = manifest.lessons if ids is None else list(ids)
    if ids is not None and not selected:
        raise EvidenceError("empty explicit curriculum selection")
    count = 0
    lessons = set(manifest.lessons)
    verified_ids = set(manifest.statuses["verified"])
    for number in _distinct(selected, "selected problem ID"):
        try:
            if number not in lessons:
                raise EvidenceError("no authoring evidence")
            count += _check_lesson(
                root,
                number,
                ids is not None,
                number in verified_ids,
                registry,
            )
        except EvidenceError as exc:
            raise EvidenceError(f"leetcode:{number}: {exc}") from exc
    return count


def _ids(raw: str) -> list[int]:
    try:
        return _distinct([_selection(item) for item in raw.split(",")], "selected ID")
    except EvidenceError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("inventory")
    commands.add_parser("check").add_argument("--ids", type=_ids)
    args = parser.parse_args(argv)
    try:
        if args.command == "inventory":
            statuses = inventory(_SITE)
            if statuses is None:
                print("No curriculum exists yet; no verified lessons.")
            else:
                print(json.dumps(statuses))
        else:
            count = check(_SITE, args.ids)
            if count is None:
                print("No curriculum exists yet; no verified lessons.")
            else:
                print(f"Verified execution evidence for {count} lesson(s).")
    except (EvidenceError, OSError) as exc:
        print(f"Curriculum evidence check failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
