# Resilio

Self-healing automation pipeline skeleton for Phase 0 observability.

## What is this
Resilio captures live runtime state on automation failures (DOM, screenshot, console, HAR)
and prepares the workflow foundation for later analysis and patching.

## Features (Phase 0)
- Class-based runtime components for capturing failure context.
- LangGraph v1 workflow with node stubs.
- Artifact storage with deterministic run folders and index metadata.
- SSL truststore injection at the entrypoint.

## Requirements
- Python 3.12+
- `uv` for environment and dependency management

## Setup
```bash
uv venv
uv sync
```

## Run
```bash
uv run python main.py
```

## Project Layout
```text
resilio/
  app.py                Application bootstrap
  config.py             Runtime configuration
  core/
    sentry.py           Runtime sentry and action protocol
    snapshotter.py      Snapshot capture and persistence
  graph/
    nodes.py            LangGraph node implementations
    workflow.py         LangGraph v1 workflow builder
  io/
    artifacts.py        Artifact storage helpers
  models/
    state.py            State and snapshot models
```

## Notes
- The Phase 0 workflow only captures artifacts.
- Phase 1+ analysis and patching nodes are placeholders.
