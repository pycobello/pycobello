"""Required front matter validation for posts. Step 9."""

from pathlib import Path

from pycobello.content.frontmatter import parse_frontmatter
from pycobello.errors import FrontMatterError


def check_required_frontmatter(content_dir: Path, config) -> list[str]:
    """Check posts have title and date. Return list of error messages."""
    errors: list[str] = []
    posts_dir = content_dir / config.collections.posts.path
    if not posts_dir.is_dir():
        return errors
    for path in posts_dir.rglob("*.md"):
        if any(p in path.parts for p in (config.build.ignore or [])):
            continue
        try:
            raw = path.read_text()
        except OSError:
            continue
        try:
            fm, _ = parse_frontmatter(raw)
        except FrontMatterError as e:
            errors.append(f"{path}: Invalid front matter: {e}")
            continue
        if not fm.get("title"):
            errors.append(f"{path}: Post missing required 'title' in front matter.")
        if not fm.get("date"):
            errors.append(f"{path}: Post missing required 'date' in front matter.")
    return errors
