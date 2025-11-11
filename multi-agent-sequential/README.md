# Multi-Agent Sequential Sample — BlogPipeline

This sample demonstrates a sequential multi-agent pipeline using `SequentialAgent`. The pipeline composes three focused agents (Outline, Writer, Editor) that run in order and pass structured outputs between them to produce a polished blog post. This approach contrasts with the orchestrator (LLM-as-coordinator) pattern in `multi-agent/` and is particularly useful when you want deterministic stepwise processing and clear data flow.

## What this sample demonstrates

- Using `SequentialAgent` to run multiple agents in a fixed sequence
- Each sub-agent has a single responsibility and uses `output_key` to expose results
- How earlier agent outputs (e.g., `blog_outline`) are injected into later agents via placeholders like `{blog_outline}`
- When sequential pipelines are preferable to an LLM coordinator

## Files

- `agent.py` — Defines `root_agent` as a `SequentialAgent` named `BlogPipeline` and registers sub-agents
- `sub_agents/outline_agent/agent.py` — `OutlineAgent` generates a structured outline and outputs `blog_outline`
- `sub_agents/writer_agent/agent.py` — `WriterAgent` consumes `blog_outline` and outputs `blog_draft`
- `sub_agents/editor_agent/agent.py` — `EditorAgent` consumes `blog_draft` and outputs `final_blog`

## Sequential pipeline example (from `agent.py`)

```python
from google.adk.agents import SequentialAgent

from .sub_agents.outline_agent.agent import outline_agent
from .sub_agents.writer_agent.agent import writer_agent
from .sub_agents.editor_agent.agent import editor_agent

root_agent = SequentialAgent(
    name="BlogPipeline",
    sub_agents=[outline_agent, writer_agent, editor_agent],
)
```

## Sub-agent roles

- OutlineAgent: Produces a catchy headline, intro hook, sectioned outline (3–5 sections) and stores it as `blog_outline`.
- WriterAgent: Strictly follows `{blog_outline}` to produce a 200–300 word draft saved as `blog_draft`.
- EditorAgent: Polishes `{blog_draft}` for grammar, flow, and clarity and outputs `final_blog`.

## Advantages of SequentialAgent over an LLM orchestrator

- Predictable control flow: Each step runs in order and cannot skip or reorder steps unintentionally.
- Easier debugging: Intermediate outputs are explicit (`output_key`) making it simple to inspect where issues occur.
- Clear responsibilities: Each agent is single-purpose and easier to test and maintain.
- Better for pipelines with strict data dependencies (e.g., outline -> draft -> edit).

When to prefer an LLM orchestrator (the `multi-agent` example):
- You want a flexible planner that can dynamically decide which tools or sub-agents to call.
- The workflow may be conditional or require branching logic determined at runtime.

## Quick start / run locally

This repository uses `uv` as the package manager. From the project root:

```bash
make install
```

Start the development API server:

```bash
make dev
```

Launch the web playground (in another terminal):

```bash
make playground
```

Run an in-memory sequential pipeline example (create `example_sequential_run.py` and run with `uv run python example_sequential_run.py`):

```python
# example_sequential_run.py
from multi_agent_sequential import root_agent
from google.adk.runners import InMemoryRunner

runner = InMemoryRunner(root_agent)
query = "Write a blog post about sustainable urban gardening."
resp = runner.run(query)
print(resp)
```

Notes:
- Ensure Google credentials are available for the ADK and any external tools.
- Sequential pipelines surface intermediate state keys (e.g., `blog_draft`) which you can log or inspect for testing.

## Tips

- Keep each agent focused on one task and use descriptive `output_key` names.
- Use strict instruction templates in middle-step agents (like the writer) to ensure consistent drafts.
- Add small unit tests for each agent by feeding example inputs and asserting expected `output_key` values.

## Troubleshooting

- If the pipeline stops or produces unexpected content, inspect the outputs after each step (look for `blog_outline`, `blog_draft`).
- If models return low-quality text, try tightening instructions or changing model settings (temperature, max tokens) if available.

---

This sequential sample is an easy-to-understand pattern for deterministic pipelines where each step must complete before the next begins.