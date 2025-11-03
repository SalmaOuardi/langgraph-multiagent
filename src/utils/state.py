"""
State definitions for LangGraph agents.
"""
from typing import TypedDict, List, Literal, Optional


class MultiToolState(TypedDict):
    """State for multi-tool routing agent."""
    
    question: str
    tool_choice: Optional[Literal["search", "calculator", "direct"]]
    tool_input: Optional[str]
    tool_output: Optional[str]
    final_answer: str


class ConversationState(TypedDict):
    """State for conversational agent with memory."""
    
    messages: List[dict]  # Full conversation history
    current_question: str
    retrieved_context: Optional[str]  # Relevant past context
    answer: str