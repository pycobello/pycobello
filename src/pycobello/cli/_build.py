"""Build command implementation."""


def run_build(project_root: str, clean: bool = False) -> None:
    """Run build pipeline. Implemented in Steps 5–7."""
    from pycobello.config.load import load_config
    from pycobello.build.pipeline import run_pipeline
    from pycobello.errors import ConfigError

    try:
        config = load_config(project_root)
    except ConfigError as e:
        raise SystemExit(str(e)) from e
    result = run_pipeline(config, project_root=project_root, clean=clean)
    if result.errors:
        raise SystemExit(1)
