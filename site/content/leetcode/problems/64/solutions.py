"""Find a minimum right-and-down path cost without changing the input grid."""

from collections.abc import Callable
from functools import cache
from typing import TypedDict

type Json = int | str | None | list[Json] | dict[str, Json]
type Emit = Callable[[dict[str, Json]], None]


class Case(TypedDict):
    grid: list[list[int]]


def _frame(
    emit: Emit,
    step: str,
    line: int,
    note: str,
    state: dict[str, Json],
    highlights: list[Json],
) -> None:
    emit(
        {
            "stepId": step,
            "codeLines": [line],
            "explanation": note,
            "state": state,
            "highlights": highlights,
        }
    )


def memoized_grid(case: Case, emit: Emit | None = None) -> int:
    grid = case["grid"]
    height, width = len(grid), len(grid[0])
    saved: list[list[int | None]] = (
        [[None] * width for _ in grid] if emit is not None else []
    )

    @cache
    def visit(row: int, column: int) -> int:
        # Each child is a possible next step toward the destination.
        if row == height - 1 and column == width - 1:
            remaining = 0
        elif row == height - 1:
            remaining = visit(row, column + 1)
        elif column == width - 1:
            remaining = visit(row + 1, column)
        else:
            remaining = min(visit(row + 1, column), visit(row, column + 1))

        weight = grid[row][column]
        total = weight + remaining
        if emit is not None:
            saved[row][column] = total
            _frame(
                emit,
                f"save-{row}-{column}",
                56,
                f"From ({row}, {column}), add weight {weight} to the best remaining cost {remaining}. Save {total}.",
                {"kind": "grid", "rows": [list(line) for line in saved]},
                [{"row": row, "column": column}],
            )
        return total

    return visit(0, 0)


def row_storage(case: Case, emit: Emit | None = None) -> int:
    grid = case["grid"]
    costs = [0] * len(grid[0])
    for row, weights in enumerate(grid):
        for column, weight in enumerate(weights):
            # Before the overwrite, costs[column] is above and costs[column - 1] is left.
            if row == 0:
                previous = costs[column - 1] if column else 0
            elif column == 0:
                previous = costs[column]
            else:
                previous = min(costs[column], costs[column - 1])
            total = weight + previous
            costs[column] = total
            if emit is not None:
                visible: list[Json] = list(costs)
                if row == 0:
                    visible[column + 1 :] = [None] * (len(costs) - column - 1)
                _frame(
                    emit,
                    f"write-{row}-{column}",
                    83,
                    f"Reach ({row}, {column}) for {previous} plus weight {weight}. Store {total}.",
                    {"kind": "array", "items": visible},
                    [{"index": column}],
                )
    return costs[-1]
