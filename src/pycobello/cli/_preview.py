"""Preview command implementation."""


def run_preview(project_root: str, port: int = 8000, watch: bool = False) -> None:
    """Serve dist/ and optionally watch. Implemented in Step 8."""
    from pycobello.preview import serve_preview

    serve_preview(project_root, port=port, watch=watch)
