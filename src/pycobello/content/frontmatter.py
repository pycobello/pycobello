"""Parse YAML front matter from Markdown. Filled in Step 4."""

import yaml

from pycobello.errors import FrontMatterError


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Return (front_matter_dict, body_markdown). No delimiter -> ({}, full text)."""
    text = text.lstrip("\n")
    if not text.startswith("---"):
        return {}, text
    try:
        idx = text.index("\n---", 3)
    except ValueError:
        return {}, text
    end = idx + 1
    fm_s = text[3:end].strip()
    body = text[end + 4 :].lstrip("\n")
    if not fm_s:
        return {}, body
    try:
        data = yaml.safe_load(fm_s)
    except yaml.YAMLError as e:
        raise FrontMatterError(str(e)) from e
    return (data or {}), body
