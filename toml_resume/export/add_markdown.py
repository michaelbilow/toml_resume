import re

ITALICIZE = {"__([^_]+)__": r"<i>\1</i>"}
STRONG_TO_BOLD = {"([</])strong>": r"\1b>"}
BOLD = {"[*]{2}([^*]+)[*]{2}": r"<b>\1</b>"}
EM_TO_ITALIC = {"([</])em>": r"\1i>"}
LINK = {r"\[([^\]]+)\]\(([^)]+)\)": r'<a href="\2">\1</a>'}
EM_DASH = {r"(\w)--(\w)": r"\1&mdash;\2"}
EM_DASH_DATE = {r'(<span class="endDate">) - ': r"\1&mdash; "}
MARKDOWN_DICT = {
    **ITALICIZE,
    **BOLD,
    **LINK,
    **EM_DASH,
    **EM_DASH_DATE,
    **STRONG_TO_BOLD,
    **EM_TO_ITALIC,
}

END_OF_STYLE = "</style>"

MY_CSS_DICT = {
    ".left-column": {"width": "180px"},
    ".info-tag-container .info-text": {"width": "159px"},
    ".keyline": {"margin": "4px 0 5px"},
    ".container": {"padding-top": "10px"},
    ".summary": {"margin": "2px 0 2px"},
    ".item": {"margin-bottom": "6px"},
    ".interests-container .item": {"margin-bottom": "3px"},
    "ul li": {"padding-bottom": "2px"},
    "ul" : {"list-style-type": "square"},
    ".page": {"padding-top":"20px"}
}
MY_CSS_COMMENT = "\n\n/* ADDED CSS */\n\n"


def basic_markdown(s):
    for k, v in MARKDOWN_DICT.items():
        s = re.compile(k).sub(v, s)
    return s


def inject_css(css_dict):
    output_style_strs = []
    for selector, style_dict in css_dict.items():
        css_style = "\n".join(
            [f"\t{element}: {value};" for element, value in style_dict.items()]
        )
        output_style_str = f"{selector} {{\n{css_style}\n}}"
        output_style_strs.append(output_style_str)
    output_css = "\n\n".join(output_style_strs)
    return f"{MY_CSS_COMMENT}{output_css}{MY_CSS_COMMENT}"


def convert_markdown_and_add_css(input_filename, output_filename):
    output_lines = []
    for line in open(input_filename, "r"):
        if line.strip() == END_OF_STYLE:
            output_lines.append(inject_css(MY_CSS_DICT))
        output_lines.append(basic_markdown(line))

    with open(output_filename, "w") as f:
        for line in output_lines:
            f.write(line)
