"""Check command implementation."""


def run_check(project_root: str) -> None:
    """Run diagnostics. Implemented in Step 9."""
    from pycobello.diagnostics.checks import run_checks

    run_checks(project_root)
