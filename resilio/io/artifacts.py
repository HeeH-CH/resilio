from __future__ import annotations

import json
from pathlib import Path
from typing import Mapping


class ArtifactStore:
    """Persist snapshot artifacts to disk."""

    def __init__(self, root: Path) -> None:
        self._root = root
        self._root.mkdir(parents=True, exist_ok=True)

    def prepare_run_dir(self, run_id: str) -> Path:
        """Create the run directory if missing."""
        run_dir = self._root / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        return run_dir

    def write_text(self, run_dir: Path, name: str, content: str) -> Path:
        """Write a UTF-8 text artifact."""
        path = run_dir / name
        path.write_text(content, encoding="utf-8")
        return path

    def write_bytes(self, run_dir: Path, name: str, content: bytes) -> Path:
        """Write a binary artifact."""
        path = run_dir / name
        path.write_bytes(content)
        return path

    def write_index(self, run_dir: Path, payload: Mapping[str, str]) -> Path:
        """Write a JSON index for the run artifacts."""
        path = run_dir / "index.json"
        path.write_text(
            json.dumps(payload, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        return path
