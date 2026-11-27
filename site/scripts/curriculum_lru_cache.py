"""Verify LRU recency by ranking the timestamps of successful accesses."""

from .curriculum_evidence import EvidenceError, array, equal_json, fields, integer, obj
from .curriculum_trace import Frame, JsonValue, TraceRun


def verify_linked_recency(case: JsonValue, run: TraceRun) -> None:
    data = fields(case, "LRU Cache input", "capacity", "operations")
    capacity = integer(data["capacity"], 1, 3000, "capacity")
    operations = array(data["operations"], "operations")
    integer(len(operations), 1, 200_000, "operation count")
    # Timestamps select the oldest live key without relying on pointer order.
    entries: dict[int, tuple[int, int]] = {}
    results: list[JsonValue] = []
    frames: list[Frame] = []
    for index, item in enumerate(operations):
        name = obj(item, "operation").get("op")
        if name == "get":
            operation = fields(item, "get operation", "op", "key")
            key = integer(operation["key"], 0, 10_000, "key")
            previous = entries.get(key)
            if previous is None:
                results.append(-1)
                note = f"Miss {key}. Recency stays the same."
            else:
                value = previous[1]
                entries[key] = (index, value)
                results.append(value)
                note = f"Read {key}={value} and move it to the newest end."
            touched = previous is not None
            line = 93
        elif name == "put":
            operation = fields(item, "put operation", "op", "key", "value")
            key = integer(operation["key"], 0, 10_000, "key")
            value = integer(operation["value"], 0, 100_000, "value")
            entries[key] = (index, value)
            results.append(None)
            note = f"Store {key}={value} at the newest end."
            if len(entries) > capacity:
                oldest = min(entries, key=entries.__getitem__)
                del entries[oldest]
                note += f" Evict {oldest}, the oldest key."
            touched = True
            line = 105
        else:
            raise EvidenceError("LRU Cache operation name must be get or put")
        if len(operations) <= 32:
            order = sorted(entries, key=entries.__getitem__)
            frames.append(
                {
                    "stepId": f"{name}-{index}",
                    "codeLines": [line],
                    "explanation": note,
                    "state": {
                        "kind": "array",
                        "items": [f"{key}={entries[key][1]}" for key in order],
                    },
                    "highlights": [{"index": len(order) - 1}] if touched else [],
                }
            )
    if not equal_json(results, run.result):
        raise EvidenceError("LRU Cache result differs from timestamp history")
    if not equal_json(case, run.post_state):
        raise EvidenceError("LRU Cache execution mutated its input")
    if len(frames) != len(run.frames):
        raise EvidenceError("LRU Cache frame count differs from timestamp history")
    for index, (actual, expected) in enumerate(zip(run.frames, frames, strict=True), 1):
        if not equal_json(actual, expected):
            raise EvidenceError(
                f"LRU Cache frame {index} differs from timestamp history"
            )
