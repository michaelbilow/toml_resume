"""Main module."""

import toml

_ORDERING = "ordering"
_VALUE = "value"

RESUME_TOP_LEVEL_SCHEMA_KEYS = {
    "basics",
    "profiles",
    "work",
    "volunteer",
    "education",
    "awards",
    "publications",
    "skills",
    "languages",
    "interests",
    "references",
    "projects",
}


def to_resume_toml(d: dict, filename: str):
    d = add_ordering_to_dict(d)
    with open(filename, 'w') as f:
        toml.dump(f, d)
    return


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
    return all(isinstance(li, dict) and
               set(li.keys()) == {_ORDERING, _VALUE} for li in lst)


def add_ordering_to_list(lst: list) -> list:
    if already_ordered(lst):
        return lst
    return [
        {
            _ORDERING: ind,
            _VALUE: add_ordering_to_list_item(v)
        }
        for ind, v in enumerate(lst)
    ]


def add_ordering_to_list_item(list_item):
    if isinstance(list_item, dict):
        return add_ordering_to_dict(list_item)
    elif isinstance(list_item, list):
        return add_ordering_to_list(list_item)
    else:
        return list_item


if __name__ == "__main__":
    pass
