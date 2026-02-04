"""Plugin hooks and app API."""

from pycobello.api.app import PyCobelloApp
from pycobello.plugins.hooks import emit, register


def test_app_add_filter_and_global() -> None:
    """Plugins can register Jinja filters and globals."""
    app = PyCobelloApp()
    app.add_filter("upper", str.upper)
    app.add_global("foo", "bar")
    assert app.jinja_filters["upper"] is str.upper
    assert app.jinja_globals["foo"] == "bar"


def test_hooks_emit_calls_registered_handlers() -> None:
    """Registering a hook and emitting calls the handler."""
    seen: list[str] = []

    def handler(msg: str) -> None:
        seen.append(msg)

    register("config_loaded", handler)
    try:
        emit("config_loaded", msg="hello")
        assert seen == ["hello"]
    finally:
        # Reset so we don't affect other tests
        from pycobello.plugins.hooks import _registry

        _registry["config_loaded"] = [h for h in _registry["config_loaded"] if h != handler]
