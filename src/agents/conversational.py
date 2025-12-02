"""
Conversational agent with lightweight memory.
"""
from typing import List

import ollama
from langgraph.graph import END, StateGraph

from utils.prompts import CONVERSATION_ANSWER_PROMPT, MEMORY_SUMMARY_PROMPT
from utils.state import ConversationState


def _format_messages(messages: List[dict]) -> str:
    if not messages:
        return "No previous messages."

    lines = []
    for message in messages:
        role = message.get("role", "user").capitalize()
        content = message.get("content", "")
        lines.append(f"{role}: {content}")
    return "\n".join(lines)


def retrieve_context_node(state: ConversationState) -> dict:
    """
    Summarize prior conversation that is relevant to the new question.
    """
    history = state.get("messages", [])
    question = state["current_question"]

    if not history:
        return {"retrieved_context": "No relevant prior conversation."}

    prompt = MEMORY_SUMMARY_PROMPT.format(
        history=_format_messages(history),
        question=question,
    )

    try:
        response = ollama.generate(
            model="mistral",
            prompt=prompt,
            options={"temperature": 0.2, "num_predict": 150},
        )
        summary = response["response"].strip()
    except Exception as exc:
        summary = f"Memory retrieval unavailable: {exc}"

    return {"retrieved_context": summary}


def answer_question_node(state: ConversationState) -> dict:
    """
    Answer the user's question using any retrieved context.
    """
    prompt = CONVERSATION_ANSWER_PROMPT.format(
        history=_format_messages(state.get("messages", [])),
        context=state.get("retrieved_context") or "No prior context available.",
        question=state["current_question"],
    )

    try:
        response = ollama.generate(
            model="mistral",
            prompt=prompt,
            options={"temperature": 0.4},
        )
        answer = response["response"].strip()
    except Exception as exc:
        answer = f"Sorry, I could not generate an answer right now: {exc}"

    return {"answer": answer}


def update_memory_node(state: ConversationState) -> dict:
    """
    Append the latest turn to the running conversation history.
    """
    history = list(state.get("messages", []))
    history.append({"role": "user", "content": state["current_question"]})
    history.append({"role": "assistant", "content": state.get("answer", "")})

    return {"messages": history}


def create_conversational_agent():
    """
    Create a LangGraph conversational agent with memory.
    """
    workflow = StateGraph(ConversationState)

    workflow.add_node("retrieve_context", retrieve_context_node)
    workflow.add_node("answer_question", answer_question_node)
    workflow.add_node("update_memory", update_memory_node)

    workflow.set_entry_point("retrieve_context")
    workflow.add_edge("retrieve_context", "answer_question")
    workflow.add_edge("answer_question", "update_memory")
    workflow.add_edge("update_memory", END)

    return workflow.compile()


if __name__ == "__main__":
    agent = create_conversational_agent()
    initial_messages: List[dict] = [
        {"role": "user", "content": "Who created LangGraph?"},
        {"role": "assistant", "content": "LangChain created the LangGraph framework."},
    ]

    result = agent.invoke(
        {
            "messages": initial_messages,
            "current_question": "What else is LangChain known for?",
        }
    )

    print("\nFinal answer:", result["answer"])
