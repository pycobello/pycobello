"""Pytest fixtures: tmp project dir with init scaffold."""

from pathlib import Path

import pytest

from pycobello.scaffold import create_scaffold


@pytest.fixture
def project_root(tmp_path: Path) -> Path:
    """Create a minimal pycobello project and return its root."""
    create_scaffold(str(tmp_path))
    return tmp_path
