"""New post/page command implementation."""


def run_new(kind: str, title: str, project_root: str) -> None:
    """Create new post or page. Implemented with scaffold."""
    from pycobello.scaffold import create_new

    create_new(kind, title, project_root)
