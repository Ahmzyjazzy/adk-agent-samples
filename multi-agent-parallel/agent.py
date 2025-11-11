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