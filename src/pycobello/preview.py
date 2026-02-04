"""Preview server and optional watch. Step 8."""

import http.server
import socketserver
import threading
from pathlib import Path


def serve_preview(
    project_root: str,
    port: int = 8000,
    watch: bool = False,
) -> None:
    """Serve dist/ with stdlib http.server; optionally watch and rebuild."""
    root = Path(project_root).resolve()
    dist = root / "dist"
    if not dist.is_dir():
        print("Run 'pycobello build' first.")
        raise SystemExit(1)

    if watch:
        try:
            from watchfiles import watch
        except ImportError:
            print("Install watch support: pip install pycobello[watch]")
            raise SystemExit(1) from None
        _run_with_watch(root, dist, port)
    else:
        _serve(dist, port)


def _serve(dist: Path, port: int) -> None:
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=str(dist), **k)

    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"Serving {dist} at http://127.0.0.1:{port}/")
        httpd.serve_forever()


def _run_with_watch(root: Path, dist: Path, port: int) -> None:
    from watchfiles import watch

    from pycobello.build.pipeline import run_pipeline
    from pycobello.config.load import load_config

    def rebuild() -> None:
        try:
            config = load_config(str(root))
            result = run_pipeline(config, project_root=root, clean=False)
            print(f"Build: {len(result.written)} written, {len(result.skipped)} skipped")
        except Exception as e:
            print(f"Build error: {e}")

    rebuild()
    server_thread = threading.Thread(
        target=_serve,
        args=(dist, port),
        daemon=True,
    )
    server_thread.start()
    watch_dirs = [root / "content", root / "theme", root / "static", root]
    for changes in watch(*watch_dirs):
        print(f"Change: {changes}")
        rebuild()
