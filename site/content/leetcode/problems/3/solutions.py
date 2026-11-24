"""Find the longest distinct substring with two sliding-window strategies."""

from collections.abc import Callable
from typing import TypedDict

type Json = int | str | list[Json] | dict[str, Json]
type Emit = Callable[[dict[str, Json]], None]


class Case(TypedDict):
    s: str


def _frame(
    emit: Emit, value: str, window: range, step: str, line: int, note: str
) -> None:
    emit(
        {
            "stepId": step,
            "codeLines": [line],
            "explanation": note,
            "state": {"kind": "array", "items": list(value)},
            "highlights": [{"index": index} for index in window],
        }
    )


def set_eviction(case: Case, emit: Emit | None = None) -> int:
    value = case["s"]
    window: set[str] = set()
    left = best = 0
    for right, character in enumerate(value):
        while character in window:
            removed = value[left]
            window.remove(removed)
            left += 1
            if emit is not None:
                _frame(
                    emit,
                    value,
                    range(left, right),
                    f"evict-{right}-{left - 1}",
                    36,
                    f"Remove {removed!r} at index {left - 1} before adding "
                    f"{character!r} at index {right}.",
                )
        window.add(character)
        best = max(best, right - left + 1)
        if emit is not None:
            _frame(
                emit,
                value,
                range(left, right + 1),
                f"accept-{right}",
                48,
                f"Include {character!r} at index {right}. Best length is {best}.",
            )
    if emit is not None:
        _frame(emit, value, range(left, len(value)), "finish", 60, f"Return {best}.")
    return best


def last_seen_jump(case: Case, emit: Emit | None = None) -> int:
    value = case["s"]
    last_seen: dict[str, int] = {}
    left = best = 0
    for right, character in enumerate(value):
        previous = last_seen.get(character, -1)
        outside = 0 <= previous < left
        # An occurrence before left is already outside the active window.
        if previous >= left:
            left = previous + 1
            if emit is not None:
                _frame(
                    emit,
                    value,
                    range(left, right),
                    f"jump-{right}",
                    72,
                    f"The previous {character!r} is at index {previous}. "
                    f"Move the left boundary to {left}.",
                )
        last_seen[character] = right
        best = max(best, right - left + 1)
        if emit is not None:
            note = f"Include {character!r} at index {right}. Best length is {best}."
            if outside:
                note = f"The previous occurrence at index {previous} is outside the window. {note}"
            _frame(emit, value, range(left, right + 1), f"accept-{right}", 84, note)
    if emit is not None:
        _frame(emit, value, range(left, len(value)), "finish", 92, f"Return {best}.")
    return best
