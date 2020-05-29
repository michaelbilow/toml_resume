import fire
from toml_resume.toml_resume import *
from toml_resume.export.export import generate_resume_from_toml, \
    generate_resume_from_json, DEFAULT_THEME
from typing import Optional, List
import os


class TomlResume:

    def toToml(self, filename: str,
               output_filename: Optional[str] = None):
        if not output_filename:
            output_filename = f"{os.path.splitext(filename)[0]}.toml"
        d = read_resume_json(filename)
        write_resume_toml(d, output_filename)

    def toJson(self, filename: str,
               output_filename: Optional[str] = None,
               flavors: Optional[List[str]] = None):
        if not output_filename:
            flavor_text = '' if not flavors else ''.join(clean_flavors(flavors))
            output_filename = f"{os.path.splitext(filename)[0]}{flavor_text}.json"
        d = read_resume_toml(filename)
        write_resume_json(d, output_filename, flavors)

    def toPdf(self, filename: str,
              output_filename: Optional[str] = None,
              flavors: Optional[List[str]] = None,
              theme: str = None):
        if not theme:
            theme = DEFAULT_THEME
        if filename.endswith('.toml'):
            generate_resume_from_toml(filename, flavors, output_filename, theme)
        if filename.endswith('.json'):
            generate_resume_from_json(filename, output_filename, theme)


if __name__ == "__main__":
    fire.Fire(TomlResume)
