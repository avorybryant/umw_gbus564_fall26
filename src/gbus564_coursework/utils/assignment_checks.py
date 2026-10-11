"""Self-check helpers for assignment Part A checkpoints.

Checkpoints are student-facing feedback, not the grade: "if this passes,
you're on track." Import in an assignment notebook the same way
utils/course_data.py is imported (repo-resolve-or-clone, see
utils/assignment_template.ipynb Setup cell):

    from utils.assignment_checks import check_equal, check_close, check_in_range, check_shape, check_type

Each helper prints a checkmark on success and raises AssertionError with a
student-readable message on failure — nothing here is hidden or graded
directly; grading Part A is "did the checkpoints pass."
"""

import numpy as np


def _ok(label: str) -> None:
    print(f"✓ {label}")


def check_equal(actual, expected, label: str) -> None:
    assert actual == expected, f"✗ {label}: expected {expected!r}, got {actual!r}"
    _ok(label)


def check_close(actual, expected, label: str, rtol: float = 1e-3, atol: float = 1e-6) -> None:
    assert np.isclose(actual, expected, rtol=rtol, atol=atol), (
        f"✗ {label}: expected ≈{expected!r}, got {actual!r}"
    )
    _ok(label)


def check_in_range(actual, low, high, label: str) -> None:
    assert low <= actual <= high, (
        f"✗ {label}: expected between {low!r} and {high!r}, got {actual!r}"
    )
    _ok(label)


def check_shape(actual, expected_shape, label: str) -> None:
    actual_shape = tuple(actual.shape)
    assert actual_shape == tuple(expected_shape), (
        f"✗ {label}: expected shape {tuple(expected_shape)}, got {actual_shape}"
    )
    _ok(label)


def check_type(actual, expected_type, label: str) -> None:
    assert isinstance(actual, expected_type), (
        f"✗ {label}: expected a {expected_type.__name__}, got {type(actual).__name__}"
    )
    _ok(label)
