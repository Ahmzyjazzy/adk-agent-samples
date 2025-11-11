# Basic Agent — "helpful_assistant"

This sample shows how to write your first ADK agent and attach the `google_search` tool so the
agent can look up real-time information. It demonstrates a minimal, well-documented example you
can copy and extend when building your own agents.

## What this sample demonstrates

- Creating an `Agent` instance with the Gemini LLM
- Adding robust HTTP retry options for transient failures
- Enabling the `google_search` tool so the agent can query the web
- Exporting the agent for easy import and quick experiments

## Files

- `agent.py` — Agent configuration (exports `root_agent`)
- `__init__.py` — Convenience export (`from .agent import root_agent`)
- `config.py` — Retry configuration used by the agent

## Agent example (from `agent.py`)

```python
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search

from config import retry_config

root_agent = Agent(
		name="helpful_assistant",
		model=Gemini(
				model="gemini-2.5-flash-lite",
				retry_options=retry_config
		),
		description="A simple agent that can answer general questions.",
		instruction="You are a helpful assistant. Use Google Search for current info or if unsure.",
		tools=[google_search],
)
```

## How the `google_search` tool is used

The `google_search` tool is passed in the agent's `tools` list. When the model decides it needs
current, external information it can call that tool. The ADK handles tool invocation and response
passing back to the model so you only need to declare the tool and let the agent use it.

Typical usage patterns:

- The agent uses the tool automatically when the instruction or model indicates a web lookup is needed.
- You can influence tool use by providing clear instructions in the `instruction` field (as shown above).

## Quick start / run locally

This repository uses `uv` as the package manager; install dependencies first (from project root):

```bash
make install
```

Try the agent interactively using the in-memory runner (example):

```python
# example_run.py (run with `uv run python example_run.py`)
from basic_agent import root_agent
from google.adk.runners import InMemoryRunner

runner = InMemoryRunner(root_agent)
resp = runner.run("Who won the 2024 Olympics men's 100m?")
print(resp)
```

Notes:
- To obtain your `GOOGLE_API_KEY` go to [AI Studio](https://aistudio.google.com/api-keys) to create one

## Tips for extending

- Add more tools to the `tools` list to increase the agent's capabilities (e.g., calendar, code-execution).
- Tweak `retry_config` in `config.py` if you need a different retry policy.
- Keep `instruction` clear and scoped to your assistant's purpose to improve reliability.

## Troubleshooting

- If the agent can't access the web tool, verify your network and Google API credentials.
- If you hit rate limits, consider adjusting `retry_config` or lowering request frequency.

---

This basic sample is intentionally small — copy and modify it as the starting point for your
own ADK agents.
