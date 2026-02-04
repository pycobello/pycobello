"""Copy static assets (theme/static + static/). Step 6."""

import shutil
from pathlib import Path


def copy_assets(
    theme_static: Path,
    user_static: Path,
    output_static: Path,
) -> list[str]:
    """Copy theme/static then static/ to output/static. Return list of copied paths."""
    copied: list[str] = []
    output_static.mkdir(parents=True, exist_ok=True)
    for src_dir in (theme_static, user_static):
        if not src_dir.is_dir():
            continue
        for src in src_dir.rglob("*"):
            if src.is_file():
                rel = src.relative_to(src_dir)
                dst = output_static / rel
                if _should_copy(src, dst):
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src, dst)
                    copied.append(str(dst))
    return copied


def _should_copy(src: Path, dst: Path) -> bool:
    """Copy if dst missing or mtime/size differ."""
    if not dst.exists():
        return True
    stat_s = src.stat()
    stat_d = dst.stat()
    return stat_s.st_mtime != stat_d.st_mtime or stat_s.st_size != stat_d.st_size
