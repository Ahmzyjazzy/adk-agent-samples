from google.adk.agents import LoopAgent, SequentialAgent

from .sub_agents.critic_agent.agent import critic_agent;
from .sub_agents.refiner_agent.agent import refiner_agent;
from .sub_agents.initial_writer_agent.agent import initial_writer_agent;

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