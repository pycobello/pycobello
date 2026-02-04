"""URL and output path computation. Step 4."""

from pathlib import Path

from slugify import slugify

from pycobello.content.model import ContentKind


def slug_from_item(path: Path, front_matter: dict, kind: ContentKind) -> str:
    """Slug from frontmatter slug, or title, or filename."""
    if front_matter.get("slug"):
        return slugify(str(front_matter["slug"]), lowercase=True)
    if front_matter.get("title"):
        return slugify(str(front_matter["title"]), lowercase=True)
    # From filename: strip date prefix and extension
    name = path.stem
    if kind == ContentKind.POST and len(name) >= 11 and name[4] == "-" and name[7] == "-":
        try:
            int(name[:4])
            int(name[5:7])
            int(name[8:10])
            name = name[11:].lstrip("-")
        except (ValueError, IndexError):
            pass
    return slugify(name, lowercase=True) or "untitled"


def url_for_item(
    slug: str,
    kind: ContentKind,
    url_prefix: str,
) -> str:
    """URL path for an item (e.g. /blog/hello/ or /about/)."""
    prefix = (url_prefix or "").strip("/")
    if prefix:
        return f"/{prefix}/{slug}/"
    return f"/{slug}/"


def output_path_for_item(
    output_dir: Path,
    url_path: str,
    clean_urls: bool = True,
) -> Path:
    """Output file path. Clean URLs -> .../index.html."""
    path = url_path.strip("/") or "index"
    if clean_urls:
        return output_dir / path / "index.html"
    return output_dir / f"{path}.html"
