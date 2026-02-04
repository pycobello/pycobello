"""Init command implementation."""


def run_init(project_root: str) -> None:
    """Create scaffold. Implemented in Step 3."""
    from pycobello.scaffold import create_scaffold

    create_scaffold(project_root)
