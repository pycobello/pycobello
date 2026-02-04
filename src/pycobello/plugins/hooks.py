"""Hook registry and event dispatch. Step 10."""

from collections.abc import Callable

HOOK_NAMES = (
    "config_loaded",
    "sources_discovered",
    "item_parsed",
    "pre_render",
    "post_render",
    "post_build",
)

_registry: dict[str, list[Callable]] = {name: [] for name in HOOK_NAMES}


def register(hook_name: str, handler: Callable) -> None:
    """Register a handler for a hook."""
    if hook_name not in _registry:
        _registry[hook_name] = []
    _registry[hook_name].append(handler)


def emit(hook_name: str, **kwargs) -> None:
    """Call all handlers for a hook."""
    for fn in _registry.get(hook_name, []):
        fn(**kwargs)


def get_hooks() -> dict[str, list[Callable]]:
    """Return registry (for tests)."""
    return _registry
