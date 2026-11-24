"""Check path costs by propagating distances across grid diagonals."""

from .curriculum_evidence import EvidenceError, array, equal_json, fields, integer
from .curriculum_trace import Frame, JsonValue, TraceRun


def _grid(case: JsonValue) -> list[list[int]]:
    data = fields(case, "Minimum Path Sum input", "grid")
    rows = array(data["grid"], "grid")
    integer(len(rows), 1, 200, "grid height")
    grid = [
        [integer(cell, 0, 200, "cell weight") for cell in array(row, "grid row")]
        for row in rows
    ]
    width = integer(len(grid[0]), 1, 200, "grid width")
    if any(len(row) != width for row in grid):
        raise EvidenceError("Minimum Path Sum requires a rectangular grid")
    return grid


def _distances(grid: list[list[int]]) -> list[list[int]]:
    height, width = len(grid), len(grid[0])
    # Any legal path costs at most this much, so the next integer is unreachable.
    infinity = 200 * (height + width - 1) + 1
    distances = [[infinity] * width for _ in grid]
    distances[0][0] = grid[0][0]
    for diagonal in range(height + width - 1):
        for row in range(max(0, diagonal - width + 1), min(height, diagonal + 1)):
            column = diagonal - row
            for y, x in ((row + 1, column), (row, column + 1)):
                if y < height and x < width:
                    proposed = distances[row][column] + grid[y][x]
                    distances[y][x] = min(distances[y][x], proposed)
    return distances


def _check_run(case: JsonValue, run: TraceRun, result: int, count: int) -> None:
    if not equal_json(run.result, result):
        raise EvidenceError("Minimum Path Sum result differs from diagonal distances")
    if not equal_json(run.post_state, case):
        raise EvidenceError("Minimum Path Sum execution mutated its input")
    if len(run.frames) != count:
        raise EvidenceError("Minimum Path Sum frame count differs from cell count")


def _check_frame(
    frame: Frame, number: int, step: str, state: JsonValue, highlight: JsonValue
) -> None:
    if (
        frame["stepId"] != step
        or not equal_json(frame["state"], state)
        or not equal_json(frame["highlights"], [highlight])
    ):
        raise EvidenceError(
            f"Minimum Path Sum frame {number} differs from diagonal distances"
        )


def verify_memoized_grid(case: JsonValue, run: TraceRun) -> None:
    grid = _grid(case)
    height, width = len(grid), len(grid[0])
    # Reverse both axes to turn distances from the destination into forward distances.
    reversed_distances = _distances([row[::-1] for row in grid[::-1]])
    _check_run(case, run, reversed_distances[-1][-1], height * width)
    saved: list[JsonValue] = []
    rows: list[list[JsonValue]] = [[None] * width for _ in grid]
    saved.extend(rows)
    for index, frame in enumerate(run.frames):
        reverse_row, reverse_column = divmod(index, width)
        row, column = height - 1 - reverse_row, width - 1 - reverse_column
        rows[row][column] = reversed_distances[reverse_row][reverse_column]
        _check_frame(
            frame,
            index + 1,
            f"save-{row}-{column}",
            {"kind": "grid", "rows": saved},
            {"row": row, "column": column},
        )


def verify_row_storage(case: JsonValue, run: TraceRun) -> None:
    grid = _grid(case)
    width = len(grid[0])
    distances = _distances(grid)
    _check_run(case, run, distances[-1][-1], len(grid) * width)
    for index, frame in enumerate(run.frames):
        row, column = divmod(index, width)
        previous: list[int | None] = list(distances[row - 1]) if row else [None] * width
        items: list[JsonValue] = [
            *distances[row][: column + 1],
            *previous[column + 1 :],
        ]
        _check_frame(
            frame,
            index + 1,
            f"write-{row}-{column}",
            {"kind": "array", "items": items},
            {"index": column},
        )
