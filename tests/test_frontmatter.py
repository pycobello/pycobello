"""Front matter parsing."""

import pytest

from pycobello.content.frontmatter import parse_frontmatter
from pycobello.errors import FrontMatterError


def test_parse_frontmatter_with_delimiter() -> None:
    """Standard front matter returns dict and body."""
    from datetime import date

    text = "---\ntitle: Hello\ndate: 2024-01-15\n---\n\nBody here."
    fm, body = parse_frontmatter(text)
    assert fm["title"] == "Hello"
    assert fm["date"] == date(2024, 1, 15)  # PyYAML parses YYYY-MM-DD as date
    assert body.strip() == "Body here."


def test_parse_frontmatter_without_delimiter() -> None:
    """No leading --- returns empty dict and full text."""
    text = "No front matter.\nJust body."
    fm, body = parse_frontmatter(text)
    assert fm == {}
    assert body == text


def test_parse_frontmatter_empty() -> None:
    """Empty between delimiters returns empty dict."""
    text = "---\n---\nBody"
    fm, body = parse_frontmatter(text)
    assert fm == {}
    assert body.strip() == "Body"


def test_parse_frontmatter_invalid_yaml() -> None:
    """Invalid YAML in front matter raises FrontMatterError."""
    text = "---\ntitle: [unclosed\n---\nBody"
    with pytest.raises(FrontMatterError):
        parse_frontmatter(text)
