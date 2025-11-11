# Multi-Agent Sample — ResearchCoordinator

This sample demonstrates a multi-agent workflow: a root coordinator agent orchestrates two specialized sub-agents to answer research-style queries. It shows how to wrap sub-agents as tools (using `AgentTool`), pass intermediate outputs between agents, and structure instructions for a predictable pipeline.

> Workflow Pattern: Use `LLM Orchestrator` (Agent with other agents as tool)

## What this sample demonstrates

- A root `Agent` acting as a coordinator for a multi-step workflow
- Wrapping sub-agents with `AgentTool` so the root agent can call them like tools
- Passing intermediate outputs via `output_key` (session state keys)
- A producer/consumer pattern: `ResearchAgent` produces findings, `SummarizerAgent` consumes them and produces a final summary

## Files

- `agent.py` — Root coordinator agent (`root_agent`) that orchestrates the workflow
- `sub_agents/research_agent/agent.py` — `ResearchAgent` which uses `google_search` to collect findings
- `sub_agents/summarizer_agent/agent.py` — `SummarizerAgent` which summarizes research findings into a concise bulleted list

## Root agent example (from `agent.py`)

```python
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import AgentTool

from config import retry_config
from .sub_agents.research_agent import research_agent
from .sub_agents.summarizer_agent import summarizer_agent

# Root Coordinator: Orchestrates the workflow by calling the sub-agents as tools.
root_agent = Agent(
    name="ResearchCoordinator",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    instruction="""You are a research coordinator. Your goal is to answer the user's query by orchestrating a workflow.
    1. First, you MUST call the `ResearchAgent` tool to find relevant information on the topic provided by the user.
    2. Next, after receiving the research findings, you MUST call the `SummarizerAgent` tool to create a concise summary.
    3. Finally, present the final summary clearly to the user as your response.""",
    tools=[
        AgentTool(research_agent), 
        AgentTool(summarizer_agent)
    ],
)
```

## Sub-agent details

### ResearchAgent
- Purpose: Use `google_search` to find 2-3 relevant pieces of information and return findings with citations.
- Exposes its output as `research_findings` in session state (via `output_key`).

### SummarizerAgent
- Purpose: Read `{research_findings}` and return a short bulleted summary (3–5 points).
- Exposes its output as `final_summary` in session state (via `output_key`).

## How the orchestration works

1. The user sends a query to the `ResearchCoordinator` (root agent).
2. The coordinator follows its instruction: first call `ResearchAgent` as a tool.
3. `ResearchAgent` runs, performs searches (via `google_search`), and stores results under `research_findings`.
4. The coordinator receives `research_findings` and then calls `SummarizerAgent` (passing the findings into its instruction template).
5. `SummarizerAgent` returns `final_summary` which the coordinator then returns to the user.

This pattern makes it easy to decompose complex tasks into smaller, testable agents.

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

Run a small in-memory orchestration example (create `example_multi_run.py` and run with `uv run python example_multi_run.py`):

```python
# example_multi_run.py
from multi_agent import root_agent
from google.adk.runners import InMemoryRunner

runner = InMemoryRunner(root_agent)
query = "Summarize recent breakthroughs in battery technology."
resp = runner.run(query)
print(resp)
```

Notes:
- To obtain your `GOOGLE_API_KEY` go to [AI Studio](https://aistudio.google.com/api-keys) to create one

## Tips

- Keep sub-agents focused and single-purpose — this improves reuse and reliability.
- Use `output_key` to make the flow explicit and avoid unclear implicit state.
- Make coordinator instructions prescriptive (explicit step-by-step) to ensure consistent tool usage.

## Troubleshooting

- If the `ResearchAgent` cannot call `google_search`, verify network access and credentials.
- If outputs are missing, check `output_key` names and ensure the coordinator references the same keys in its instruction template.

---

This multi-agent sample is a starting point — use it to prototype agent pipelines and larger orchestration patterns.
