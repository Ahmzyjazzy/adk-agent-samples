# Multi-Agent Loop Sample — StoryPipeline

This sample demonstrates an iterative refinement workflow using a `LoopAgent`. A story writer produces an initial draft, then enters a loop where a critic reviews the work and a refiner applies feedback. The loop continues until the critic approves the story (or a max iteration limit is reached), making this an ideal pattern for iterative improvement cycles.

## What this sample demonstrates

- Using `LoopAgent` to run agents repeatedly until a termination condition is met
- An `InitialWriterAgent` that runs once to produce a first draft
- A `CriticAgent` that evaluates and provides feedback (or signals approval)
- A `RefinerAgent` that either refines based on feedback or calls `exit_loop()` to terminate the loop
- How to use `FunctionTool` to explicitly control loop exit from within an agent
- Combining `SequentialAgent` and `LoopAgent` in the root workflow

## Files

- `agent.py` — Constructs `story_refinement_loop` (a `LoopAgent` with critic + refiner) and `root_agent` (a `SequentialAgent` that runs initial writer then the loop)
- `sub_agents/initial_writer_agent/agent.py` — `InitialWriterAgent` produces a first draft and stores it as `current_story`
- `sub_agents/critic_agent/agent.py` — `CriticAgent` reviews the story and outputs `critique` (either feedback or "APPROVED")
- `sub_agents/refiner_agent/agent.py` — `RefinerAgent` refines the story or calls `exit_loop()` to exit the loop
- `tools.py` — Defines the `exit_loop` function that signals loop termination

## Example wiring (from `agent.py`)

```python
from google.adk.agents import LoopAgent, SequentialAgent

from .sub_agents.critic_agent.agent import critic_agent
from .sub_agents.refiner_agent.agent import refiner_agent
from .sub_agents.initial_writer_agent.agent import initial_writer_agent

# The LoopAgent contains the agents that will run repeatedly: Critic -> Refiner.
story_refinement_loop = LoopAgent(
    name="StoryRefinementLoop",
    sub_agents=[critic_agent, refiner_agent],
    max_iterations=2,  # Prevents infinite loops
)

# The root agent is a SequentialAgent that defines the overall workflow: Initial Write -> Refinement Loop.
root_agent = SequentialAgent(
    name="StoryPipeline",
    sub_agents=[initial_writer_agent, story_refinement_loop],
) 
```

## How the iterative loop works

1. **Initial Write**: `InitialWriterAgent` writes a first draft and stores it as `current_story` in the session state.
2. **Enter Loop** (max 2 iterations in this example):
   - **Critic Step**: `CriticAgent` reads `{current_story}` and outputs feedback (`critique`). If the story is good, it outputs exactly `"APPROVED"`.
   - **Refiner Step**: `RefinerAgent` reads both `{current_story}` and `{critique}`:
     - If critique is `"APPROVED"`, it calls `exit_loop()` to terminate the loop immediately.
     - Otherwise, it rewrites the story, updating `current_story` for the next iteration.
3. After the loop exits (either by approval or max iterations), the final story is returned.

This pattern is ideal when you have an iterative improvement process with a clear exit condition.

## Key components

- **LoopAgent**: Runs sub-agents in sequence repeatedly until max iterations or an explicit exit signal.
- **FunctionTool**: Used by the refiner to call `exit_loop()` when the critic approves.
- **output_key**: Both critic and refiner update the shared state (`critique`, `current_story`).

## Advantages of loop agents

- Handles iterative refinement naturally (no need to manually hardcode retry logic).
- Provides a clear exit condition via `FunctionTool` (e.g., when a critic approves).
- Max iterations prevent infinite loops in production.

When NOT to use loop agents:
- When you have a fixed sequence of steps (use `SequentialAgent` instead).
- When parallel independent tasks are needed (use `ParallelAgent` instead).

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

Run an in-memory iterative refinement example (create `example_loop_run.py` and run with `uv run python example_loop_run.py`):

```python
# example_loop_run.py
from multi_agent_loop import root_agent
from google.adk.runners import InMemoryRunner

runner = InMemoryRunner(root_agent)
query = "Write a short story about a robot discovering friendship."
resp = runner.run(query)
print(resp)
```

Notes:
- To obtain your `GOOGLE_API_KEY` go to [AI Studio](https://aistudio.google.com/api-keys) to create one
- Adjust `max_iterations` in `agent.py` to balance refinement depth and latency.
- Monitor token usage since each iteration runs multiple agents (critic + refiner).

## Tips

- Keep the critic's evaluation criteria clear in its instruction (e.g., "respond with exactly APPROVED if...").
- Use explicit output signals (like `exit_loop()`) rather than trying to parse model outputs for loop control.
- Log or inspect intermediate states (`current_story`, `critique`) to debug refinement cycles.
- Start with a small `max_iterations` (e.g., 2–3) and increase if needed to avoid runaway costs.

## Troubleshooting

- If the loop doesn't exit: ensure the refiner is calling `exit_loop()` when the critique is exactly `"APPROVED"`.
- If the refiner produces low-quality refinements: tighten the instruction or check that feedback from the critic is clear and specific.
- If hitting max iterations without approval: consider adjusting the critic's approval criteria or using more iterations.

---

This loop sample is a starting point for any iterative improvement workflow — from story refinement to code review cycles to proposal evaluation pipelines.