"""Load entry points and call register(app). Step 10."""

import importlib.metadata

from pycobello.api.app import get_app


def load_plugins(enabled: list[str] | None = None) -> None:
    """Load pycobello.plugins entry points and call register(app)."""
    app = get_app()
    for ep in importlib.metadata.entry_points(group="pycobello.plugins"):
        if enabled is not None and ep.name not in enabled:
            continue
        plugin = ep.load()
        if hasattr(plugin, "register"):
            plugin.register(app)
