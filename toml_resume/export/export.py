import shutil
import subprocess
from functools import reduce
from pathlib import Path
from typing import Dict, List, Optional

from toml_resume.export.add_markdown import convert_markdown_and_add_css
from toml_resume.toml_resume import (clean_flavors, read_resume_toml,
                                     write_resume_json)

DEFAULT_THEME = "macchiato"
OUTPUT_PATH = Path("target/")
RESUME_DOT_JSON = "resume.json"
RESUME_DOT_PDF = "resume.pdf"

DEFAULT_PUPPETEER_OPTS = {
    "--margin-top": "0",
    "--margin-right": "0",
    "--margin-bottom": "0",
    "--margin-left": "0",
    "--format": "A4",
}


def generate_resume_from_toml_and_config(toml_filename: str,
                                         output_filename: str, config: dict):
    generate_resume_from_toml(toml_filename, config.get("flavors", None),
                              output_filename, config.get("theme", None),
                              config.get("puppeteer_opts", None))


def generate_resume_from_toml(toml_filename: str,
                              flavors: Optional[List[str]] = None,
                              output_filename: Optional[str] = None,
                              theme: Optional[str] = None,
                              puppeteer_opts: Optional[Dict[str, str]] = None):
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
    if not theme:
        theme = DEFAULT_THEME
    d = read_resume_toml(toml_filename)
    json_filename = OUTPUT_PATH.joinpath(RESUME_DOT_JSON)
    write_resume_json(d, json_filename, flavors)
    if not output_filename:
        flavor_text = '' if not flavors else ''.join(clean_flavors(flavors))
        output_filename = f"resume{flavor_text}.pdf"

    generate_resume_from_json(json_filename,
                              output_filename=output_filename,
                              theme=theme,
                              puppeteer_opts=puppeteer_opts)


def generate_resume_from_json(json_filename: str,
                              output_filename: str = RESUME_DOT_PDF,
                              theme: str = DEFAULT_THEME,
                              puppeteer_opts: Optional[Dict[str, str]] = None):
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
    if not puppeteer_opts:
        puppeteer_opts = DEFAULT_PUPPETEER_OPTS
    if not output_filename:
        output_filename = str(Path(json_filename).with_suffix(".pdf"))
    output_filename = OUTPUT_PATH.joinpath(output_filename)

    tmp_resume_filename = OUTPUT_PATH.joinpath(RESUME_DOT_JSON)
    if not json_filename == tmp_resume_filename:
        shutil.copy(json_filename, tmp_resume_filename)

    raw_html_filename = output_filename.with_name(
        f"{output_filename.stem}_raw").with_suffix(".html")
    export_with_json_resume(raw_html_filename, theme)

    clean_html_filename = output_filename.with_suffix(".html")
    convert_markdown_and_add_css(raw_html_filename, clean_html_filename)

    print_with_puppeteer(clean_html_filename, output_filename, puppeteer_opts)
    output_resume_filename = tmp_resume_filename.with_name(output_filename.stem).with_suffix(".json")
    shutil.move(tmp_resume_filename, output_resume_filename)
    return


def export_with_json_resume(output_filename: Path, theme: str):
    print(output_filename, theme)
    try:
        print(str(output_filename.parent.absolute()))
        subprocess.run(["resume", "export",
                        str(output_filename.name), "--theme", theme],
                       cwd=str(output_filename.parent.absolute()))
    except FileNotFoundError as e:
        print("Install resume-cli: `npm install -g resume-cli`")
        raise e
    return


def print_with_puppeteer(input_html_filename: str, output_filename: str,
                         puppeteer_opts: dict):
    puppeteer_opts_list = list(
        reduce(lambda x, y: x + y, puppeteer_opts.items()))
    try:
        subprocess.run([
            "puppeteer", *puppeteer_opts_list, "print", input_html_filename,
            output_filename
        ])
    except FileNotFoundError as e:
        print("Install puppeteer: `npm install -g puppeteer`")
        raise e
    return
