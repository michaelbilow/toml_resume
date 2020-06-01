import json
from pathlib import Path

_ORDERING = "ordering"
_VALUE = "value"
_DEFAULT = "_default"

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

RESUME_JSON_SCHEMA = json.load(
    open(
        str(
            Path(__file__).parent.absolute().joinpath(
                'resources/schema.json')), 'r'))
