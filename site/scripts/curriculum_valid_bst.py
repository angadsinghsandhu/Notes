"""Check BST output using subtree extrema and frame order using tree structure."""

from itertools import pairwise

from .curriculum_evidence import EvidenceError, array, equal_json, fields, integer
from .curriculum_trace import JsonValue, TraceRun

type Node = tuple[int, int | None, int | None]
type Check = tuple[int, int, str]


def _tree(case: JsonValue) -> tuple[list[Node], list[int]]:
    data = fields(case, "Validate Binary Search Tree input", "tree")
    rows = array(data["tree"], "tree")
    count = integer(len(rows), 1, 10_000, "node count")
    tree: list[Node] = []
    for row in rows:
        items = array(row, "node row")
        if len(items) != 3:
            raise EvidenceError("node row must contain a value and two child indices")
        value, left, right = items
        tree.append(
            (
                integer(value, -(2**31), 2**31 - 1, "node value"),
                None if left is None else integer(left, 0, count - 1, "child index"),
                None if right is None else integer(right, 0, count - 1, "child index"),
            )
        )

    order: list[int] = []
    seen: set[int] = set()
    pending = [0]
    while pending:
        index = pending.pop()
        if index in seen:
            raise EvidenceError("Validate Binary Search Tree has a repeated node")
        seen.add(index)
        order.append(index)
        _, left, right = tree[index]
        pending.extend(child for child in (right, left) if child is not None)
    if len(seen) != count:
        raise EvidenceError("Validate Binary Search Tree has an unreachable node")
    return tree, order


def _ordered_subtrees(tree: list[Node], preorder: list[int]) -> bool:
    extrema = [(0, 0)] * len(tree)
    for index in reversed(preorder):
        value, left, right = tree[index]
        low, high = value, value
        if left is not None:
            low, left_max = extrema[left]
            if left_max >= value:
                return False
        if right is not None:
            right_min, high = extrema[right]
            if right_min <= value:
                return False
        extrema[index] = (low, high)
    return True


def _check_outcome(
    case: JsonValue, run: TraceRun, tree: list[Node], preorder: list[int]
) -> None:
    if not equal_json(run.result, _ordered_subtrees(tree, preorder)):
        raise EvidenceError(
            "Validate Binary Search Tree result differs from subtree extrema"
        )
    if not equal_json(run.post_state, case):
        raise EvidenceError("Validate Binary Search Tree execution mutated its input")


def _check_frames(tree: list[Node], run: TraceRun, checks: list[Check]) -> None:
    if len(run.frames) != len(checks):
        raise EvidenceError(
            "Validate Binary Search Tree frame count differs from visits"
        )
    if not checks:
        return
    state: JsonValue = {
        "kind": "tree",
        "nodes": [
            {"id": f"node-{index}", "value": row[0]} for index, row in enumerate(tree)
        ],
        "edges": [
            {"from": f"node-{index}", "to": f"node-{child}"}
            for index, row in enumerate(tree)
            for child in row[1:]
            if child is not None
        ],
    }
    for number, (frame, (index, line, note)) in enumerate(
        zip(run.frames, checks, strict=True), 1
    ):
        expected: JsonValue = {
            "stepId": f"check-{index}",
            "codeLines": [line],
            "explanation": note,
            "state": state,
            "highlights": [{"nodeId": f"node-{index}"}],
        }
        if not equal_json(frame, expected):
            raise EvidenceError(
                f"Validate Binary Search Tree frame {number} differs from the structural check"
            )


def verify_recursive_bounds(case: JsonValue, run: TraceRun) -> None:
    tree, preorder = _tree(case)
    _check_outcome(case, run, tree, preorder)
    checks: list[Check] = []
    if len(tree) <= 32:
        parents: dict[int, tuple[int, bool]] = {}
        for index, (_, left, right) in enumerate(tree):
            if left is not None:
                parents[left] = (index, True)
            if right is not None:
                parents[right] = (index, False)

        for index in preorder:
            lows: list[int] = []
            highs: list[int] = []
            ancestor = index
            while ancestor in parents:
                ancestor, from_left = parents[ancestor]
                (highs if from_left else lows).append(tree[ancestor][0])
            lower = max(lows) if lows else float("-inf")
            upper = min(highs) if highs else float("inf")
            value = tree[index][0]
            inside = lower < value < upper
            low = str(lower) if lows else "-∞"
            high = str(upper) if highs else "+∞"
            verdict = "inside" if inside else "outside"
            checks.append(
                (index, 55, f"{value} is {verdict} the open interval ({low}, {high}).")
            )
            if not inside:
                break
    _check_frames(tree, run, checks)


def verify_iterative_inorder(case: JsonValue, run: TraceRun) -> None:
    tree, preorder = _tree(case)
    _check_outcome(case, run, tree, preorder)
    checks: list[Check] = []
    if len(tree) <= 32:

        def ranks(index: int | None) -> list[int]:
            if index is None:
                return []
            _, left, right = tree[index]
            return [*ranks(left), index, *ranks(right)]

        order = ranks(0)
        checks.append(
            (
                order[0],
                86,
                f"Visit {tree[order[0]][0]} first. There is no preceding value.",
            )
        )
        for previous, index in pairwise(order):
            before, value = tree[previous][0], tree[index][0]
            verdict = "greater" if value > before else "not greater"
            checks.append(
                (index, 86, f"{value} is {verdict} than the preceding value {before}.")
            )
            if value <= before:
                break
    _check_frames(tree, run, checks)
