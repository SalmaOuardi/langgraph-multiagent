# Examples

Run examples from the repository root with an active virtual environment (`uv venv && source .venv/bin/activate`).

- `python examples/basic_usage.py` — shows the multi-tool router picking calculator/search/direct.
- `python examples/with_memory.py` — demonstrates a follow-up question that reuses conversation memory.
- `python examples/interactive_cli.py` — launches a simple chat loop with tool routing.

Tips:
- Set `TAVILY_API_KEY` to enable live web search; without it the search tool will return a clear message instead of failing import.
- Ensure `ollama` is running with the `mistral` model pulled for local LLM calls.
