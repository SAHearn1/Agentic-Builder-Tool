"""
DevOps-Builder Agent using LangGraph and Claude 3.5 Sonnet.
This agent acts as an autonomous DevOps engineer.
"""
import os
from typing import TypedDict, Annotated, Sequence
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from tools import get_tools


def create_agent_graph():
    """
    Creates and returns the DevOps-Builder agent graph with Claude 3.5 Sonnet.
    Uses LangGraph's ReAct agent with memory persistence.
    """
    # Get Anthropic API key
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not anthropic_api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is not set")
    
    # Initialize Claude 3.5 Sonnet model
    llm = ChatAnthropic(
        model="claude-3-5-sonnet-20240620",
        anthropic_api_key=anthropic_api_key,
        temperature=0.7,
        max_tokens=4096,
        timeout=60.0,
    )
    
    # Get all tools (GitHub, Vercel, GCS)
    tools = get_tools()
    
    # Create memory saver for conversation persistence
    memory = MemorySaver()
    
    # Create ReAct agent with tools and memory
    agent_graph = create_react_agent(
        model=llm,
        tools=tools,
        checkpointer=memory,
        state_modifier=(
            "You are an expert DevOps engineer assistant. "
            "You help with code deployment, infrastructure management, and automation tasks. "
            "You have access to GitHub for repository management, Vercel for deployments, "
            "and Google Cloud Storage for logging build statuses. "
            "Always be helpful, precise, and production-focused in your responses."
        )
    )
    
    return agent_graph


# Create the agent graph instance
agent_graph = create_agent_graph()
