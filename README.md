# ADK Agent Samples

A collection of sample applications demonstrating the capabilities of the Google Agent Development Kit (ADK). These samples showcase how to build intelligent agents using the Gemini LLM and various tools.

## Overview

This project contains practical examples of how to create and configure agents using the Google ADK framework. Each sample demonstrates different features and use cases for building AI-powered applications.

## Project Structure

```
.
├── basic-agent/          # Basic agent example
│   ├── agent.py          # Agent configuration and setup
│   ├── util.py           # Utility functions
│   └── __init__.py
├── main.py               # Main entry point
├── pyproject.toml        # Project configuration
├── Makefile              # Build and run commands
└── README.md             # This file
```

## Requirements

- **uv**: Fast Python package manager (v0.9.8 or later recommended)
- **Python**: 3.11 or higher
- **Google ADK**: >= 1.18.0

## Installation

This project uses [uv](https://docs.astral.sh/uv/) for fast and reliable Python package management.

### Option 1: Using Make (Recommended)

The easiest way to get started:

```bash
make install
```

This command will:
- Install `uv` if not already present
- Sync all Python dependencies

### Option 2: Using uv Directly

If you have `uv` already installed:

```bash
uv sync
```

### Installing uv

If you need to install `uv` manually:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

For more installation options, visit the [uv documentation](https://docs.astral.sh/uv/getting-started/installation/).

## Getting Started

### Basic Agent Example

The `basic-agent` module demonstrates a simple agent configuration:

```python
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search

root_agent = Agent(
    name="helpful_assistant",
    model=Gemini(model="gemini-2.5-flash-lite"),
    description="A simple agent that can answer general questions.",
    instruction="You are a helpful assistant. Use Google Search for current info or if unsure.",
    tools=[google_search],
)
```

### Key Features

- **Gemini LLM Integration**: Utilizes the Gemini 2.5 Flash Lite model for fast and efficient responses
- **Tool Integration**: Includes Google Search tool for real-time information retrieval
- **Retry Logic**: Implements automatic retry handling for transient errors (rate limits, timeouts)
- **In-Memory Execution**: Uses InMemoryRunner for straightforward agent execution

### Error Handling

The agents are configured with robust retry options to handle transient failures:

```python
retry_config = types.HttpRetryOptions(
    attempts=5,              # Maximum retry attempts
    exp_base=7,              # Delay multiplier for exponential backoff
    initial_delay=1,         # Initial delay in seconds
    http_status_codes=[429, 500, 503, 504]  # Errors to retry on
)
```

## Usage

### Using Make Commands (Recommended)

The `Makefile` provides convenient commands for common tasks:

```bash
make install     # Install dependencies and setup environment
make dev         # Start the ADK API server for development
make playground  # Launch the web playground (Streamlit)
```

### Using uv Directly

If you prefer to run commands directly with `uv`:

```bash
# Run the API server
uv run adk api_server . --allow_origins="*"

# Launch the web playground
uv run adk web --port 8501
```

### Development Workflow

1. **Install dependencies**:
   ```bash
   make install
   ```

2. **Start the development API server**:
   ```bash
   make dev
   ```
   This starts the ADK API server with CORS enabled for all origins.

3. **Launch the playground** (in another terminal):
   ```bash
   make playground
   ```
   This opens the interactive web playground on port 8501.


## Configuration

### Environment Variables

Ensure you have the necessary Google API credentials configured:

- Set up Google Cloud authentication (typically via `GOOGLE_APPLICATION_CREDENTIALS`)
- Configure API keys or service account credentials as needed for Google Search and Gemini APIs

## Examples

### Creating a Custom Agent

To create your own agent, follow this pattern:

1. Import necessary ADK components
2. Configure retry options (optional but recommended)
3. Create an Agent instance with:
   - A descriptive name
   - An LLM model (Gemini, etc.)
   - A description of the agent's purpose
   - Clear instructions for the agent's behavior
   - A list of tools the agent can use

```python
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini

my_agent = Agent(
    name="my_custom_agent",
    model=Gemini(model="gemini-2.5-flash-lite"),
    description="My custom agent description",
    instruction="Your specific instructions here",
    tools=[],  # Add tools as needed
)
```

## Dependencies

- **google-adk**: Google Agent Development Kit for building intelligent agents
- **Python**: 3.11+

## Contributing

Contributions are welcome! Please ensure that:

1. Your code follows the existing style and structure
2. All dependencies are properly documented in `pyproject.toml`
3. New samples include clear documentation and comments

## License

This project is provided as sample code by Ahmzy Codelabs LLC.

## Support

For issues, questions, or contributions, please contact: contact@ahmzycodelabs.dev

---

**Version**: 0.1.0  
**Author**: Ahmzy Codelabs LLC  
**Last Updated**: November 2025
