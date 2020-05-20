#!/usr/bin/env python
"""Tests for `toml_resume` package."""
# pylint: disable=redefined-outer-name

import random

import pytest

from toml_resume import toml_resume
from toml_resume.constants import (_ORDERING, _VALUE,
                                   RESUME_TOP_LEVEL_SCHEMA_KEYS)


def test_merge_lists():
    l1 = [{_ORDERING: 0, _VALUE: "x"}, {_ORDERING: 2, _VALUE: "z"}]
    l2 = [{_ORDERING: 1, _VALUE: "y"}]
    print(toml_resume.sort_merge_lists(l1, l2))
    assert toml_resume.sort_merge_lists(l1, l2) == [l1[0], l2[0], l1[1]]


def test_fail_merge_lists():
    l1 = [{_ORDERING: 0, _VALUE: "x"}, {_ORDERING: 2, _VALUE: "z"}]
    l2 = [{_ORDERING: 1, _VALUE: "y"}, {_ORDERING: 2, _VALUE: "q"}]
    try:
        toml_resume.sort_merge_lists(l1, l2)
    except AssertionError:
        assert True
        return
    assert False


def test_fail_on_multiple_non_mergeable_values():
    key = random.choice(list(RESUME_TOP_LEVEL_SCHEMA_KEYS))
    d1 = {key: "v1"}
    d2 = {key: "v2"}
    try:
        toml_resume.recursively_sort_combine([d1, d2])
    except ValueError:
        assert True
        return
    assert False
