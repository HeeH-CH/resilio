# Resilio Implementation Plan

## Goals
- Capture live runtime state when automation fails (DOM, screenshot, console, HAR).
- Generate minimal, safe patches aligned to observed environment changes.
- Enforce human approval via PR workflow before deployment.

## Global Constraints
- Use class-based design for all core components.
- Manage dependencies and environment with `uv` and `uv.lock`.
- Inject SSL truststore at the app entrypoint:
  - `import truststore`
  - `truststore.inject_into_ssl()`
- Use LangGraph v1 APIs for the workflow graph.
- Write code comments and in-code explanations in English.

## Architecture Overview
- Runtime Sentry: wraps actions, catches failures, hands off to snapshotter.
- State Snapshotter: persists HTML, screenshots, console logs, and HAR traces.
- Context Distiller: reduces raw DOM to a compact, LLM-friendly tree.
- Root Cause Analyzer: rule-based prefilter + LLM analysis.
- Patch Architect: generates PatchSpec with minimal change principle.
- Safety Gatekeeper: validates selectors and syntax before execution.
- Sandbox Validator: replays failure steps and opens PR on success.

## Phased Roadmap
### Phase 0: Observability
- Implement `RuntimeSentry` and `StateSnapshotter`.
- Define `Snapshot` schema and artifact storage layout.
- Provide a basic artifact viewer or index.

### Phase 1: Assisted Healing
- Implement `ContextDistiller`, `RootCauseAnalyzer`, and `PatchArchitect`.
- Define strict `PatchSpec` schema for output validation.
- Send patch suggestions to a notification channel (e.g., Teams).

### Phase 2: Autonomous Recovery
- Implement `SafetyGatekeeper` and `SandboxValidator`.
- Add replay execution and automatic PR creation.
- Enforce human approval before merge.

### Phase 3: Collective Intelligence
- Add vector DB-backed knowledge base of prior fixes.
- Retrieve similar past patches before generating new ones.

## LangGraph v1 Workflow
- Nodes: Capture -> Distill -> Analyze -> Patch -> Verify -> Deliver
- Each node implemented as a class with a `run()` method.
- Graph orchestrates state flow and persists artifacts.

## Repository Layout (Planned)
- `src/resilio/`
  - `core/` (sentry, snapshotter, distiller, analyzer, architect, gatekeeper, validator)
  - `graph/` (LangGraph v1 workflow)
  - `models/` (Snapshot, PatchSpec, VerificationReport)
  - `io/` (artifact storage, log formatting)
- `configs/`
- `tests/`

## Quality and Safety
- Selector existence checks against snapshot DOM.
- AST/lint checks for generated patches.
- Replay-based verification before PR creation.

## Definition of Done (Phase 0)
- Failure captures DOM, screenshot, console, and HAR.
- Artifacts stored with deterministic naming.
- Basic viewer/index lists captured artifacts.
