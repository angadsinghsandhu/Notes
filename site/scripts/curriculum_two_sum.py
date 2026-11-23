"""Independent result, post-state and trace checks for problem #1."""

from collections.abc import Iterator
from itertools import combinations

from .curriculum_evidence import EvidenceError, array, equal_json, fields, integer
from .curriculum_trace import Frame, JsonValue, TraceRun


def _facts(case: JsonValue, run: TraceRun) -> tuple[list[int], int, tuple[int, int]]:
    data = fields(case, "Two Sum input", "nums", "target")
    nums = [
        integer(value, -(10**9), 10**9, "Two Sum value")
        for value in array(data["nums"], "Two Sum nums")
    ]
    integer(len(nums), 2, 10_000, "Two Sum input length")
    target = integer(data["target"], -(10**9), 10**9, "Two Sum target")
    answers = (
        (i, j)
        for i, j in combinations(range(len(nums)), 2)
        if nums[j] == target - nums[i]
    )
    answer = next(answers, None)
    if answer is None or next(answers, None) is not None:
        raise EvidenceError("Two Sum input must have a unique pair")
    if not equal_json(run.result, list(answer)):
        raise EvidenceError("Two Sum result differs from the canonical unique pair")
    if not equal_json(run.post_state, case):
        raise EvidenceError("Two Sum execution mutated its input")
    return nums, target, answer


def _frame(
    step: str, line: int, explanation: str, state: Frame, highlights: list[JsonValue]
) -> Frame:
    return {
        "stepId": step,
        "codeLines": [line],
        "explanation": explanation,
        "state": state,
        "highlights": highlights,
    }


def _table(
    step: str,
    line: int,
    explanation: str,
    headings: tuple[str, str],
    entries: list[tuple[int, int]],
    *rows: int,
) -> Frame:
    return _frame(
        step,
        line,
        explanation,
        {
            "kind": "table",
            "columns": list(headings),
            "rows": [list(row) for row in entries],
        },
        [{"row": row, "column": 0} for row in rows],
    )


def _check_frames(actual: list[Frame], expected: Iterator[Frame]) -> None:
    index = 0
    for index, frame in enumerate(expected, 1):
        if index > len(actual):
            raise EvidenceError("Two Sum frame count is missing execution steps")
        if not equal_json(actual[index - 1], frame):
            raise EvidenceError(f"Two Sum frame {index} differs from its invariant")
    if len(actual) != index:
        raise EvidenceError("Two Sum frame count includes extra execution steps")


def verify_pairs(case: JsonValue, run: TraceRun) -> None:
    nums, target, answer = _facts(case, run)

    def expected() -> Iterator[Frame]:
        positions = range(len(nums))
        for i, j in combinations(positions, 2):
            total = nums[i] + nums[j]
            yield _frame(
                f"compare-{i}-{j}",
                58,
                f"Positions {i} and {j} sum to {total}. Target is {target}.",
                {"kind": "array", "items": list(nums)},
                [{"index": i}, {"index": j}],
            )
            if (i, j) == answer:
                break

    _check_frames(run.frames, expected())


def verify_sorted(case: JsonValue, run: TraceRun) -> None:
    nums, target, answer = _facts(case, run)
    positions = sorted(range(len(nums)), key=nums.__getitem__)
    entries = [(nums[position], position) for position in positions]
    headings = ("Value", "Original index")

    def expected() -> Iterator[Frame]:
        remaining = list(range(len(entries)))
        yield _table(
            "sort",
            76,
            "Sort by value and keep each original index.",
            headings,
            entries,
            remaining[0],
            remaining[-1],
        )
        step = 0
        while True:
            first, last = remaining[0], remaining[-1]
            low, high = entries[first][0], entries[last][0]
            total = low + high
            yield _table(
                f"compare-{step}",
                94,
                f"Endpoint values {low} and {high} sum to {total}. Target is {target}.",
                headings,
                entries,
                first,
                last,
            )
            if {positions[first], positions[last]} == set(answer):
                break
            if total < target:
                discarded = remaining.pop(0)
                line, reason = 110, "Sum is too small. Drop the left endpoint."
            else:
                discarded = remaining.pop()
                line, reason = 115, "Sum is too large. Drop the right endpoint."
            if positions[discarded] in answer:
                raise EvidenceError("Two Sum pointer discarded a valid answer position")
            yield _table(
                f"move-{step}",
                line,
                reason,
                headings,
                entries,
                remaining[0],
                remaining[-1],
            )
            step += 1

    _check_frames(run.frames, expected())


def _prefix_entries(nums: list[int], length: int) -> list[tuple[int, int]]:
    prefix = nums[:length]
    reverse = prefix[::-1]
    return [
        (value, length - 1 - reverse.index(value)) for value in dict.fromkeys(prefix)
    ]


def verify_hash(case: JsonValue, run: TraceRun) -> None:
    nums, target, (earlier, later) = _facts(case, run)
    headings = ("Seen value", "Latest original index")

    def expected() -> Iterator[Frame]:
        for index in range(later + 1):
            value = nums[index]
            needed = target - value
            before = _prefix_entries(nums, index)
            outcome = (
                "No earlier match." if index < later else f"Found index {earlier}."
            )
            yield _table(
                f"lookup-{index}",
                140,
                f"Index {index} has {value} and needs {needed}. {outcome}",
                headings,
                before,
                *(row for row, (key, _) in enumerate(before) if key == needed),
            )
            if index < later:
                after = _prefix_entries(nums, index + 1)
                yield _table(
                    f"record-{index}",
                    160,
                    f"Record {value} at index {index} for later lookups.",
                    headings,
                    after,
                    after.index((value, index)),
                )

    _check_frames(run.frames, expected())
