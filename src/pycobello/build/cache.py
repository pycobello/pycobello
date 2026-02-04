"""Cache manifest (JSON) read/write and hashing. Step 7."""

import hashlib
import json
from pathlib import Path


def content_sha256(content: bytes | str) -> str:
    """SHA256 hex digest of content."""
    if isinstance(content, str):
        content = content.encode("utf-8")
    return hashlib.sha256(content).hexdigest()


def file_sha256(path: Path) -> str:
    """SHA256 of file contents."""
    return content_sha256(path.read_bytes())


def load_cache(cache_path: Path) -> dict:
    """Load cache.json; return empty dict if missing."""
    if not cache_path.is_file():
        return {"files": {}, "outputs": {}, "source_to_output": {}}
    return json.loads(cache_path.read_text())


def save_cache(cache_path: Path, data: dict) -> None:
    """Write cache.json."""
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps(data, indent=2))
