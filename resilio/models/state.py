from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, TypedDict


@dataclass(frozen=True)
class SnapshotInput:
    """Raw inputs captured at failure time."""

    dom_html: Optional[str] = None
    screenshot_png: Optional[bytes] = None
    console_log: Optional[str] = None
    har_json: Optional[str] = None


@dataclass(frozen=True)
class ArtifactPaths:
    """Filesystem paths for persisted artifacts."""

    dom_html: Optional[str] = None
    screenshot_png: Optional[str] = None
    console_log: Optional[str] = None
    har_json: Optional[str] = None
    index_json: Optional[str] = None


@dataclass(frozen=True)
class Snapshot:
    """Metadata describing a captured snapshot."""

    run_id: str
    captured_at: str
    last_action: Optional[str]
    error_type: Optional[str]
    error_message: Optional[str]
    artifacts: ArtifactPaths


class ResilioState(TypedDict, total=False):
    """LangGraph state container."""

    run_id: str
    last_action: str
    error_type: str
    error_message: str
    snapshot_input: SnapshotInput
    artifacts: ArtifactPaths
    snapshot: Snapshot
