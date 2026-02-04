"""Plugin loading and hooks."""

from pycobello.plugins.hooks import get_hooks
from pycobello.plugins.manager import load_plugins

__all__ = ["load_plugins", "get_hooks"]
