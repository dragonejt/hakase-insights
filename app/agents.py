from os import getenv

from langchain import hub
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_community.chat_models.cloudflare_workersai import ChatCloudflareWorkersAI

from app.tools import current_time


def date_time_agent() -> AgentExecutor:
    """Create a date time agent using the current time tool."""

    tools = [current_time]

    # Load the language model from langchain hub
    llm = ChatCloudflareWorkersAI(
        account_id=getenv("CF_ACCOUNT_ID"),
        api_token=getenv("CF_API_TOKEN"),
        model="@hf/nousresearch/hermes-2-pro-mistral-7b",
    )

    prompt = hub.pull("langchain-ai/openai-functions-template")

    # Create a react agent with the language model and tools
    agent = create_tool_calling_agent(llm, tools, prompt)

    # Create an agent executor with the agent and tools
    executor = AgentExecutor(agent=agent, tools=tools)

    return executor
