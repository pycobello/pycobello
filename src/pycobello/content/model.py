"""Dataclasses for content items."""

from dataclasses import dataclass
from datetime import date
from enum import Enum
from pathlib import Path


class ContentKind(str, Enum):
    """Post or page."""

    POST = "post"
    PAGE = "page"


@dataclass
class ContentItem:
    """A single content file (post or page)."""

    kind: ContentKind
    source_path: Path
    front_matter: dict
    body_markdown: str
    slug: str
    url_path: str
    date: date | None = None
    template: str | None = None
