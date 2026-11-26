"""Three approaches to Two Sum, with optional execution snapshots."""

from collections.abc import Callable
from typing import TypedDict

type Json = None | int | str | list[Json] | dict[str, Json]
type Emit = Callable[[dict[str, Json]], None]


class Case(TypedDict):
    nums: list[int]
    target: int


def _array_frame(
    emit: Emit, step: str, line: int, explanation: str, items: list[int], *indices: int
) -> None:
    emit(
        {
            "stepId": step,
            "codeLines": [line],
            "explanation": explanation,
            "state": {"kind": "array", "items": list(items)},
            "highlights": [{"index": index} for index in indices],
        }
    )


def _table_frame(
    emit: Emit,
    step: str,
    line: int,
    explanation: str,
    columns: list[str],
    entries: list[tuple[int, int]],
    *rows: int,
) -> None:
    emit(
        {
            "stepId": step,
            "codeLines": [line],
            "explanation": explanation,
            "state": {
                "kind": "table",
                "columns": list(columns),
                "rows": [[value, position] for value, position in entries],
            },
            "highlights": [{"row": row, "column": 0} for row in rows],
        }
    )


def pair_enumeration(case: Case, emit: Emit | None = None) -> list[int]:
    nums, target = case["nums"], case["target"]
    # Visiting only right > left considers each pair once and forbids self-matches.
    for left in range(len(nums)):
        for right in range(left + 1, len(nums)):
            total = nums[left] + nums[right]
            if emit is not None:
                _array_frame(
                    emit,
                    f"compare-{left}-{right}",
                    58,
                    f"Positions {left} and {right} sum to {total}. Target is {target}.",
                    nums,
                    left,
                    right,
                )
            if total == target:
                return [left, right]
    raise ValueError("Input must contain a solution.")


def sorted_two_pointers(case: Case, emit: Emit | None = None) -> list[int]:
    nums, target = case["nums"], case["target"]
    ordered = sorted((value, index) for index, value in enumerate(nums))
    columns = ["Value", "Original index"]
    left, right = 0, len(ordered) - 1
    if emit is not None:
        _table_frame(
            emit,
            "sort",
            76,
            "Sort by value and keep each original index.",
            columns,
            ordered,
            left,
            right,
        )
    step = 0
    while left < right:
        low, first = ordered[left]
        high, second = ordered[right]
        total = low + high
        if emit is not None:
            _table_frame(
                emit,
                f"compare-{step}",
                94,
                f"Endpoint values {low} and {high} sum to {total}. Target is {target}.",
                columns,
                ordered,
                left,
                right,
            )
        if total == target:
            return [min(first, second), max(first, second)]
        # The left endpoint cannot reach a larger sum with any remaining value.
        if total < target:
            left += 1
            move_line = 110
            reason = "Sum is too small. Drop the left endpoint."
        else:
            # The right endpoint cannot reach a smaller sum within this interval.
            right -= 1
            move_line = 115
            reason = "Sum is too large. Drop the right endpoint."
        if emit is not None:
            _table_frame(
                emit,
                f"move-{step}",
                move_line,
                reason,
                columns,
                ordered,
                left,
                right,
            )
        step += 1
    raise ValueError("Input must contain a solution.")


def complement_hash(case: Case, emit: Emit | None = None) -> list[int]:
    nums, target = case["nums"], case["target"]
    seen: dict[int, int] = {}
    columns = ["Seen value", "Latest original index"]
    for index, value in enumerate(nums):
        needed = target - value
        # Look up first so the current index cannot be its own partner.
        earlier = seen.get(needed)
        if emit is not None:
            entries = list(seen.items())
            matches = tuple(
                row for row, (key, _) in enumerate(entries) if key == needed
            )
            outcome = (
                "No earlier match." if earlier is None else f"Found index {earlier}."
            )
            _table_frame(
                emit,
                f"lookup-{index}",
                140,
                f"Index {index} has {value} and needs {needed}. {outcome}",
                columns,
                entries,
                *matches,
            )
        if earlier is not None:
            return [earlier, index]
        seen[value] = index
        if emit is not None:
            entries = list(seen.items())
            row = next(row for row, (key, _) in enumerate(entries) if key == value)
            _table_frame(
                emit,
                f"record-{index}",
                160,
                f"Record {value} at index {index} for later lookups.",
                columns,
                entries,
                row,
            )
    raise ValueError("Input must contain a solution.")
