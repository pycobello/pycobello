"""File writing with write-avoidance by hash. Step 6."""

from pathlib import Path

from pycobello.build.cache import content_sha256


def write_if_changed(
    path: Path,
    content: str,
    cached_sha256: str | None,
) -> tuple[bool, str]:
    """Write content to path only if sha256 differs. Return (written, new_sha256)."""
    new_hash = content_sha256(content)
    if cached_sha256 == new_hash:
        return False, new_hash
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True, new_hash
