"""Verify Word Ladder with a graph built from shared deletion patterns."""

from collections import defaultdict
from typing import Literal

from .curriculum_evidence import EvidenceError, array, equal_json, fields, integer, text
from .curriculum_trace import Frame, JsonValue, TraceRun

type Graph = dict[str, tuple[str, ...]]


def _inputs(case: JsonValue) -> tuple[str, str, set[str]]:
    data = fields(case, "Word Ladder input", "beginWord", "endWord", "wordList")
    begin = text(data["beginWord"], "beginWord")
    width = integer(len(begin), 1, 10, "word length")
    end = text(data["endWord"], "endWord")
    items = array(data["wordList"], "wordList")
    integer(len(items), 1, 5000, "dictionary size")
    words = [text(item, "dictionary word") for item in items]
    for word in [begin, end, *words]:
        if len(word) != width:
            raise EvidenceError("Word Ladder requires words of equal length")
        if any(not "a" <= letter <= "z" for letter in word):
            raise EvidenceError("Word Ladder requires lowercase English letters")
    if begin == end:
        raise EvidenceError("Word Ladder requires distinct endpoints")
    dictionary = set(words)
    if len(dictionary) != len(words):
        raise EvidenceError("Word Ladder dictionary must contain distinct words")
    return begin, end, dictionary


def _graph(vertices: set[str]) -> Graph:
    # A shared key fixes the changed position and every other character.
    signatures = {
        word: [(i, word[:i] + word[i + 1 :]) for i in range(len(word))]
        for word in sorted(vertices)
    }
    buckets: dict[tuple[int, str], list[str]] = defaultdict(list)
    for word, keys in signatures.items():
        for key in keys:
            buckets[key].append(word)
    return {
        word: tuple(
            neighbor for key in keys for neighbor in buckets[key] if neighbor != word
        )
        for word, keys in signatures.items()
    }


def _layers(graph: Graph, origin: str) -> list[set[str]]:
    visited = {origin}
    layers = [visited.copy()]
    while layers[-1]:
        next_layer = {
            neighbor for word in layers[-1] for neighbor in graph[word]
        } - visited
        visited.update(next_layer)
        layers.append(next_layer)
    return layers


def _frame(
    step: str,
    line: int,
    note: str,
    kind: str,
    items: list[str],
    active_count: int = 0,
) -> Frame:
    return {
        "stepId": step,
        "codeLines": [line],
        "explanation": note,
        "state": {"kind": kind, "items": [*items]},
        "highlights": [{"index": index} for index in range(active_count)],
    }


def _queue_frames(
    graph: Graph, begin: str, end: str, start_layers: list[set[str]]
) -> list[Frame]:
    frames: list[Frame] = []
    current_layer = [begin]
    discovered = {begin}
    for length in range(1, len(start_layers)):
        next_layer: list[str] = []
        for offset, word in enumerate(current_layer):
            note = (
                f"Reach {word}. The ladder contains {length} words."
                if word == end
                else f"Visit {word} at ladder length {length}."
            )
            frames.append(
                _frame(
                    f"visit-{len(frames)}",
                    60,
                    note,
                    "queue",
                    current_layer[offset:] + next_layer,
                    1,
                )
            )
            if word == end:
                return frames
            for neighbor in graph[word]:
                if neighbor not in discovered:
                    next_layer.append(neighbor)
                    discovered.add(neighbor)
        current_layer = next_layer
    frames.append(
        _frame(
            "exhausted", 94, f"The queue emptied before reaching {end}.", "queue", []
        )
    )
    return frames


def _frontier_frames(
    graph: Graph, end: str, start_layers: list[set[str]]
) -> list[Frame]:
    layers = (start_layers, _layers(graph, end))
    depths = [0, 0]
    side = 0
    frames: list[Frame] = []
    while True:
        active = layers[side][depths[side]]
        opposite = layers[1 - side][depths[1 - side]]
        if not active or not opposite:
            frames.append(
                _frame(
                    "exhausted",
                    165,
                    "One frontier emptied before the searches met.",
                    "array",
                    [],
                )
            )
            return frames
        if len(active) > len(opposite):
            side = 1 - side
            active, opposite = opposite, active
        ordered = sorted(active)
        label = ("Start", "Target")[side]
        depth = depths[side]
        frames.append(
            _frame(
                f"expand-{len(frames)}",
                133,
                f"{label} frontier at distance {depth}. Expand the highlighted words.",
                "array",
                [*ordered, "|", *sorted(opposite)],
                len(ordered),
            )
        )
        other_distances = {
            word: distance
            for distance, layer in enumerate(layers[1 - side][: depths[1 - side] + 1])
            for word in layer
        }
        for word in ordered:
            for neighbor in graph[word]:
                if neighbor in other_distances:
                    length = depth + other_distances[neighbor] + 2
                    frames.append(
                        _frame(
                            "meet",
                            137,
                            f"Join {word} to {neighbor}. The ladder contains {length} words.",
                            "array",
                            [word, neighbor],
                            2,
                        )
                    )
                    return frames
        depths[side] += 1


def _verify(case: JsonValue, run: TraceRun, kind: Literal["queue", "array"]) -> None:
    begin, end, dictionary = _inputs(case)
    frames: list[Frame] = []
    expected = 0
    if end in dictionary:
        graph = _graph(dictionary | {begin})
        layers = _layers(graph, begin)
        expected = next(
            (length for length, layer in enumerate(layers, 1) if end in layer), 0
        )
        if len(dictionary) <= 32:
            frames = (
                _queue_frames(graph, begin, end, layers)
                if kind == "queue"
                else _frontier_frames(graph, end, layers)
            )
    elif len(dictionary) <= 32:
        line = 51 if kind == "queue" else 102
        frames = [_frame("absent", line, f"{end} is outside the dictionary.", kind, [])]
    if not equal_json(run.result, expected):
        raise EvidenceError("Word Ladder result differs from graph distances")
    if not equal_json(run.post_state, case):
        raise EvidenceError("Word Ladder execution mutated its input")
    if len(run.frames) != len(frames):
        raise EvidenceError("Word Ladder frame count differs from graph traversal")
    for index, (actual, check) in enumerate(zip(run.frames, frames, strict=True), 1):
        if not equal_json(actual, check):
            raise EvidenceError(
                f"Word Ladder frame {index} differs from graph traversal"
            )


def verify_queue_bfs(case: JsonValue, run: TraceRun) -> None:
    _verify(case, run, "queue")


def verify_two_frontier_bfs(case: JsonValue, run: TraceRun) -> None:
    _verify(case, run, "array")
