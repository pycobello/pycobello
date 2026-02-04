"""Load config from pycobello.yml (YAML only)."""

from pathlib import Path

import yaml

from pycobello.config.models import (
    BuildSettings,
    CollectionConfig,
    CollectionsSettings,
    PluginsSettings,
    PyCobelloSettings,
    SiteSettings,
)
from pycobello.errors import ConfigError


def load_config(project_root: str = ".", config_path: str | None = None) -> PyCobelloSettings:
    """Load and validate config from YAML. Raises ConfigError if missing or invalid."""
    root = Path(project_root).resolve()
    path = root / (config_path or "pycobello.yml")
    if not path.is_file():
        raise ConfigError(
            f"Config not found: {path}. Run 'pycobello init' to create a new site."
        )
    try:
        raw = yaml.safe_load(path.read_text()) or {}
    except yaml.YAMLError as e:
        raise ConfigError(f"Invalid YAML in {path}: {e}") from e
    if not isinstance(raw, dict):
        raise ConfigError(f"Config must be a YAML object (key-value map), got {type(raw).__name__}.")
    try:
        return _settings_from_dict(raw)
    except (TypeError, KeyError) as e:
        raise ConfigError(f"Invalid config in {path}: {e}") from e


def _settings_from_dict(d: dict) -> PyCobelloSettings:
    """Build PyCobelloSettings from a plain dict (no env)."""
    site_d = d.get("site") or {}
    build_d = d.get("build") or {}
    coll_d = d.get("collections") or {}
    plugins_d = d.get("plugins") or {}

    site = SiteSettings(
        title=_str(site_d.get("title"), "My Site"),
        base_url=_str(site_d.get("base_url"), ""),
        author=_str(site_d.get("author"), ""),
    )
    build = BuildSettings(
        content_dir=_str(build_d.get("content_dir"), "content"),
        theme_dir=_str(build_d.get("theme_dir"), "theme"),
        static_dir=_str(build_d.get("static_dir"), "static"),
        output_dir=_str(build_d.get("output_dir"), "dist"),
        clean_urls=_bool(build_d.get("clean_urls"), True),
        ignore=_str_list(build_d.get("ignore")),
    )
    posts_d = coll_d.get("posts") if isinstance(coll_d.get("posts"), dict) else {}
    pages_d = coll_d.get("pages") if isinstance(coll_d.get("pages"), dict) else {}
    collections = CollectionsSettings(
        posts=CollectionConfig(
            path=_str(posts_d.get("path"), "posts"),
            url_prefix=_str(posts_d.get("url_prefix"), "blog"),
            template=_str(posts_d.get("template"), "post.html"),
        ),
        pages=CollectionConfig(
            path=_str(pages_d.get("path"), "pages"),
            url_prefix=_str(pages_d.get("url_prefix"), ""),
            template=_str(pages_d.get("template"), "page.html"),
        ),
    )
    plugins = PluginsSettings(enabled=_str_list(plugins_d.get("enabled")))

    return PyCobelloSettings(site=site, build=build, collections=collections, plugins=plugins)


def _str(v: object, default: str) -> str:
    if v is None:
        return default
    return str(v).strip()


def _bool(v: object, default: bool) -> bool:
    if v is None:
        return default
    if isinstance(v, bool):
        return v
    return str(v).lower() in ("true", "1", "yes")


def _str_list(v: object) -> list[str]:
    if v is None:
        return []
    if isinstance(v, list):
        return [str(x).strip() for x in v]
    return []
