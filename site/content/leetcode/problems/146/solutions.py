"""Keep key lookup and recency order in separate structures."""

from collections.abc import Callable
from typing import Literal, TypedDict

type Json = int | str | None | list[Json] | dict[str, Json]
type Emit = Callable[[dict[str, Json]], None]


class Get(TypedDict):
    op: Literal["get"]
    key: int


class Put(TypedDict):
    op: Literal["put"]
    key: int
    value: int


class Case(TypedDict):
    capacity: int
    operations: list[Get | Put]


class Node:
    def __init__(self, key: int, value: int) -> None:
        self.key = key
        self.value = value
        self.prev = self
        self.next = self

    def unlink(self) -> None:
        self.prev.next = self.next
        self.next.prev = self.prev


class LRUCache:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.nodes: dict[int, Node] = {}
        # The sentinel's next node is oldest, and its previous node is newest.
        self.root = Node(-1, -1)

    def _make_newest(self, node: Node) -> None:
        node.prev = self.root.prev
        node.next = self.root
        self.root.prev.next = node
        self.root.prev = node

    def get(self, key: int) -> int:
        node = self.nodes.get(key)
        if node is None:
            return -1
        node.unlink()
        self._make_newest(node)
        return node.value

    def put(self, key: int, value: int) -> int | None:
        node = self.nodes.get(key)
        if node is None:
            node = Node(key, value)
            self.nodes[key] = node
        else:
            node.value = value
            node.unlink()
        self._make_newest(node)
        if len(self.nodes) <= self.capacity:
            return None
        oldest = self.root.next
        oldest.unlink()
        del self.nodes[oldest.key]
        return oldest.key

    def snapshot(self) -> list[Json]:
        items: list[Json] = []
        node = self.root.next
        while node is not self.root:
            items.append(f"{node.key}={node.value}")
            node = node.next
        return items


def linked_recency(case: Case, emit: Emit | None = None) -> list[int | None]:
    cache = LRUCache(case["capacity"])
    operations = case["operations"]
    # shortcut: only small examples emit snapshots, use sampled playback for long streams
    capture = emit if len(operations) <= 32 else None
    results: list[int | None] = []
    for index, operation in enumerate(operations):
        key = operation["key"]
        if operation["op"] == "get":
            result = cache.get(key)
            results.append(result)
            if capture is None:
                continue
            line = 93
            note = (
                f"Miss {key}. Recency stays the same."
                if result == -1
                else f"Read {key}={result} and move it to the newest end."
            )
            touched = result != -1
        else:
            evicted = cache.put(key, operation["value"])
            results.append(None)
            if capture is None:
                continue
            line = 105
            note = f"Store {key}={operation['value']} at the newest end."
            if evicted is not None:
                note += f" Evict {evicted}, the oldest key."
            touched = True
        items = cache.snapshot()
        capture(
            {
                "stepId": f"{operation['op']}-{index}",
                "codeLines": [line],
                "explanation": note,
                "state": {"kind": "array", "items": items},
                "highlights": [{"index": len(items) - 1}] if touched else [],
            }
        )
    return results
