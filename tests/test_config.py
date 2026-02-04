"""Config load success and failure."""

from pathlib import Path

import pytest

from pycobello.config.load import load_config
from pycobello.errors import ConfigError


def test_load_config_success(project_root: Path) -> None:
    """Load config from init-created pycobello.yml."""
    config = load_config(str(project_root))
    assert config.site.title == "My Site"
    assert config.build.content_dir == "content"
    assert config.build.output_dir == "dist"
    assert config.collections.posts.url_prefix == "blog"
    assert config.collections.pages.template == "page.html"


def test_load_config_missing_file(tmp_path: Path) -> None:
    """Missing config raises ConfigError with helpful message."""
    with pytest.raises(ConfigError) as exc_info:
        load_config(str(tmp_path))
    assert "pycobello init" in str(exc_info.value)


def test_load_config_invalid_yaml(project_root: Path) -> None:
    """Invalid YAML raises ConfigError."""
    cfg = project_root / "pycobello.yml"
    cfg.write_text("site:\n  title: [unclosed")
    with pytest.raises(ConfigError) as exc_info:
        load_config(str(project_root))
    assert "Invalid YAML" in str(exc_info.value) or "config" in str(exc_info.value).lower()
