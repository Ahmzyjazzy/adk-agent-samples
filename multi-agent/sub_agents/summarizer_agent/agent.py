from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini

from config import retry_config

# Summarizer Agent: Its job is to summarize the text it receives.
summarizer_agent = Agent(
    name="SummarizerAgent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    # The instruction is modified to request a bulleted list for a clear output format.
    instruction="""Read the provided research findings: {research_findings} Create a concise summary as a bulleted list with 3-5 key points.""",
    output_key="final_summary",
)