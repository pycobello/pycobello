"""Custom exceptions with friendly messages."""


class PyCobelloError(Exception):
    """Base exception for pycobello."""

    pass


class ConfigError(PyCobelloError):
    """Configuration file missing or invalid."""

    pass


class FrontMatterError(PyCobelloError):
    """Invalid YAML front matter."""

    pass


class BuildError(PyCobelloError):
    """Build failed (e.g. missing template)."""

    pass
