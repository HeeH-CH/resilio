from __future__ import annotations

from langgraph.graph import END, StateGraph

from resilio.graph.nodes import ResilioNodes
from resilio.models.state import ResilioState


class ResilioWorkflow:
    """Build the LangGraph v1 workflow."""

    def __init__(self, nodes: ResilioNodes) -> None:
        self._nodes = nodes

    def build(self):
        """Compile and return the workflow graph."""
        graph = StateGraph(ResilioState)
        graph.add_node("capture", self._nodes.capture)
        graph.add_node("distill", self._nodes.distill)
        graph.add_node("analyze", self._nodes.analyze)
        graph.add_node("patch", self._nodes.patch)
        graph.add_node("verify", self._nodes.verify)
        graph.add_node("deliver", self._nodes.deliver)

        graph.set_entry_point("capture")
        graph.add_edge("capture", "distill")
        graph.add_edge("distill", "analyze")
        graph.add_edge("analyze", "patch")
        graph.add_edge("patch", "verify")
        graph.add_edge("verify", "deliver")
        graph.add_edge("deliver", END)

        return graph.compile()
