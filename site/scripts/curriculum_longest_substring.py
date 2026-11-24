"""Reconstruct sliding-window evidence from distinct suffixes of each prefix."""

from collections.abc import Iterator

from .curriculum_evidence import EvidenceError, equal_json, fields, integer
from .curriculum_trace import JsonValue, TraceRun


def _suffix_starts(value: str) -> Iterator[int]:
    for right in range(len(value)):
        seen: set[str] = set()
        for position in range(right, -1, -1):
            character = value[position]
            if character in seen:
                yield position + 1
                break
            seen.add(character)
        else:
            yield 0


def _verify(case: JsonValue, run: TraceRun, evict_one_at_a_time: bool) -> None:
    data = fields(case, "Longest Substring input", "s")
    value = data["s"]
    if not isinstance(value, str):
        raise EvidenceError("Longest Substring input must be a string")
    integer(len(value), 0, 100_000, "substring input length")
    if not equal_json(run.post_state, case):
        raise EvidenceError("Longest Substring execution mutated its input")

    items: JsonValue = {"kind": "array", "items": list(value)}
    count = left = best = 0

    def check(step: str, start: int, stop: int) -> None:
        nonlocal count
        if count >= len(run.frames):
            raise EvidenceError("Longest Substring frame count omits steps")
        frame = run.frames[count]
        count += 1
        if (
            frame["stepId"] != step
            or not equal_json(frame["state"], items)
            or not equal_json(
                frame["highlights"], [{"index": index} for index in range(start, stop)]
            )
        ):
            raise EvidenceError(
                f"Longest Substring frame {count} differs from its suffix"
            )

    for right, start in enumerate(_suffix_starts(value)):
        if evict_one_at_a_time:
            for removed in range(left, start):
                check(f"evict-{right}-{removed}", removed + 1, right)
        elif start > left:
            check(f"jump-{right}", start, right)
        left = start
        best = max(best, right - left + 1)
        check(f"accept-{right}", left, right + 1)
    check("finish", left, len(value))
    if count != len(run.frames):
        raise EvidenceError("Longest Substring frame count includes extra steps")
    if not equal_json(run.result, best):
        raise EvidenceError("Longest Substring result differs from the suffix lengths")


def verify_eviction(case: JsonValue, run: TraceRun) -> None:
    _verify(case, run, evict_one_at_a_time=True)


def verify_jump(case: JsonValue, run: TraceRun) -> None:
    _verify(case, run, evict_one_at_a_time=False)
