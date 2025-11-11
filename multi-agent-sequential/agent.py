from google.adk.agents import SequentialAgent

from .sub_agents.outline_agent.agent import outline_agent
from .sub_agents.writer_agent.agent import writer_agent
from .sub_agents.editor_agent.agent import editor_agent

root_agent = SequentialAgent(
    name="BlogPipeline",
    sub_agents=[outline_agent, writer_agent, editor_agent],
)