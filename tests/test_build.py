"""Build pipeline and incremental write-avoidance."""

from pathlib import Path

from pycobello.build.pipeline import run_pipeline
from pycobello.config.load import load_config


def test_build_produces_output(project_root: Path) -> None:
    """After init, build produces dist/index.html and post/page outputs."""
    config = load_config(str(project_root))
    result = run_pipeline(config, project_root=project_root, clean=True)
    assert not result.errors
    dist = project_root / "dist"
    assert (dist / "index.html").exists()
    assert len(result.written) >= 1
    # Blog and about (clean URLs)
    assert (dist / "blog").is_dir() or (dist / "about").is_dir()


def test_incremental_build_skips_unchanged(project_root: Path) -> None:
    """Second build with no changes writes nothing (all skipped)."""
    config = load_config(str(project_root))
    result1 = run_pipeline(config, project_root=project_root, clean=True)
    assert not result1.errors
    result2 = run_pipeline(config, project_root=project_root, clean=False)
    assert not result2.errors
    # Second run should have nothing written (or only index if we don't cache it)
    assert len(result2.written) == 0, f"Expected no writes on second run, got {result2.written}"
