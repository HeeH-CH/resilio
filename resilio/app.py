from __future__ import annotations

from resilio.config import ResilioConfig
from resilio.core.sentry import RuntimeSentry
from resilio.core.snapshotter import StateSnapshotter
from resilio.graph.nodes import ResilioNodes
from resilio.graph.workflow import ResilioWorkflow
from resilio.io.artifacts import ArtifactStore


class ResilioApp:
    """Application bootstrap for Phase 0 observability."""

    def __init__(self, config: ResilioConfig | None = None) -> None:
        self._config = config or ResilioConfig.default()
        self._store = ArtifactStore(self._config.artifact_root)
        self._snapshotter = StateSnapshotter(self._store)
        self._nodes = ResilioNodes(self._snapshotter)
        self._workflow = ResilioWorkflow(self._nodes)
        self._graph = self._workflow.build()
        self._sentry = RuntimeSentry(self._graph)

    def run(self) -> None:
        """Initialize components and wait for external integration."""
        return None

    @property
    def sentry(self) -> RuntimeSentry:
        """Expose the runtime sentry for integrations."""
        return self._sentry
