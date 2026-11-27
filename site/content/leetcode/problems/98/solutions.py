"""Validate a tree stored as rows of value, left index and right index."""

from collections.abc import Callable
from typing import TypedDict

type Json = bool | int | str | None | list[Json] | dict[str, Json]
type Emit = Callable[[dict[str, Json]], None]
type Node = tuple[int, int | None, int | None]


class Case(TypedDict):
    tree: list[Node]


def _tree_state(tree: list[Node]) -> dict[str, Json]:
    return {
        "kind": "tree",
        "nodes": [
            {"id": f"node-{index}", "value": value}
            for index, (value, _, _) in enumerate(tree)
        ],
        "edges": [
            {"from": f"node-{parent}", "to": f"node-{child}"}
            for parent, (_, left, right) in enumerate(tree)
            for child in (left, right)
            if child is not None
        ],
    }


def _frame(
    emit: Emit, state: dict[str, Json], index: int, line: int, note: str
) -> None:
    emit(
        {
            "stepId": f"check-{index}",
            "codeLines": [line],
            "explanation": note,
            "state": state,
            "highlights": [{"nodeId": f"node-{index}"}],
        }
    )


def recursive_bounds(case: Case, emit: Emit | None = None) -> bool:
    tree = case["tree"]
    # A frame includes the full tree, so only trace small teaching examples.
    state = _tree_state(tree) if emit is not None and len(tree) <= 32 else None

    def visit(index: int | None, lower: int | None, upper: int | None) -> bool:
        if index is None:
            return True
        value, left, right = tree[index]
        # The interval keeps the restrictions from every ancestor.
        within = (lower is None or lower < value) and (upper is None or value < upper)
        if emit is not None and state is not None:
            low = "-∞" if lower is None else str(lower)
            high = "+∞" if upper is None else str(upper)
            verdict = "inside" if within else "outside"
            _frame(
                emit,
                state,
                index,
                55,
                f"{value} is {verdict} the open interval ({low}, {high}).",
            )
        return within and visit(left, lower, value) and visit(right, value, upper)

    return visit(0, None, None)


def iterative_inorder(case: Case, emit: Emit | None = None) -> bool:
    tree = case["tree"]
    state = _tree_state(tree) if emit is not None and len(tree) <= 32 else None
    pending: list[int] = []
    index: int | None = 0
    previous: int | None = None
    while index is not None or pending:
        while index is not None:
            pending.append(index)
            index = tree[index][1]

        # The left subtree is complete. Visit its parent before the right subtree.
        current = pending.pop()
        value, _, right = tree[current]
        increasing = previous is None or previous < value
        if emit is not None and state is not None:
            if previous is None:
                note = f"Visit {value} first. There is no preceding value."
            else:
                verdict = "greater" if increasing else "not greater"
                note = f"{value} is {verdict} than the preceding value {previous}."
            _frame(emit, state, current, 86, note)
        if not increasing:
            return False
        previous = value
        index = right
    return True
