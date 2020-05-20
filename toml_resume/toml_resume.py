"""Main module."""

import functools
import json
from collections import defaultdict
from typing import Dict, List, Optional, Set, Tuple

import toml

from toml_resume.constants import (_DEFAULT, _ORDERING, _VALUE,
                                   RESUME_TOP_LEVEL_SCHEMA_KEYS)


def to_resume_json(d: dict, filename: str, flavors: Set[str] = None):
    if flavors is None:
        flavors = {"default"}

    output = combine_all_flavors(d, flavors)

    with open(filename, 'w') as f:
        json.dump(d, f)


def combine_all_flavors(d: dict, flavors: Set[str]):
    to_combine = [d[flavor] for flavor in flavors]
    return recursively_sort_combine(to_combine)


def recursively_sort_combine(ds: List[dict]):
    functools.reduce(sort_combine, ds)


def sort_combine(d1: dict, d2: dict):
    output_dict = {}
    for k in set(list(d1.keys()) + list(d2.keys())):
        if k not in d2:
            output_dict[k] = d1[k]
            continue
        if k not in d1:
            output_dict[k] = d2[k]
            continue
        v1 = d1[k]
        v2 = d2[k]
        if isinstance(v1, dict):
            output_dict[k] = sort_combine(v1, v2)
        elif isinstance(v1, list):
            output_dict = sort_merge_lists(v1, v2)
        else:
            raise ValueError(f"conflicting values for {k}:\n\n{v1}\n&\n{v2}")
    return output_dict


def sort_merge_lists(l1: list, l2: list):
    raw_output = l1 + l2
    output = sorted(raw_output, key=lambda x: x[_ORDERING])
    assert len(set(x[_ORDERING] for x in output)) == len(output)
    return output


def to_resume_toml(d: dict, filename: str):
    d = add_ordering_to_dict(d)
    d = add_default_extension(d)
    with open(filename, 'w') as f:
        toml.dump(d, f)
    return


def add_default_extension(d: dict):
    output_dict = defaultdict(dict)
    for k in d.keys():
        if k in RESUME_TOP_LEVEL_SCHEMA_KEYS:
            output_dict[_DEFAULT][k] = d[k]
    return output_dict


def add_ordering_to_dict(d: dict) -> dict:
    output = {}
    for k, v in d.items():
        if isinstance(v, dict):
            output[k] = add_ordering_to_dict(v)
        elif isinstance(v, list):
            output[k] = add_ordering_to_list(v)
        else:
            output[k] = v
    return output


def already_ordered(lst: list) -> bool:
    return all(
        isinstance(li, dict) and set(li.keys()) == {_ORDERING, _VALUE}
        for li in lst)


def add_ordering_to_list(lst: list) -> list:
    if already_ordered(lst):
        return lst
    return [{
        _ORDERING: ind,
        _VALUE: add_ordering_to_list_item(v)
    } for ind, v in enumerate(lst)]


def add_ordering_to_list_item(list_item):
    if isinstance(list_item, dict):
        return add_ordering_to_dict(list_item)
    elif isinstance(list_item, list):
        return add_ordering_to_list(list_item)
    else:
        return list_item


if __name__ == "__main__":
    pass
