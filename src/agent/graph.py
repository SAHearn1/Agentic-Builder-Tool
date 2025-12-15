"""LangGraph agent graph definition."""

from typing import Literal

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage
from langgraph.graph import END, StateGraph
from langgraph.prebuilt import ToolNode

from src.config import get_settings
from src.tools import get_all_tools

from .state import AgentState


# System message for the agent
SYSTEM_MESSAGE = """You are an autonomous DevOps engineer agent. Your role is to:
1. Write production-quality code based on user requirements
2. Commit code to GitHub repositories
3. Deploy applications to Vercel
4. Store artifacts in Google Cloud Storage

Always think step-by-step and use the available tools to accomplish tasks.
Be thorough and ensure deployments are successful."""


def create_agent_graph():
    """Create the LangGraph agent graph for autonomous DevOps operations.

    Returns:
        Compiled LangGraph graph
    """
    settings = get_settings()

    # Initialize Claude model
    model = ChatAnthropic(
        model=settings.agent_model,
        api_key=settings.anthropic_api_key,
        temperature=settings.agent_temperature,
    )

    # Get tools
    tools = get_all_tools()

    # Bind tools to model
    model_with_tools = model.bind_tools(tools)

    # Define agent node
    def call_model(state: AgentState) -> AgentState:
        """Call the LLM with tools."""
        messages = state["messages"]

        # Add system message if this is the first call
        if len(messages) == 1:
            system_message = SystemMessage(content=SYSTEM_MESSAGE)
            messages = [system_message] + list(messages)

        response = model_with_tools.invoke(messages)

        # Update iteration count
        iteration_count = state.get("iteration_count", 0) + 1

        return {
            "messages": [response],
            "iteration_count": iteration_count,
        }

    # Define routing function
    def should_continue(state: AgentState) -> Literal["tools", "end"]:
        """Determine if the agent should continue or end."""
        messages = state["messages"]
        last_message = messages[-1]

        # Check iteration limit
        if state.get("iteration_count", 0) >= settings.agent_max_iterations:
            return "end"

        # If there are tool calls, continue to tools
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "tools"

        # Otherwise, end
        return "end"

    # Create the graph
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", ToolNode(tools))

    # Set entry point
    workflow.set_entry_point("agent")

    # Add edges
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "end": END,
        },
    )
    workflow.add_edge("tools", "agent")

    # Compile the graph
    return workflow.compile()
