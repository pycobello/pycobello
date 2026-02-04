"""PyCobello — a blazing fast, dependency-light static site generator."""

__version__ = "0.1.0"

from pycobello.config.load import load_config

__all__ = ["__version__", "load_config"]
