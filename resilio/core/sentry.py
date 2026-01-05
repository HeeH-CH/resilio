from __future__ import annotations

from typing import Any, Protocol

from resilio.models.state import ResilioState, SnapshotInput


class GraphRunner(Protocol):
    """Callable interface for compiled LangGraph workflows."""

    def invoke(self, state: ResilioState) -> ResilioState:
        """Invoke the workflow with the provided state."""
        ...


class ResilioAction(Protocol):
    """Executable action interface for the runtime sentry."""

    def run(self) -> Any:
        """Run the action."""
        ...


class RuntimeSentry:
    """Run actions and trigger the snapshot workflow on failure."""

    def __init__(self, workflow: GraphRunner) -> None:
        self._workflow = workflow

    def run_action(
        self,
        action: ResilioAction,
        last_action: str,
        snapshot_input: SnapshotInput | None = None,
    ) -> ResilioState | None:
        """Execute an action and capture artifacts on error."""
        try:
            action.run()
            return None
        except Exception as exc:
            state: ResilioState = {
                "last_action": last_action,
                "error_type": type(exc).__name__,
                "error_message": str(exc),
                "snapshot_input": snapshot_input or SnapshotInput(),
            }
            return self._workflow.invoke(state)
