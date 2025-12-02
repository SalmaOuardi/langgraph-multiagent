"""
State definitions for LangGraph agents.
"""
from typing import List, Literal, Optional, TypedDict

try:
    from typing import NotRequired, Required
except ImportError:  # Python <3.11
    from typing_extensions import NotRequired, Required


class MultiToolState(TypedDict):
    """State for multi-tool routing agent."""

    question: Required[str]
    tool_choice: NotRequired[Literal["search", "calculator", "direct"]]
    tool_input: NotRequired[str]
    tool_output: NotRequired[str]
    final_answer: NotRequired[str]


class ConversationState(TypedDict):
    """State for conversational agent with memory."""

    messages: Required[List[dict]]
    current_question: Required[str]
    retrieved_context: NotRequired[Optional[str]]
    answer: NotRequired[str]
