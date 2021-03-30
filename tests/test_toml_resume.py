#!/usr/bin/env python
"""Tests for `toml_resume` package."""
# pylint: disable=redefined-outer-name

import json
import random

import pytest

from toml_resume import toml_resume
from toml_resume.constants import _ORDERING, _VALUE, RESUME_TOP_LEVEL_SCHEMA_KEYS

# def test_merge_lists():
#     l1 = [{_ORDERING: 0, _VALUE: "x"}, {_ORDERING: 2, _VALUE: "z"}]
#     l2 = [{_ORDERING: 1, _VALUE: "y"}]
#     print(toml_resume.sort_merge_lists(l1, l2))
#     assert toml_resume.sort_merge_lists(l1, l2) == [l1[0], l2[0], l1[1]]
#
#
# def test_favor_second_list_in_merge():
#     l1 = [{_ORDERING: 0, _VALUE: "x"}, {_ORDERING: 2, _VALUE: "z"}]
#     l2 = [{_ORDERING: 1, _VALUE: "y"}, {_ORDERING: 2, _VALUE: "q"}]
#     assert toml_resume.sort_merge_lists(l1, l2) == [l1[0]] + l2
#
#
# def test_favor_second_atomic_value():
#     key = random.choice(list(RESUME_TOP_LEVEL_SCHEMA_KEYS))
#     d1 = {key: "v1"}
#     d2 = {key: "v2"}
#     assert toml_resume.recursively_sort_combine([d1, d2]) == d2
#
#
# def test_merge_mergeable_values():
#     key = random.choice(list(RESUME_TOP_LEVEL_SCHEMA_KEYS))
#     d1 = {key: "v1"}
#     d2 = {key+"_": "v2"}
#     output = toml_resume.recursively_sort_combine([d1, d2])
#     assert output == {**d1, **d2}

# def test_round_trip(capsys):
#     input_filename = 'example/resume.json'
#     d = toml_resume.read_resume_json(input_filename)
#     output_filename = 'example/test_from_json.toml'
#     toml_resume.write_resume_toml(d, output_filename)
#     d2 = toml_resume.read_resume_toml(output_filename)
#     output_filename2 = 'example/test_from_toml.json'
#     toml_resume.write_resume_json(d2, output_filename2)
#
#     assert json.load(open(input_filename)) == json.load(open(output_filename2))


def test_flavors(capsys):
    input_filename = "example/flavors.toml"
    flavors = ["short"]
    d = toml_resume.read_resume_toml(input_filename)
    # print(json.dumps(d, indent=2))
    toml_resume.write_resume_json(d, "example/flavors_none.json")
    toml_resume.write_resume_json(d, "example/flavors_short.json", flavors)


def test_big_flavors(capsys):
    d = {"_default": {"a": 1, "b": 2}, "_other": {"b": 3}}
    assert toml_resume.combine_all_flavors(d, ["_default"]) == d["_default"]
    assert toml_resume.combine_all_flavors(d, ["_other", "_default"]) == {
        "a": 1,
        "b": 3,
    }


def test_get_default(capsys):
    d = {"a": 1, "b": 2, "_other": {"b": 3}}
    assert toml_resume.combine_all_flavors(d, ["_default"]) == {"a": 1, "b": 2}
    assert toml_resume.combine_all_flavors(d, ["_other", "_default"]) == {
        "a": 1,
        "b": 3,
    }


def test_nested_flavors(capsys):
    d = {"a": 1, "b": {"_default": 2, "_other": 3}}
    output = toml_resume.combine_all_flavors(d, ["_other", "_default"])
    print(output)
    assert toml_resume.combine_all_flavors(d, ["_default"]) == {"a": 1, "b": 2}
    assert output == {"a": 1, "b": 3}
