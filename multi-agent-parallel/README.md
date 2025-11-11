# Multi-Agent Parallel Sample — ParallelResearchTeam

This sample demonstrates a hybrid workflow that runs independent research agents in parallel and then synthesizes their outputs with an aggregator agent. Use this pattern when you have independent tasks that can run concurrently (faster throughput) and a final step that needs to combine results.

## What this sample demonstrates

- Running independent agents in parallel using `ParallelAgent` (concurrent research)
- Using a `SequentialAgent` at the top level to first run the parallel stage and then run the `AggregatorAgent` to synthesize results
- Each parallel sub-agent uses `google_search` to produce concise research outputs and exposes them via `output_key` (e.g., `tech_research`)
- The aggregator receives all parallel outputs via placeholders and returns a unified `executive_summary`

## Files

- `agent.py` — Constructs `parallel_research_team` (a `ParallelAgent`) and `root_agent` (a `SequentialAgent`) that runs the parallel team then the aggregator
- `sub_agents/tech_researcher/agent.py` — `TechResearcher` (outputs `tech_research`)
- `sub_agents/health_researcher/agent.py` — `HealthResearcher` (outputs `health_research`)
- `sub_agents/finance_researcher/agent.py` — `FinanceResearcher` (outputs `finance_research`)
- `sub_agents/aggregator_agent/agent.py` — `AggregatorAgent` (consumes the three outputs and produces `executive_summary`)

## Example wiring (from `agent.py`)

```python
from google.adk.agents import SequentialAgent, ParallelAgent

from .sub_agents.tech_researcher.agent import tech_researcher
from .sub_agents.health_researcher.agent import health_researcher
from .sub_agents.finance_researcher.agent import finance_researcher
from .sub_agents.aggregator_agent.agent import aggregator_agent

# The ParallelAgent runs all its sub-agents simultaneously.
parallel_research_team = ParallelAgent(
    name="ParallelResearchTeam",
    sub_agents=[tech_researcher, health_researcher, finance_researcher],
)

# This SequentialAgent defines the high-level workflow: run the parallel team first, then run the aggregator.
root_agent = SequentialAgent(
    name="ResearchSystem",
    sub_agents=[parallel_research_team, aggregator_agent],
)
```

## How the flow works

1. The `ParallelAgent` launches `TechResearcher`, `HealthResearcher`, and `FinanceResearcher` concurrently. Each agent performs independent web searches and writes its result to the session state using its `output_key`.
2. When all parallel agents finish, the `SequentialAgent` continues and calls `AggregatorAgent`.
3. `AggregatorAgent` receives the three outputs via placeholders (`{tech_research}`, `{health_research}`, `{finance_research}`) and synthesizes them into a single `executive_summary`.

This pattern is ideal when the sub-tasks are independent and can be parallelized to reduce wall-clock time.

## Advantages of parallel agents

- Faster completion for independent tasks (wall-clock speedups)
- Clear separation of concerns across focused researcher agents
- Aggregator can combine diverse perspectives into a coherent summary

When NOT to use parallel agents:
- When tasks must run in a strict order with dependencies between them (use `SequentialAgent` instead)
- When only a single agent is needed — parallel adds complexity

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

Run a simple in-memory example (create `example_parallel_run.py` and run with `uv run python example_parallel_run.py`):

```python
# example_parallel_run.py
from multi_agent_parallel import root_agent
from google.adk.runners import InMemoryRunner

runner = InMemoryRunner(root_agent)
query = "Provide quick research on AI, medical, and fintech trends for an executive briefing."
resp = runner.run(query)
print(resp)
```

Notes:
- To obtain your `GOOGLE_API_KEY` go to [AI Studio](https://aistudio.google.com/api-keys) to create one

## Tips

- Keep each parallel researcher focused and concise (e.g., 100 words) to make aggregation easier.
- Use distinct `output_key` names and clear instruction templates so the aggregator can reliably inject each output.
- Consider adding timeouts or max concurrency controls if running many parallel agents in production.

## Troubleshooting

- If some parallel agents fail: check logs for individual agent errors and API rate limits.
- If the aggregator receives empty outputs, verify each researcher's `output_key` and ensure they successfully completed.
- If you hit concurrent API limits, reduce concurrency, increase retries, or contact your API provider.

---

This parallel sample demonstrates a practical pattern for concurrent research and synthesis. Use it as a template for building high-throughput, multi-perspective agent systems.
