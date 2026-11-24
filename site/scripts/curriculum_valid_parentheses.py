"""Check bracket-stack evidence by canceling adjacent matching pairs."""

import re
from collections.abc import Iterator

from .curriculum_evidence import EvidenceError, equal_json, fields, integer, text
from .curriculum_trace import JsonValue, TraceRun

_PAIRS = re.compile(r"\(\)|\[\]|\{\}")
_CLOSERS = ")]}"


def _reduce(value: str) -> str:
    while True:
        reduced = _PAIRS.sub("", value)
        if reduced == value:
            return reduced
        value = reduced


def _prefix_states(value: str) -> Iterator[tuple[str, str]]:
    residue = ""
    for index, bracket in enumerate(value):
        # Cancel pairs in each prefix without replaying its earlier cancellations.
        residue = _reduce(residue + bracket)
        if any(closer in residue for closer in _CLOSERS):
            # The rejected closer has no legal cancellation and stays off the stack.
            yield f"reject-{index}", residue[:-1]
            return
        operation = "pop" if bracket in _CLOSERS else "push"
        yield f"{operation}-{index}", residue
    yield "finish", residue


def verify_stack(case: JsonValue, run: TraceRun) -> None:
    data = fields(case, "Valid Parentheses input", "s")
    value = text(data["s"], "bracket string")
    integer(len(value), 1, 10_000, "bracket string length")
    if any(bracket not in "()[]{}" for bracket in value):
        raise EvidenceError("Valid Parentheses input must contain only brackets")
    if not equal_json(run.result, _reduce(value) == ""):
        raise EvidenceError("Valid Parentheses result differs from pair reduction")
    if not equal_json(run.post_state, case):
        raise EvidenceError("Valid Parentheses execution mutated its input")
    count = 0
    for count, (step, residue) in enumerate(_prefix_states(value), 1):
        if count > len(run.frames):
            raise EvidenceError("Valid Parentheses frame count omits steps")
        frame = run.frames[count - 1]
        if frame["stepId"] != step or not equal_json(
            frame["state"], {"kind": "stack", "items": list(residue)}
        ):
            raise EvidenceError(
                f"Valid Parentheses frame {count} differs from pair reduction"
            )
    if count != len(run.frames):
        raise EvidenceError("Valid Parentheses frame count includes extra steps")
