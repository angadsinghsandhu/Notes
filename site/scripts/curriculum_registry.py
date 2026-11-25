"""Explicitly reviewed curriculum implementations and immutable source pins."""

from collections.abc import Callable, Mapping
from dataclasses import dataclass

from .curriculum_longest_substring import verify_eviction, verify_jump
from .curriculum_minimum_path_sum import verify_memoized_grid, verify_row_storage
from .curriculum_trace import JsonValue, PythonAdapter, SqlAdapter, TraceRun
from .curriculum_two_sum import verify_hash, verify_pairs, verify_sorted
from .curriculum_valid_parentheses import verify_stack


@dataclass(frozen=True)
class Enrollment:
    path: str
    sha256: str
    adapter: PythonAdapter | SqlAdapter
    # Receives the unmodified input and actual run, never the declared answers.
    verify: Callable[[JsonValue, TraceRun], None]


type Registry = Mapping[tuple[int, str], Enrollment]
# Add exact source pins and independent checks only after reviewing the implementation.
_TWO_SUM_SHA256 = "b1fde0a1e87d41e1bf480d836c111ccc22b743d53e7dce8a1e0e2b901253f825"
_LONGEST_SUBSTRING_SHA256 = (
    "4a3b2845d0216c2226eb0f3face3b88e431a01d400090ec849098ab2d6aeea7f"
)
_VALID_PARENTHESES_SHA256 = (
    "94ad0b3c9cb1d078a4140fabe87182f785dafab9e7fed62b61d444da69b2a0a5"
)
_MINIMUM_PATH_SUM_SHA256 = (
    "8f11ee992b9ae3158008046c2ce8ca7cf093df5a152030940b63243a41883842"
)
ENROLLED: Registry = {
    (1, "pair-enumeration"): Enrollment(
        "solutions.py", _TWO_SUM_SHA256, PythonAdapter("pair_enumeration"), verify_pairs
    ),
    (1, "sorted-two-pointers"): Enrollment(
        "solutions.py",
        _TWO_SUM_SHA256,
        PythonAdapter("sorted_two_pointers"),
        verify_sorted,
    ),
    (1, "complement-hash"): Enrollment(
        "solutions.py", _TWO_SUM_SHA256, PythonAdapter("complement_hash"), verify_hash
    ),
    (3, "set-eviction"): Enrollment(
        "solutions.py",
        _LONGEST_SUBSTRING_SHA256,
        PythonAdapter("set_eviction"),
        verify_eviction,
    ),
    (3, "last-seen-jump"): Enrollment(
        "solutions.py",
        _LONGEST_SUBSTRING_SHA256,
        PythonAdapter("last_seen_jump"),
        verify_jump,
    ),
    (20, "unmatched-openings"): Enrollment(
        "solutions.py",
        _VALID_PARENTHESES_SHA256,
        PythonAdapter("valid_parentheses"),
        verify_stack,
    ),
    (64, "memoized-grid"): Enrollment(
        "solutions.py",
        _MINIMUM_PATH_SUM_SHA256,
        PythonAdapter("memoized_grid"),
        verify_memoized_grid,
    ),
    (64, "row-storage"): Enrollment(
        "solutions.py",
        _MINIMUM_PATH_SUM_SHA256,
        PythonAdapter("row_storage"),
        verify_row_storage,
    ),
}
