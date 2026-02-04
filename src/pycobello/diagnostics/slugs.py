"""Duplicate URL / slug collision check. Step 9."""

from pathlib import Path

from pycobello.content.discovery import discover_items


def check_duplicate_urls(content_dir: Path, config) -> list[str]:
    """Return list of error messages for duplicate url_path."""
    coll_dict = {"posts": config.collections.posts, "pages": config.collections.pages}
    items = discover_items(content_dir, coll_dict, ignore=config.build.ignore)
    seen: dict[str, str] = {}
    errors: list[str] = []
    for item in items:
        if item.url_path in seen:
            errors.append(
                f"Duplicate URL {item.url_path}: {seen[item.url_path]} and {item.source_path}"
            )
        else:
            seen[item.url_path] = str(item.source_path)
    return errors
