"""Validate bracket nesting, optionally emitting the stack after each step."""

from collections.abc import Callable
from typing import TypedDict

type Json = int | str | list[Json] | dict[str, Json]
type Emit = Callable[[dict[str, Json]], None]


class Case(TypedDict):
    s: str


def _frame(emit: Emit, step: str, line: int, note: str, stack: list[str]) -> None:
    emit(
        {
            "stepId": step,
            "codeLines": [line],
            "explanation": note,
            "state": {"kind": "stack", "items": list(stack)},
            "highlights": [{"index": len(stack) - 1}] if stack else [],
        }
    )


def valid_parentheses(case: Case, emit: Emit | None = None) -> bool:
    openings = {")": "(", "]": "[", "}": "{"}
    # The last element is the only opening the next closing bracket can match.
    stack: list[str] = []
    for index, bracket in enumerate(case["s"]):
        opening = openings.get(bracket)
        if opening is None:
            stack.append(bracket)
            if emit is not None:
                _frame(emit, f"push-{index}", 33, f"Push '{bracket}'.", stack)
            continue
        if not stack or stack[-1] != opening:
            if emit is not None:
                note = (
                    f"Reject '{bracket}' with no opening to match."
                    if not stack
                    else f"Reject '{bracket}'. The top '{stack[-1]}' cannot match it."
                )
                _frame(emit, f"reject-{index}", 37, note, stack)
            return False
        stack.pop()
        if emit is not None:
            _frame(
                emit,
                f"pop-{index}",
                46,
                f"'{bracket}' closes '{opening}'. Pop it.",
                stack,
            )

    balanced = not stack
    if emit is not None:
        note = (
            "The stack is empty." if balanced else "Some openings are still unmatched."
        )
        _frame(emit, "finish", 56, note, stack)
    return balanced
