"""Find shortest ladders with one queue or two breadth-first frontiers."""

from collections import deque
from collections.abc import Callable, Iterator
from typing import TypedDict

type Json = int | str | list[Json] | dict[str, Json]
type Emit = Callable[[dict[str, Json]], None]


class Case(TypedDict):
    beginWord: str
    endWord: str
    wordList: list[str]


def _neighbors(word: str) -> Iterator[str]:
    for index, original in enumerate(word):
        prefix, suffix = word[:index], word[index + 1 :]
        for letter in "abcdefghijklmnopqrstuvwxyz":
            if letter != original:
                yield prefix + letter + suffix


def _frame(
    emit: Emit,
    step: str,
    line: int,
    note: str,
    kind: str,
    items: list[str],
    active_count: int = 0,
) -> None:
    emit(
        {
            "stepId": step,
            "codeLines": [line],
            "explanation": note,
            "state": {"kind": kind, "items": [*items]},
            "highlights": [{"index": index} for index in range(active_count)],
        }
    )


def queue_bfs(case: Case, emit: Emit | None = None) -> int:
    begin, end = case["beginWord"], case["endWord"]
    remaining = set(case["wordList"])
    # Whole-queue snapshots are for small teaching examples.
    if len(remaining) > 32:
        emit = None
    if end not in remaining:
        if emit is not None:
            _frame(emit, "absent", 51, f"{end} is outside the dictionary.", "queue", [])
        return 0

    remaining.discard(begin)
    queue = deque([(begin, 1)])
    visit = 0
    while queue:
        word, length = queue.popleft()
        if emit is not None:
            note = (
                f"Reach {word}. The ladder contains {length} words."
                if word == end
                else f"Visit {word} at ladder length {length}."
            )
            _frame(
                emit,
                f"visit-{visit}",
                60,
                note,
                "queue",
                [word, *(pending for pending, _ in queue)],
                1,
            )
        if word == end:
            return length
        for candidate in _neighbors(word):
            if candidate in remaining:
                # Mark discoveries now so a later parent cannot enqueue them again.
                remaining.remove(candidate)
                queue.append((candidate, length + 1))
        visit += 1

    if emit is not None:
        _frame(
            emit,
            "exhausted",
            94,
            f"The queue emptied before reaching {end}.",
            "queue",
            [],
        )
    return 0


def two_frontier_bfs(case: Case, emit: Emit | None = None) -> int:
    begin, end = case["beginWord"], case["endWord"]
    dictionary = set(case["wordList"])
    if len(dictionary) > 32:
        emit = None
    if end not in dictionary:
        if emit is not None:
            _frame(
                emit, "absent", 102, f"{end} is outside the dictionary.", "array", []
            )
        return 0

    frontier, other_frontier = {begin}, {end}
    distances, other_distances = {begin: 0}, {end: 0}
    from_start = True
    layer = 0
    while frontier and other_frontier:
        if len(frontier) > len(other_frontier):
            frontier, other_frontier = other_frontier, frontier
            distances, other_distances = other_distances, distances
            from_start = not from_start

        next_frontier: set[str] = set()
        active = sorted(frontier) if emit is not None else frontier
        if emit is not None:
            side = "Start" if from_start else "Target"
            distance = distances[next(iter(frontier))]
            _frame(
                emit,
                f"expand-{layer}",
                133,
                f"{side} frontier at distance {distance}. Expand the highlighted words.",
                "array",
                [*active, "|", *sorted(other_frontier)],
                len(active),
            )
        for word in active:
            distance = distances[word]
            for candidate in _neighbors(word):
                # A bridge can touch any word already reached from the other end.
                if candidate in other_distances:
                    length = distance + other_distances[candidate] + 2
                    if emit is not None:
                        _frame(
                            emit,
                            "meet",
                            137,
                            f"Join {word} to {candidate}. The ladder contains {length} words.",
                            "array",
                            [word, candidate],
                            2,
                        )
                    return length
                if candidate in dictionary and candidate not in distances:
                    distances[candidate] = distance + 1
                    next_frontier.add(candidate)
        frontier = next_frontier
        layer += 1

    if emit is not None:
        _frame(
            emit,
            "exhausted",
            165,
            "One frontier emptied before the searches met.",
            "array",
            [],
        )
    return 0
