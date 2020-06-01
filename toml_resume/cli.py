import os
from typing import List, Optional

import fire

from toml_resume.export.export import (DEFAULT_THEME,
                                       generate_resume_from_json,
                                       generate_resume_from_toml,
                                       generate_resume_from_toml_and_config)
from toml_resume.toml_resume import *


class TomlResume:
    def toToml(self, filename: str, output_filename: Optional[str] = None):
        if not output_filename:
            output_filename = f"{os.path.splitext(filename)[0]}.toml"
        d = read_resume_json(filename)
        write_resume_toml(d, output_filename)

    def reformatToml(self,
                     filename: str,
                     output_filename: Optional[str] = None):
        if not output_filename:
            output_filename = f"{os.path.splitext(filename)[0]}_reformatted.toml"
        d = read_resume_toml(filename)
        write_resume_toml(d, output_filename)

    def toJson(self,
               filename: str,
               flavors: Optional[List[str]] = None,
               output_filename: Optional[str] = None):
        if not output_filename:
            flavor_text = '' if not flavors else ''.join(
                clean_flavors(flavors))
            output_filename = f"{os.path.splitext(filename)[0]}{flavor_text}.json"
        d = read_resume_toml(filename)
        write_resume_json(d, output_filename, flavors)

    def toPdf(self,
              filename: str,
              flavors: Optional[List[str]] = None,
              output_filename: Optional[str] = None,
              theme: Optional[str] = None):
        if isinstance(flavors, str):
            flavors = [flavors]
        if isinstance(flavors, tuple):
            flavors = list(flavors)
        if not theme:
            theme = DEFAULT_THEME
        if filename.endswith('.toml'):
            generate_resume_from_toml(filename, flavors, output_filename,
                                      theme)
        if filename.endswith('.json'):
            generate_resume_from_json(filename, output_filename, theme)

    def toPdfs(self, filename: str, config_filename: str):
        output_configs = toml.load(config_filename)
        for output_stub, config in output_configs.items():
            output_filename = f"{output_stub}.pdf"
            generate_resume_from_toml_and_config(filename, output_filename,
                                                 config)


if __name__ == "__main__":
    fire.Fire(TomlResume)
