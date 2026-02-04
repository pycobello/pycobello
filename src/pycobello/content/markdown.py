"""Markdown rendering via markdown-it-py. Step 4."""

from markdown_it import MarkdownIt


def _md() -> MarkdownIt:
    return MarkdownIt()


def markdown_to_html(text: str) -> str:
    """Render Markdown to HTML."""
    return _md().render(text)


def get_tokens(text: str):
    """Return token stream for diagnostics (e.g. link extraction)."""
    return _md().parse(text)
