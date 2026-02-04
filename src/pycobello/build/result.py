"""BuildResult dataclass."""

from dataclasses import dataclass


@dataclass
class BuildResult:
    """Result of a build run."""

    written: list[str]
    skipped: list[str]
    errors: list[str]
