import hashlib
import json
import unittest
from contextlib import redirect_stderr
from io import StringIO
from itertools import combinations
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.curriculum import Enrollment, check, inventory, main
from scripts.curriculum_evidence import EvidenceError
from scripts.curriculum_trace import JsonValue, PythonAdapter, TraceRun

SOURCE = b"""def solve(grid, emit):
    for row, cells in enumerate(grid):
        for column, weight in enumerate(cells):
            predecessors = []
            if row:
                predecessors.append(grid[row - 1][column])
            if column:
                predecessors.append(grid[row][column - 1])
            cells[column] = weight + min(predecessors, default=0)
            emit({"stepId": f"cell-{row}-{column}", "codeLines": [9],
                  "explanation": "Accumulate the minimum cost to reach this cell.",
                  "state": {"kind": "grid", "rows": grid},
                  "highlights": [{"row": row, "column": column}]})
    return grid[-1][-1]
"""
GRID = ((2, 5, 1), (3, 0, 8), (4, 1, 2))


def put(root: Path, path: str, data: object) -> dict[str, str]:
    child = root / path
    child.parent.mkdir(parents=True, exist_ok=True)
    raw = data if isinstance(data, bytes) else json.dumps(data).encode()
    child.write_bytes(raw)
    return {"path": path, "sha256": hashlib.sha256(raw).hexdigest()}


def minimum_prefix(row: int, column: int) -> int:
    costs: list[int] = []
    for downs in combinations(range(row + column), row):
        y = x = 0
        cost = GRID[y][x]
        for index in range(row + column):
            if index in downs:
                y += 1
            else:
                x += 1
            cost += GRID[y][x]
        costs.append(cost)
    return min(costs)


def expected_snapshots() -> list[list[list[int]]]:
    current = [list(row) for row in GRID]
    snapshots: list[list[list[int]]] = []
    for row, cells in enumerate(current):
        for column in range(len(cells)):
            cells[column] = minimum_prefix(row, column)
            snapshots.append([line.copy() for line in current])
    return snapshots


def independent_check(case: JsonValue, run: TraceRun) -> None:
    if case != [list(row) for row in GRID]:
        raise EvidenceError("unexpected DP oracle fixture")
    expected = expected_snapshots()
    if (
        run.result != minimum_prefix(2, 2)
        or run.post_state != expected[-1]
        or [frame["state"] for frame in run.frames]
        != [{"kind": "grid", "rows": rows} for rows in expected]
    ):
        raise EvidenceError("minimum path oracle or cell snapshot invariant failed")


class CurriculumTests(unittest.TestCase):
    def setUp(self) -> None:
        temp = TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.site = Path(temp.name) / "site"
        self.site.mkdir()
        self.root = self.site / "content/leetcode"
        self.problem = self.root / "problems/64"

    def manifest(self) -> JsonValue:
        return {
            "version": 1,
            "problems": [
                {
                    "number": i,
                    "id": f"leetcode:{i}",
                    "status": "draft" if i == 64 else "planned",
                }
                for i in range(1, 2001)
            ],
            "lessons": ["leetcode:64"],
            "paths": [],
        }

    def lesson(
        self,
        *,
        publish: bool = True,
        wrong_middle: bool = False,
        wrong_post: bool = False,
        source: bytes = SOURCE,
    ) -> dict[tuple[int, str], Enrollment]:
        put(self.root, "manifest.json", self.manifest())
        implementation = put(self.problem, "solution.py", source)
        digest = implementation["sha256"]
        snapshots = expected_snapshots()
        example = {
            "id": "small",
            "input": GRID,
            "result": 8,
            "postState": GRID if wrong_post else snapshots[-1],
        }
        examples = put(
            self.problem, "examples.json", {"version": 1, "examples": [example]}
        )
        if wrong_middle:
            snapshots[4][1][1] += 1
        frames = [
            {
                "stepId": f"cell-{row}-{column}",
                "codeLines": [9],
                "explanation": "Accumulate the minimum cost to reach this cell.",
                "state": {"kind": "grid", "rows": rows},
                "highlights": [{"row": row, "column": column}],
            }
            for index, rows in enumerate(snapshots)
            for row, column in [divmod(index, 3)]
        ]
        trace = put(
            self.problem,
            "traces/in-place/small.json",
            {
                "version": 1,
                "problemId": "leetcode:64",
                "approachId": "in-place",
                "exampleId": "small",
                "implementationSha256": digest,
                "result": 8,
                "frames": frames,
            },
        )
        put(
            self.problem,
            "metadata.json",
            {
                "problemId": "leetcode:64",
                "prose": put(self.problem, "lesson.md", b"# A test lesson")
                if publish
                else None,
                "examples": examples,
                "approaches": [
                    {
                        "id": "in-place",
                        "language": "python",
                        "implementation": {**implementation, "entryPoint": "solve"},
                        "verification": {
                            "implementationSha256": digest,
                            "entryPoint": "solve",
                            "examplesSha256": examples["sha256"],
                            "passedExampleIds": ["small"],
                            "checkedOn": "2026-11-22",
                        },
                        "traces": [
                            {
                                **trace,
                                "exampleId": "small",
                                "implementationSha256": digest,
                            }
                        ],
                    }
                ],
            },
        )
        return {
            (64, "in-place"): Enrollment(
                "solution.py",
                hashlib.sha256(SOURCE).hexdigest(),
                PythonAdapter("solve"),
                independent_check,
            )
        }

    def test_inventory_and_missing_explicit_id(self) -> None:
        self.assertIsNone(inventory(self.site))
        self.assertIsNone(check(self.site))
        with self.assertRaisesRegex(EvidenceError, "no curriculum"):
            check(self.site, (64,))
        self.root.mkdir(parents=True)
        with self.assertRaisesRegex(EvidenceError, "manifest.json"):
            check(self.site)
        put(self.root, "manifest.json", self.manifest())
        sets = inventory(self.site)
        assert sets is not None
        self.assertEqual(sets["draft"], [64])
        self.assertEqual(sets["planned"], [i for i in range(1, 2001) if i != 64])
        self.assertEqual(sets["verified"], [])
        with self.assertRaisesRegex(EvidenceError, "leetcode:65"):
            check(self.site, (65,))

    def test_valid_foreign_and_dangling_content_symlinks_fail(self) -> None:
        site = self.site
        foreign = site.parent / "foreign"
        put(foreign, "leetcode/manifest.json", self.manifest())
        for target in (foreign, site.parent / "missing"):
            with self.subTest(target=target):
                link = site / "content"
                link.symlink_to(target, target_is_directory=True)
                try:
                    with self.assertRaisesRegex(EvidenceError, "content"):
                        inventory(site)
                    with self.assertRaisesRegex(EvidenceError, "content"):
                        check(site)
                finally:
                    link.unlink()

    def test_inventory_rejects_incomplete_or_duplicate_identity_list(self) -> None:
        manifest = json.loads(json.dumps(self.manifest()))
        manifest["problems"].pop()
        put(self.root, "manifest.json", manifest)
        with self.assertRaisesRegex(EvidenceError, "first missing ID 2000"):
            inventory(self.site)
        manifest["problems"].append(manifest["problems"][0])
        put(self.root, "manifest.json", manifest)
        with self.assertRaisesRegex(EvidenceError, "duplicate manifest identity"):
            inventory(self.site)

    def test_prose_only_draft_can_publish_but_explicit_verification_fails(self) -> None:
        self.lesson()
        metadata_path = self.problem / "metadata.json"
        metadata = json.loads(metadata_path.read_bytes())
        metadata["approaches"] = []
        metadata["examples"] = None
        put(self.problem, "metadata.json", metadata)
        self.assertEqual(check(self.site), 0)
        with self.assertRaisesRegex(EvidenceError, "no approaches"):
            check(self.site, (64,))

    def test_verified_status_cannot_bypass_published_prose(self) -> None:
        registry = self.lesson(publish=False)
        manifest_path = self.root / "manifest.json"
        manifest = json.loads(manifest_path.read_bytes())
        manifest["problems"][63]["status"] = "verified"
        put(self.root, "manifest.json", manifest)
        with self.assertRaisesRegex(EvidenceError, "verified lesson requires prose"):
            check(self.site, registry=registry)

    def test_default_only_published_explicit_authoring(self) -> None:
        registry = self.lesson(publish=False)
        self.assertEqual(check(self.site), 0)
        self.assertEqual(check(self.site, (64,), registry), 1)
        self.lesson()
        self.assertEqual(check(self.site, registry=registry), 1)

    def test_reviewed_source_and_registry_are_independent_of_metadata(self) -> None:
        registry = self.lesson(source=SOURCE + b"\n")
        with self.assertRaisesRegex(EvidenceError, "enrollment"):
            check(self.site)
        with self.assertRaisesRegex(EvidenceError, "enrollment"):
            check(self.site, registry=registry)
        registry = self.lesson()
        (self.problem / "solution.py").write_bytes(b"pass")
        with self.assertRaisesRegex(EvidenceError, "SHA256"):
            check(self.site, registry=registry)

    def test_each_published_approach_requires_enrollment_and_trace_evidence(
        self,
    ) -> None:
        registry = self.lesson()
        metadata = json.loads((self.problem / "metadata.json").read_bytes())
        metadata["approaches"].append({**metadata["approaches"][0], "id": "second"})
        put(self.problem, "metadata.json", metadata)
        with self.assertRaisesRegex(
            EvidenceError, "second: no reviewed execution enrollment"
        ):
            check(self.site, registry=registry)
        metadata["approaches"].pop()
        metadata["approaches"][0]["traces"] = []
        put(self.problem, "metadata.json", metadata)
        with self.assertRaisesRegex(EvidenceError, "at least one trace"):
            check(self.site, registry=registry)

    def test_examples_bytes_and_trace_identity_are_checked(self) -> None:
        registry = self.lesson()
        with (self.problem / "examples.json").open("ab") as examples:
            examples.write(b"\n")
        with self.assertRaisesRegex(EvidenceError, "examples.json.*SHA256"):
            check(self.site, registry=registry)
        self.lesson()
        metadata = json.loads((self.problem / "metadata.json").read_bytes())
        trace_path = "traces/in-place/small.json"
        trace = json.loads((self.problem / trace_path).read_bytes())
        trace["exampleId"] = "renamed"
        evidence = put(self.problem, trace_path, trace)
        metadata["approaches"][0]["traces"][0].update(evidence)
        put(self.problem, "metadata.json", metadata)
        with self.assertRaisesRegex(EvidenceError, "trace identity"):
            check(self.site, registry=registry)

    def test_middle_frame_disagrees_with_execution_after_rehashing(self) -> None:
        registry = self.lesson(wrong_middle=True)
        with self.assertRaisesRegex(EvidenceError, "frame 5"):
            check(self.site, registry=registry)

    def test_post_state_and_independent_oracle(self) -> None:
        registry = self.lesson(wrong_post=True)
        with self.assertRaisesRegex(EvidenceError, "post-state"):
            check(self.site, registry=registry)
        registry = self.lesson()
        first = registry[64, "in-place"]

        def oracle(_case: JsonValue, _run: TraceRun) -> None:
            raise EvidenceError("sentinel oracle failure")

        with self.assertRaisesRegex(EvidenceError, "sentinel oracle failure"):
            check(
                self.site,
                registry={
                    (64, "in-place"): Enrollment(
                        first.path, first.sha256, first.adapter, oracle
                    )
                },
            )

    def test_bad_cli_selection(self) -> None:
        for selection in ("", "01", "1,1", "2001", "1,,64"):
            with (
                self.subTest(selection=selection),
                self.assertRaises(SystemExit) as exit,
                redirect_stderr(StringIO()),
            ):
                main(["check", "--ids", selection])
            self.assertEqual(exit.exception.code, 2)
