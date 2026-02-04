"""Internal link check using markdown-it tokens. Step 9."""

from pathlib import Path

from pycobello.content.discovery import discover_items
from pycobello.content.markdown import get_tokens


def check_internal_links(content_dir: Path, config) -> list[str]:
    """Extract link hrefs from markdown; resolve .md/extensionless to known URLs; report broken."""
    coll_dict = {"posts": config.collections.posts, "pages": config.collections.pages}
    items = discover_items(content_dir, coll_dict, ignore=config.build.ignore)
    known_urls: set[str] = set()
    for item in items:
        known_urls.add(item.url_path.rstrip("/") or "/")
        known_urls.add(item.url_path)
    errors: list[str] = []
    for item in items:
        tokens = get_tokens(item.body_markdown)
        for t in _iter_links(tokens):
            href = getattr(t, "attrGet", lambda _: None)("href") or ""
            if not href or href.startswith(("#", "http://", "https://", "mailto:")):
                continue
            if href.startswith("/"):
                target = href.rstrip("/") or "/"
            else:
                target = _resolve_relative(href, item.url_path)
            if target and target not in known_urls and not target.startswith("http"):
                errors.append(f"{item.source_path}: Broken internal link to {href}")
    return errors


def _iter_links(tokens):
    """Yield link_open tokens (use attrGet('href'))."""
    for t in tokens:
        if t.type == "link_open":
            yield t
        try:
            children = t.children
        except AttributeError:
            children = []
        yield from _iter_links(children or [])


def _resolve_relative(href: str, base_url_path: str) -> str:
    """Resolve relative href from base url path. Best-effort."""
    base = base_url_path.rstrip("/") or "/"
    if base != "/":
        base = base + "/"
    if href.endswith(".md"):
        href = href[:-3]
    if "/" in base:
        parts = base.split("/")
        parts.pop()
        while href.startswith("../"):
            href = href[3:]
            if parts:
                parts.pop()
        base = "/" + "/".join(parts) + "/" if parts else "/"
    return (base.rstrip("/") + "/" + href.lstrip("/")).rstrip("/") or "/"
