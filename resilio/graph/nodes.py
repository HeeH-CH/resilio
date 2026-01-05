from __future__ import annotations

from resilio.core.snapshotter import StateSnapshotter
from resilio.models.state import ResilioState


class ResilioNodes:
    """Node implementations for the LangGraph workflow."""

    def __init__(self, snapshotter: StateSnapshotter) -> None:
        self._snapshotter = snapshotter

    def capture(self, state: ResilioState) -> ResilioState:
        """Capture failure-time artifacts."""
        return self._snapshotter.capture(state)

    def distill(self, state: ResilioState) -> ResilioState:
        """Placeholder for DOM distillation."""
        return state

    def analyze(self, state: ResilioState) -> ResilioState:
        """Placeholder for root cause analysis."""
        return state

    def patch(self, state: ResilioState) -> ResilioState:
        """Placeholder for patch generation."""
        return state

    def verify(self, state: ResilioState) -> ResilioState:
        """Placeholder for safety checks."""
        return state

    def deliver(self, state: ResilioState) -> ResilioState:
        """Placeholder for delivery steps."""
        return state
