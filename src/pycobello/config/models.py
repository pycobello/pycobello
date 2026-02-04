"""Config models (dataclasses) built from YAML. No pydantic."""

from dataclasses import dataclass, field


@dataclass
class SiteSettings:
    """Site metadata."""

    title: str = "My Site"
    base_url: str = ""
    author: str = ""


@dataclass
class BuildSettings:
    """Paths and build options."""

    content_dir: str = "content"
    theme_dir: str = "theme"
    static_dir: str = "static"
    output_dir: str = "dist"
    clean_urls: bool = True
    ignore: list[str] = field(default_factory=list)


@dataclass
class CollectionConfig:
    """Single collection (posts or pages)."""

    path: str
    url_prefix: str = ""
    template: str = ""


@dataclass
class CollectionsSettings:
    """Posts and pages collection config."""

    posts: CollectionConfig = field(
        default_factory=lambda: CollectionConfig(
            path="posts", url_prefix="blog", template="post.html"
        )
    )
    pages: CollectionConfig = field(
        default_factory=lambda: CollectionConfig(path="pages", url_prefix="", template="page.html")
    )


@dataclass
class PluginsSettings:
    """Plugin enable list."""

    enabled: list[str] = field(default_factory=list)


@dataclass
class PyCobelloSettings:
    """Root config (from pycobello.yml only; no env overrides)."""

    site: SiteSettings = field(default_factory=SiteSettings)
    build: BuildSettings = field(default_factory=BuildSettings)
    collections: CollectionsSettings = field(default_factory=CollectionsSettings)
    plugins: PluginsSettings = field(default_factory=PluginsSettings)
