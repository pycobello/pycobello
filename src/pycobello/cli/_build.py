"""Build command implementation."""


def run_build(project_root: str, clean: bool = False) -> None:
    """Run build pipeline. Implemented in Steps 5–7."""
    from pycobello.build.pipeline import run_pipeline
    from pycobello.config.load import load_config
    from pycobello.errors import ConfigError

    try:
        config = load_config(project_root)
    except ConfigError as e:
        raise SystemExit(str(e)) from e
    result = run_pipeline(config, project_root=project_root, clean=clean)
    if result.errors:
        for err in result.errors:
            print(err, file=__import__("sys").stderr)
        raise SystemExit(1)
    print(f"Build done: {len(result.written)} written, {len(result.skipped)} skipped.")
