from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ResilioConfig:
    """Runtime configuration for the Resilio app."""

    artifact_root: Path

    @classmethod
    def default(cls) -> "ResilioConfig":
        """Return the default configuration."""
        return cls(artifact_root=Path.cwd() / "artifacts")
