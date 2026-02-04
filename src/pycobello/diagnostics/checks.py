"""Check runner and core checks. Step 9."""

from pathlib import Path

from pycobello.config.load import load_config
from pycobello.errors import ConfigError


def run_checks(project_root: str) -> None:
    """Run all diagnostics; exit non-zero on any error."""
    try:
        config = load_config(project_root)
    except ConfigError as e:
        _err(str(e))
        raise SystemExit(1) from e

    root = Path(project_root).resolve()
    content_dir = root / config.build.content_dir
    errors: list[str] = []

    from pycobello.diagnostics.slugs import check_duplicate_urls
    from pycobello.diagnostics.frontmatter import check_required_frontmatter
    from pycobello.diagnostics.links import check_internal_links

    errors.extend(check_duplicate_urls(content_dir, config))
    errors.extend(check_required_frontmatter(content_dir, config))
    errors.extend(check_internal_links(content_dir, config))

    if errors:
        for e in errors:
            _err(e)
        raise SystemExit(1)


def _err(msg: str) -> None:
    import sys
    print(msg, file=sys.stderr)
