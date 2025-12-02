import sys
from pathlib import Path

import pytest

ollama = pytest.importorskip("ollama")
langgraph = pytest.importorskip("langgraph")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import agents.conversational as conversational
import agents.multi_tool as multi_tool
from tools.search import WebSearchTool


def test_web_search_tool_graceful_when_missing_api_key(monkeypatch):
    monkeypatch.delenv("TAVILY_API_KEY", raising=False)
    tool = WebSearchTool()

    result = tool.search("LangGraph latest features")
    assert "unavailable" in result.lower()


def test_multi_tool_agent_routing_and_synthesis(monkeypatch):
    def fake_generate(model, prompt, options=None, **_):
        if "Respond with ONLY ONE WORD" in prompt:
            if "Latest AI news" in prompt:
                return {"response": "search"}
            return {"response": "calculator"}

        if "Extract ONLY the mathematical expression" in prompt:
            return {"response": "2 + 2"}

        if "Information gathered from tools" in prompt:
            if "search results stub" in prompt:
                return {"response": "Synthesized search answer"}
            return {"response": "Synthesized calculation answer"}

        if "Answer this question directly" in prompt:
            return {"response": "Direct response"}

        return {"response": "direct"}

    monkeypatch.setattr(multi_tool, "search_web", lambda query: "search results stub")
    monkeypatch.setattr(multi_tool.ollama, "generate", fake_generate)

    agent = multi_tool.create_multi_tool_agent()

    calc = agent.invoke({"question": "What is 2 + 2?"})
    assert calc["tool_choice"] == "calculator"
    assert "4" in calc["tool_output"]
    assert "Synthesized calculation answer" in calc["final_answer"]

    search = agent.invoke({"question": "Latest AI news"})
    assert search["tool_choice"] == "search"
    assert search["tool_output"] == "search results stub"
    assert "Synthesized search answer" in search["final_answer"]


def test_conversational_agent_updates_memory(monkeypatch):
    def fake_generate(model, prompt, options=None, **_):
        if "Summarize the key facts" in prompt:
            return {"response": "We discussed LangGraph and LangChain."}

        if "continuing a conversation" in prompt:
            return {"response": "LangChain also built LangServe."}

        return {"response": "Fallback response"}

    monkeypatch.setattr(conversational.ollama, "generate", fake_generate)

    agent = conversational.create_conversational_agent()
    start_messages = [
        {"role": "user", "content": "Who created LangGraph?"},
        {"role": "assistant", "content": "LangChain created it."},
    ]

    result = agent.invoke(
        {
            "messages": start_messages,
            "current_question": "What else has that team built?",
        }
    )

    assert result["retrieved_context"].startswith("We discussed")
    assert result["answer"] == "LangChain also built LangServe."
    assert len(result["messages"]) == len(start_messages) + 2
    assert result["messages"][-1]["content"] == "LangChain also built LangServe."
