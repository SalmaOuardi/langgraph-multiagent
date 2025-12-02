"""
Example demonstrating the conversational agent with memory.
"""
import sys
from pathlib import Path

src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from agents.conversational import create_conversational_agent


def main():
    print("=" * 70)
    print("🧠 Conversational Agent with Memory")
    print("=" * 70)

    agent = create_conversational_agent()
    messages = []

    first_question = "Who created LangGraph and what problem does it solve?"
    print(f"\n❓ Q1: {first_question}")
    first = agent.invoke({"messages": messages, "current_question": first_question})
    print(f"🤖 A1: {first['answer']}\n")

    messages = first["messages"]
    follow_up = "What else has that team built recently?"
    print(f"❓ Q2 (follow-up): {follow_up}")
    second = agent.invoke({"messages": messages, "current_question": follow_up})
    print(f"🤖 A2: {second['answer']}\n")

    print("📚 Conversation history tracked by the agent:")
    for msg in second["messages"]:
        print(f" - {msg['role']}: {msg['content']}")


if __name__ == "__main__":
    main()
