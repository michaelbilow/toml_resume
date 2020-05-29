"""Main module."""

import functools
import json
import jsonschema
from typing import Dict, List, Optional, Any

import toml

from toml_resume.constants import (_DEFAULT, RESUME_JSON_SCHEMA)
from toml_resume.encoder import neat_encoder


def read_resume_json(filename: str) -> Dict[str, Any]:
    d = json.load(open(filename, 'r'))
    jsonschema.validate(d, RESUME_JSON_SCHEMA)
    return d


def read_resume_toml(filename: str) -> Dict[str, Any]:
    d = toml.load(open(filename, 'r'))
    return d


def write_resume_toml(d: Dict[str, Any], filename: str) -> None:
    with open(filename, 'w') as f:
        toml.dump(d, f, neat_encoder)


def write_resume_json(d: dict, filename: str, flavors: Optional[List[str]] = None) -> None:
    if not flavors:
        flavors = []
    if _DEFAULT not in flavors:
        flavors.append(_DEFAULT)
    flavors = clean_flavors(flavors)
    output = combine_all_flavors(d, flavors)
    jsonschema.validate(output, RESUME_JSON_SCHEMA)
    with open(filename, 'w') as f:
        json.dump(output, f, indent=2)


def is_flavor(s: str) -> bool:
    return s.startswith("_")


def clean_flavors(flavors: List[str]) -> List[str]:
    return [f"_{x}" if not is_flavor(x) else x for x in flavors]


def get_default(d: Dict[str, Any]) -> Dict[str, Any]:
    output_dict = {_DEFAULT: {}}
    for k, v in d.items():
        if is_flavor(k):
            output_dict[k] = v
        else:
            output_dict[_DEFAULT][k] = v
    return output_dict


def combine_all_flavors(d: Dict[str, Any], flavors: List[str]) -> Dict[str, Any]:
    with_default = get_default(d)
    to_combine = [flatten_flavors_dict(with_default.get(flavor, {}), flavors)
                  for flavor in flavors]
    return functools.reduce(lambda x, y: {**y, **x}, to_combine)


def first_present_key(d: Dict[str, Any], lst: List[str]) -> Optional[str]:
    for s in lst:
        if s in d:
            return s
    return None


def flatten_flavors_dict(d: dict, flavors: List[str]) -> dict:
    output_dict = {}
    if not d:
        return {}
    if not isinstance(d, dict):
        print(d)
        raise ValueError
    if all(is_flavor(x) for x in d):
        chosen_key = first_present_key(d, flavors)
        chosen_value = d[chosen_key]
        if isinstance(chosen_value, dict):
            return flatten_flavors_dict(chosen_value, flavors)
        elif isinstance(chosen_value, list):
            return flatten_flavors_list(chosen_value, flavors)
        else:
            return chosen_value
    for k, v in d.items():
        if isinstance(v, dict):
            if all(is_flavor(x) for x in v):
                chosen_key = first_present_key(v, flavors)
                if chosen_key:
                    chosen_value = v[chosen_key]
                    if isinstance(chosen_value, dict):
                        output_dict[k] = flatten_flavors_dict(chosen_value, flavors)
                    elif isinstance(chosen_value, list):
                        output_dict[k] = flatten_flavors_list(chosen_value, flavors)
                    else:
                        output_dict[k] = chosen_value
            else:
                output_dict[k] = flatten_flavors_dict(v, flavors)
        elif isinstance(v, list):
            output_dict[k] = flatten_flavors_list(v, flavors)
        else:
            output_dict[k] = v
    return output_dict


def flatten_flavors_list(l: List[Any], flavors: List[str]) -> List[Any]:
    output_lst = []
    for li in l:
        if isinstance(li, list):
            output_lst.append(flatten_flavors_list(li, flavors))
        elif isinstance(li, dict):
            output_lst.append(flatten_flavors_dict(li, flavors))
        else:
            output_lst.append(li)
    return [x for x in output_lst if x]


if __name__ == "__main__":
    pass
