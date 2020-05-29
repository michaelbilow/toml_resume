import subprocess
import os

from typing import Optional, List

from toml_resume.toml_resume import read_resume_toml, write_resume_json, clean_flavors
from toml_resume.export.add_markdown import convert_markdown_and_add_css
import shutil

DEFAULT_THEME = "macchiato"
RESUME_DOT_JSON = "resume.json"
RESUME_DOT_PDF = "resume.pdf"


def generate_resume_from_toml(toml_filename: str,
                              flavors: Optional[List[str]] = None,
                              output_filename: Optional[str] = None,
                              theme: str = DEFAULT_THEME):
    d = read_resume_toml(toml_filename)
    write_resume_json(d, RESUME_DOT_JSON, flavors)
    if not output_filename:
        flavor_text = '' if not flavors else ''.join(clean_flavors(flavors))
        output_filename = f"resume{flavor_text}.pdf"

    generate_resume_from_json(RESUME_DOT_JSON, output_filename=output_filename, theme=theme)


def generate_resume_from_json(json_filename: str,
                              output_filename: str = RESUME_DOT_PDF,
                              theme: str = DEFAULT_THEME):
    if not output_filename:
        output_filename = f"{os.path.splitext(json_filename)[0]}.pdf"
    if json_filename != RESUME_DOT_JSON:
        shutil.copy(json_filename, RESUME_DOT_JSON)

    output_filename_stub = os.path.splitext(output_filename)[0]

    raw_html_filename = f"{output_filename_stub}_raw.html"
    clean_html_filename = f"{output_filename_stub}.html"
    subprocess.run(["resume", "export", raw_html_filename, "--theme", theme])
    convert_markdown_and_add_css(raw_html_filename, clean_html_filename)
    subprocess.run(["puppeteer", "--margin-top", "0", "--margin-right",  "0",
                    "--margin-bottom", "0", "--margin-left", "0", "--format", "A4",
                    "print", clean_html_filename, output_filename])

    if json_filename != RESUME_DOT_JSON:
        os.remove(RESUME_DOT_JSON)
