"""Discover content files in content dir. Filled in Step 4."""

from pathlib import Path

from pycobello.content.model import ContentItem, ContentKind


def discover_items(
    content_dir: Path,
    collections: dict,
    ignore: list[str] | None = None,
) -> list[ContentItem]:
    """Find all markdown files in collection paths. Returns list of ContentItems (parsed in pipeline)."""
    from pycobello.content.frontmatter import parse_frontmatter
    from pycobello.render.routing import slug_from_item

    ignore = ignore or []
    items: list[ContentItem] = []
    for name, coll in collections.items():
        if name == "posts":
            kind = ContentKind.POST
            path_dir = content_dir / getattr(coll, "path", "posts")
        elif name == "pages":
            kind = ContentKind.PAGE
            path_dir = content_dir / getattr(coll, "path", "pages")
        else:
            continue
        if not path_dir.is_dir():
            continue
        for path in path_dir.rglob("*.md"):
            if any(p in path.parts for p in ignore):
                continue
            try:
                raw = path.read_text()
            except OSError:
                continue
            fm, body = parse_frontmatter(raw)
            slug = slug_from_item(path, fm, kind)
            url_prefix = getattr(coll, "url_prefix", "") or ""
            if url_prefix:
                url_path = f"/{url_prefix.rstrip('/')}/{slug}/"
            else:
                url_path = f"/{slug}/"
            from datetime import date as date_type

            d = None
            if "date" in fm and fm["date"]:
                try:
                    d = date_type.fromisoformat(str(fm["date"]).split("T")[0])
                except (ValueError, TypeError):
                    pass
            template = fm.get("template") or getattr(coll, "template", "")
            items.append(
                ContentItem(
                    kind=kind,
                    source_path=path,
                    front_matter=fm,
                    body_markdown=body,
                    slug=slug,
                    url_path=url_path.rstrip("/") or "/",
                    date=d,
                    template=template or None,
                )
            )
    return items
