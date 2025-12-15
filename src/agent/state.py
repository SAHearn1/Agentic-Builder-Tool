"""Agent state definition for LangGraph."""

from typing import Annotated, Sequence, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """State for the autonomous DevOps agent.
    
    Attributes:
        messages: Conversation history with the agent
        task: Current task description
        code_generated: Generated code content
        deployment_status: Status of deployment operations
        artifacts: URLs or references to created artifacts
        iteration_count: Number of iterations performed
    """
    
    messages: Annotated[Sequence[BaseMessage], add_messages]
    task: str
    code_generated: str
    deployment_status: str
    artifacts: list[str]
    iteration_count: int
