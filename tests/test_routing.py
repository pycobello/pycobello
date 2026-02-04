"""Slug and output path routing."""

from pathlib import Path

from pycobello.content.model import ContentKind
from pycobello.render.routing import (
    output_path_for_item,
    slug_from_item,
)


def test_slug_from_frontmatter_slug() -> None:
    """Explicit slug in front matter is used."""
    path = Path("dummy.md")
    fm = {"slug": "my-custom-slug"}
    assert slug_from_item(path, fm, ContentKind.POST) == "my-custom-slug"


def test_slug_from_title() -> None:
    """Slug derived from title when no slug."""
    path = Path("dummy.md")
    fm = {"title": "Hello World"}
    assert slug_from_item(path, fm, ContentKind.PAGE) == "hello-world"


def test_slug_from_filename() -> None:
    """Slug from filename when no slug/title."""
    path = Path("some-post.md")
    fm = {}
    assert slug_from_item(path, fm, ContentKind.PAGE) == "some-post"


def test_slug_from_filename_strips_date_prefix() -> None:
    """Post filename YYYY-MM-DD-name yields name."""
    path = Path("2024-01-15-hello.md")
    fm = {}
    assert slug_from_item(path, fm, ContentKind.POST) == "hello"


def test_output_path_clean_urls() -> None:
    """Clean URLs produce path/index.html."""
    out = Path("/out")
    assert output_path_for_item(out, "/blog/hello/", clean_urls=True) == Path(
        "/out/blog/hello/index.html"
    )
    assert output_path_for_item(out, "/", clean_urls=True) == Path("/out/index/index.html")


def test_output_path_no_clean_urls() -> None:
    """Without clean URLs produce path.html."""
    out = Path("/out")
    assert output_path_for_item(out, "/about/", clean_urls=False) == Path("/out/about.html")
