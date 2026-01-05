from __future__ import annotations

from datetime import datetime, timezone

from resilio.io.artifacts import ArtifactStore
from resilio.models.state import ArtifactPaths, ResilioState, Snapshot, SnapshotInput


class StateSnapshotter:
    """Capture and persist failure-time context."""

    def __init__(self, store: ArtifactStore) -> None:
        self._store = store

    def capture(self, state: ResilioState) -> ResilioState:
        """Persist artifacts and return updated state."""
        run_id = state.get("run_id") or self._new_run_id()
        run_dir = self._store.prepare_run_dir(run_id)
        snapshot_input = state.get("snapshot_input") or SnapshotInput()

        dom_path = None
        if snapshot_input.dom_html is not None:
            dom_path = str(
                self._store.write_text(run_dir, "dom.html", snapshot_input.dom_html)
            )

        screenshot_path = None
        if snapshot_input.screenshot_png is not None:
            screenshot_path = str(
                self._store.write_bytes(
                    run_dir, "screenshot.png", snapshot_input.screenshot_png
                )
            )

        console_path = None
        if snapshot_input.console_log is not None:
            console_path = str(
                self._store.write_text(
                    run_dir, "console.log", snapshot_input.console_log
                )
            )

        har_path = None
        if snapshot_input.har_json is not None:
            har_path = str(
                self._store.write_text(run_dir, "network.har", snapshot_input.har_json)
            )

        artifacts = ArtifactPaths(
            dom_html=dom_path,
            screenshot_png=screenshot_path,
            console_log=console_path,
            har_json=har_path,
        )

        index_payload = {
            "run_id": run_id,
            "dom_html": dom_path or "",
            "screenshot_png": screenshot_path or "",
            "console_log": console_path or "",
            "har_json": har_path or "",
        }
        index_path = str(self._store.write_index(run_dir, index_payload))

        artifacts = ArtifactPaths(
            dom_html=dom_path,
            screenshot_png=screenshot_path,
            console_log=console_path,
            har_json=har_path,
            index_json=index_path,
        )

        snapshot = Snapshot(
            run_id=run_id,
            captured_at=self._timestamp(),
            last_action=state.get("last_action"),
            error_type=state.get("error_type"),
            error_message=state.get("error_message"),
            artifacts=artifacts,
        )

        return {
            "run_id": run_id,
            "artifacts": artifacts,
            "snapshot": snapshot,
        }

    def _new_run_id(self) -> str:
        return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")

    def _timestamp(self) -> str:
        return datetime.now(timezone.utc).isoformat()
