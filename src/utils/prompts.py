"""
Prompt templates for agents.
"""

ROUTER_PROMPT = """You are a routing assistant. Your job is to decide which tool to use.

Question: "{question}"

Available tools:
- "search": Use for questions about current events, news, facts that change, or things happening now
  Examples: "What happened today?", "Who won the election?", "Latest AI news"
  
- "calculator": Use for mathematical calculations and numerical operations
  Examples: "What is 25 * 17?", "Calculate 2^10", "100 / 7"
  
- "direct": Use if you can answer from your general knowledge without external tools
  Examples: "What is Python?", "Explain machine learning", "What is the capital of France?"

Think step by step:
1. Does this need current/recent information? → search
2. Does this need precise calculation? → calculator  
3. Can I answer from general knowledge? → direct

Respond with ONLY ONE WORD: search, calculator, or direct"""


SYNTHESIZER_PROMPT = """You are a helpful assistant. Answer the user's question based on the information provided.

Question: {question}

Information gathered from tools:
{tool_output}

Instructions:
- Answer directly and concisely
- Use the information provided
- If information is insufficient, say so
- Be factual and precise

Answer:"""


DIRECT_ANSWER_PROMPT = """You are a helpful assistant. Answer this question directly using your knowledge.

Question: {question}

Instructions:
- Be concise (2-4 sentences)
- Be factual
- If you're not sure, say so

Answer:"""


MEMORY_SUMMARY_PROMPT = """You are a conversation memory module.

Conversation so far:
{history}

Current question: {question}

Summarize the key facts or answers that are relevant to the current question.
Keep it to 3 bullet points or fewer."""


CONVERSATION_ANSWER_PROMPT = """You are a helpful assistant continuing a conversation.

Conversation so far:
{history}

Relevant context:
{context}

User question: {question}

Answer concisely (3-5 sentences) using the relevant context when available."""
