# LangGraph Multi-Agent System

A modular multi-agent system built with LangGraph, featuring tool routing, conversational memory, and flexible agent orchestration.

## 🎯 Features

- **Multi-tool routing**: Automatically routes queries to web search, calculator, or direct LLM
- **Conversational memory**: Maintains context across multiple turns
- **Modular architecture**: Easy to extend with new tools and agents
- **Type-safe state management**: Pydantic-based state definitions
- **Production-ready**: Error handling, logging, tests

## 🏗️ Architecture

### Multi-Tool Agent
```
User Query → Router → [Search | Calculator | Direct] → Synthesizer → Answer
```

### Conversational Agent
```
Query → Memory Check → [Use History | Fetch New Info] → Answer + Update Memory
```

## 🚀 Quick Start
```bash
# Setup with uv
uv venv
source .venv/bin/activate
uv pip install -e .

# Configure environment
cp .env.example .env
# Add your TAVILY_API_KEY

# Install Ollama
ollama pull mistral

# Run examples
python examples/basic_usage.py
python examples/with_memory.py
```

## 📖 Examples

### Basic Multi-Tool Agent
```python
from src.agents.multi_tool import create_multi_tool_agent

agent = create_multi_tool_agent()
result = agent.invoke({"question": "What are the latest AI trends?"})
print(result["final_answer"])
```

### With Conversation Memory
```python
from src.agents.conversational import create_conversational_agent

agent = create_conversational_agent()
messages = []

# First question
result = agent.invoke({
    "messages": messages,
    "current_question": "Who created LangGraph?"
})

# Follow-up (uses memory)
messages.append({"role": "user", "content": "Who created LangGraph?"})
messages.append({"role": "assistant", "content": result["answer"]})

result = agent.invoke({
    "messages": messages,
    "current_question": "What else did they build?"
})
```

## 🛠️ Tech Stack

- **Framework**: LangGraph 0.0.20
- **LLM**: Mistral 7B (via Ollama)
- **Search**: Tavily API
- **Package Manager**: uv
- **Python**: 3.9+

## 📁 Project Structure
```
langgraph-multiagent/
├── src/
│   ├── agents/
│   │   ├── multi_tool.py       # Multi-tool routing agent
│   │   └── conversational.py   # Agent with memory
│   ├── tools/
│   │   ├── search.py           # Web search (Tavily)
│   │   └── calculator.py       # Math calculations
│   ├── utils/
│   │   ├── state.py            # State type definitions
│   │   └── prompts.py          # Prompt templates
│   └── main.py
├── tests/
├── examples/
│   ├── basic_usage.py
│   └── with_memory.py
├── docs/
└── pyproject.toml
```

## 🧪 Testing
```bash
uv pip install -e ".[dev]"
pytest tests/
```

## 📚 Documentation

- [Architecture Details](docs/ARCHITECTURE.md)
- [Usage Examples](docs/EXAMPLES.md)

## 🤝 Contributing

This is a personal learning project, but suggestions are welcome!

## 📝 License

MIT

---

**Built with LangGraph** | Salma Ouardi | 2024