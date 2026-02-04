"""Structured logging helpers."""

import logging

LOG = logging.getLogger("pycobello")


def configure(verbose: bool = False) -> None:
    """Configure pycobello logger. Call once from CLI."""
    level = logging.DEBUG if verbose else logging.INFO
    LOG.setLevel(level)
    if not LOG.handlers:
        h = logging.StreamHandler()
        h.setLevel(level)
        LOG.addHandler(h)
