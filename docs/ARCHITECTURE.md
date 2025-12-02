# Architecture

This project ships two LangGraph-powered agents that share common building blocks (LLM routing, tools, and conversation state).

## Multi-Tool Agent
- **Flow:** router → search/calculator/direct → synthesizer → END  
- **Router:** Classifies a question into `search`, `calculator`, or `direct` using a low-temperature LLM call.  
- **Tools:**  
  - `search` uses Tavily for current information (lazily configured so the module can be imported without an API key).  
  - `calculator` extracts a math expression with the LLM, then evaluates it with a guarded calculator.  
  - `direct` bypasses tools when the LLM can answer from prior knowledge.  
- **Synthesizer:** Combines the original question with tool output to produce the final answer.

## Conversational Agent
- **Flow:** retrieve_context → answer_question → update_memory → END  
- **retrieve_context:** Summarizes recent turns that might be relevant to the new question.  
- **answer_question:** Generates an answer using the conversation summary plus the current question.  
- **update_memory:** Appends the latest user/assistant turns to the running `messages` list so the next invocation has context.

## State Models
- `MultiToolState`: question + optional tool choice/output and final answer.  
- `ConversationState`: running `messages`, current question, retrieved context, and answer.  
Optional keys are declared with `typing.Required`/`NotRequired` for clearer type checking.

## Error Handling Notes
- Tavily is lazily imported and the search tool reports configuration issues instead of raising on import.  
- LLM calls are wrapped with lightweight fallbacks so the graphs keep running even when a call fails.
