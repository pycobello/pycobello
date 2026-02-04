"""Public app surface for plugins (stable minimal). Step 10."""

from typing import Any

_app: "PyCobelloApp | None" = None


class PyCobelloApp:
    """Plugin API: register hooks, add Jinja filters/globals."""

    def __init__(self) -> None:
        self._jinja_filters: dict[str, Any] = {}
        self._jinja_globals: dict[str, Any] = {}

    def add_filter(self, name: str, fn: Any) -> None:
        self._jinja_filters[name] = fn

    def add_global(self, name: str, value: Any) -> None:
        self._jinja_globals[name] = value

    def register_hook(self, hook_name: str, handler: Any) -> None:
        from pycobello.plugins.hooks import register
        register(hook_name, handler)

    @property
    def jinja_filters(self) -> dict[str, Any]:
        return self._jinja_filters

    @property
    def jinja_globals(self) -> dict[str, Any]:
        return self._jinja_globals


def get_app() -> PyCobelloApp:
    global _app
    if _app is None:
        _app = PyCobelloApp()
    return _app
