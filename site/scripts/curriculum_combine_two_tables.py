"""Verify SQLite join output by grouping the address rows by person ID."""

from .curriculum_evidence import SAFE_INTEGER, EvidenceError, array, equal_json, integer
from .curriculum_trace import JsonValue, SqlAdapter, TraceRun

LEFT_JOIN_ADAPTER = SqlAdapter(
    setup=(
        (
            "CREATE TABLE Person (personId INT NOT NULL PRIMARY KEY, "
            "lastName TEXT, firstName TEXT)"
        ),
        (
            "CREATE TABLE Address (addressId INT NOT NULL PRIMARY KEY, "
            "personId INT, city TEXT, state TEXT)"
        ),
    ),
    inserts=(
        "INSERT INTO Person VALUES (?, ?, ?)",
        "INSERT INTO Address VALUES (?, ?, ?, ?)",
    ),
    code_lines=(2, 3, 4, 6),
    explanation=(
        "The query returns one row per matching address and a NULL-extended row "
        "for each person without a match. Source IDs determine the display order."
    ),
)


def _key(value: JsonValue, label: str) -> int:
    return integer(value, -SAFE_INTEGER, SAFE_INTEGER, label)


def _row(value: JsonValue, width: int, label: str) -> list[JsonValue]:
    row = array(value, label)
    if len(row) != width:
        raise EvidenceError(f"{label} must have {width} fields")
    if any(cell is not None and not isinstance(cell, str) for cell in row[-2:]):
        raise EvidenceError(f"{label} text columns must be strings or NULL")
    return row


def verify_left_join(case: JsonValue, run: TraceRun) -> None:
    groups = array(case, "SQL fixture")
    if len(groups) != 2:
        raise EvidenceError("SQL fixture must include Person and Address groups")
    people: dict[int, list[JsonValue]] = {}
    for value in array(groups[0], "Person rows"):
        person_id, last, first = _row(value, 3, "Person row")
        key = _key(person_id, "personId")
        if key in people:
            raise EvidenceError("duplicate Person primary key")
        people[key] = [first, last]
    address_ids: set[int] = set()
    addresses: dict[int, list[tuple[int, list[JsonValue]]]] = {}
    for value in array(groups[1], "Address rows"):
        address_id, person_id, city, state = _row(value, 4, "Address row")
        key = _key(address_id, "addressId")
        if key in address_ids:
            raise EvidenceError("duplicate Address primary key")
        address_ids.add(key)
        if person_id is not None:
            person = _key(person_id, "Address.personId")
            addresses.setdefault(person, []).append((key, [city, state]))
    rows: list[JsonValue] = []
    for person, name in sorted(people.items()):
        for _, address in sorted(addresses.get(person, [(0, [None, None])])):
            rows.append(name + address)
    result: dict[str, JsonValue] = {
        "columns": ["firstName", "lastName", "city", "state"],
        "rows": rows,
    }
    if not equal_json(run.result, result):
        raise EvidenceError("SQL result differs from grouped address rows")
    if not equal_json(run.post_state, case):
        raise EvidenceError("SQL execution changed the fixture input")
    frame: dict[str, JsonValue] = {
        "stepId": "query-result",
        "codeLines": list(LEFT_JOIN_ADAPTER.code_lines),
        "explanation": LEFT_JOIN_ADAPTER.explanation,
        "state": {"kind": "table", **result},
        "highlights": [],
    }
    if len(run.frames) != 1 or not equal_json(run.frames[0], frame):
        raise EvidenceError("SQL frame differs from grouped address rows")
