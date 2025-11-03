"""
Multi-tool agent with routing logic.

This agent can:
1. Decide which tool to use (router)
2. Execute the chosen tool
3. Synthesize the final answer
"""
from langgraph.graph import StateGraph, END
from typing import Literal
import ollama

from utils.state import MultiToolState
from utils.prompts import ROUTER_PROMPT, SYNTHESIZER_PROMPT, DIRECT_ANSWER_PROMPT
from tools.search import search_web
from tools.calculator import calculate


# ====================
# NODE 1: ROUTER
# ====================

def router_node(state: MultiToolState) -> dict:
    """
    Decides which tool to use based on the question.
    
    This is the "brain" - it analyzes the question and picks a tool.
    
    Args:
        state: Current state with 'question'
        
    Returns:
        Updated state with 'tool_choice'
    """
    question = state['question']
    
    print(f"\n🧠 Router analyzing: '{question}'")
    
    # Ask LLM to classify the question
    prompt = ROUTER_PROMPT.format(question=question)
    
    response = ollama.generate(
        model='mistral',
        prompt=prompt,
        options={
            'temperature': 0.1,  # Low temperature = more deterministic
            'num_predict': 10,   # We only need one word, so limit tokens
        }
    )
    
    # Extract the tool choice
    tool_choice = response['response'].strip().lower()
    
    # Validate it's one of our tools
    if tool_choice not in ['search', 'calculator', 'direct']:
        print(f"⚠️  Invalid tool '{tool_choice}', defaulting to 'direct'")
        tool_choice = 'direct'
    
    print(f"✅ Router chose: {tool_choice}")
    
    return {"tool_choice": tool_choice}


# ====================
# NODE 2: SEARCH TOOL
# ====================

def search_node(state: MultiToolState) -> dict:
    """
    Executes web search.
    
    Args:
        state: Current state with 'question'
        
    Returns:
        Updated state with 'tool_output'
    """
    question = state['question']
    
    print(f"\n🔍 Searching web for: '{question}'")
    
    # Execute search
    results = search_web(question)
    
    print(f"✅ Search complete, got {len(results)} characters of results")
    
    return {"tool_output": results}


# ====================
# NODE 3: CALCULATOR TOOL
# ====================

def calculator_node(state: MultiToolState) -> dict:
    """
    Executes calculation.
    
    Args:
        state: Current state with 'question'
        
    Returns:
        Updated state with 'tool_output'
    """
    question = state['question']
    
    print(f"\n🔢 Calculating: '{question}'")
    
    # First, extract just the math expression from the question
    # We'll ask the LLM to help us extract it
    extract_prompt = f"""Extract ONLY the mathematical expression from this question. Return just the numbers and operators, nothing else.

Question: {question}

Mathematical expression:"""
    
    response = ollama.generate(
        model='mistral',
        prompt=extract_prompt,
        options={'temperature': 0.1}
    )
    
    expression = response['response'].strip()
    print(f"   Extracted expression: {expression}")
    
    # Calculate
    result = calculate(expression)
    
    print(f"✅ Result: {result}")
    
    return {"tool_output": f"Calculation: {expression} = {result}"}


# ====================
# NODE 4: DIRECT ANSWER
# ====================

def direct_answer_node(state: MultiToolState) -> dict:
    """
    Answers directly without tools.
    
    Args:
        state: Current state with 'question'
        
    Returns:
        Updated state with 'tool_output'
    """
    question = state['question']
    
    print(f"\n💭 Answering directly: '{question}'")
    
    prompt = DIRECT_ANSWER_PROMPT.format(question=question)
    
    response = ollama.generate(
        model='mistral',
        prompt=prompt,
        options={'temperature': 0.7}  # Bit higher for natural language
    )
    
    answer = response['response'].strip()
    
    print(f"✅ Direct answer generated")
    
    return {"tool_output": answer}


# ====================
# NODE 5: SYNTHESIZER
# ====================

def synthesizer_node(state: MultiToolState) -> dict:
    """
    Creates final answer from tool output.
    
    Args:
        state: Current state with 'question' and 'tool_output'
        
    Returns:
        Updated state with 'final_answer'
    """
    question = state['question']
    tool_output = state['tool_output']
    
    print(f"\n✨ Synthesizing final answer...")
    
    # If it was a direct answer, we can just use it
    if state['tool_choice'] == 'direct':
        return {"final_answer": tool_output}
    
    # Otherwise, synthesize from tool output
    prompt = SYNTHESIZER_PROMPT.format(
        question=question,
        tool_output=tool_output
    )
    
    response = ollama.generate(
        model='mistral',
        prompt=prompt,
        options={'temperature': 0.5}
    )
    
    final_answer = response['response'].strip()
    
    print(f"✅ Final answer ready")
    
    return {"final_answer": final_answer}


# ====================
# ROUTING FUNCTION
# ====================

def route_to_tool(state: MultiToolState) -> Literal["search", "calculator", "direct"]:
    """
    This function tells LangGraph which node to go to next.
    
    It's called after the router_node finishes.
    
    Args:
        state: Current state with 'tool_choice'
        
    Returns:
        Name of the next node to execute
    """
    # Simply return the tool choice - LangGraph will route to that node
    return state['tool_choice']


# ====================
# CREATE THE AGENT
# ====================

def create_multi_tool_agent():
    """
    Creates and compiles the multi-tool agent.
    
    Graph structure:
        START
          ↓
        router (decides: search/calculator/direct)
          ↓
        [conditional edges]
          ↓
        search_node OR calculator_node OR direct_node
          ↓
        synthesizer
          ↓
        END
    
    Returns:
        Compiled LangGraph agent
    """
    # Create the graph
    workflow = StateGraph(MultiToolState)
    
    # Add all nodes
    workflow.add_node("router", router_node)
    workflow.add_node("search", search_node)
    workflow.add_node("calculator", calculator_node)
    workflow.add_node("direct", direct_answer_node)
    workflow.add_node("synthesizer", synthesizer_node)
    
    # Set entry point
    workflow.set_entry_point("router")
    
    # Add conditional edges from router to tools
    # This is the magic - based on router's decision, go to different nodes
    workflow.add_conditional_edges(
        "router",  # From this node
        route_to_tool,  # Use this function to decide where to go
        {
            "search": "search",        # If returns "search", go to search node
            "calculator": "calculator",  # If returns "calculator", go to calculator node
            "direct": "direct"         # If returns "direct", go to direct node
        }
    )
    
    # All tools connect to synthesizer
    workflow.add_edge("search", "synthesizer")
    workflow.add_edge("calculator", "synthesizer")
    workflow.add_edge("direct", "synthesizer")
    
    # Synthesizer connects to END
    workflow.add_edge("synthesizer", END)
    
    # Compile the graph
    return workflow.compile()


# ====================
# TEST THE AGENT
# ====================

if __name__ == "__main__":
    print("=" * 70)
    print("🤖 MULTI-TOOL AGENT TEST")
    print("=" * 70)
    
    # Create agent
    agent = create_multi_tool_agent()
    
    # Test questions (one for each tool)
    test_questions = [
        "What is 157 * 23?",  # Should use calculator
        "What are the latest developments in LangGraph?",  # Should use search
        "What is Python?",  # Should use direct
    ]
    
    for question in test_questions:
        print("\n" + "="*70)
        print(f"❓ QUESTION: {question}")
        print("="*70)
        
        # Invoke the agent
        result = agent.invoke({"question": question})
        
        print("\n" + "-"*70)
        print(f"📊 RESULT:")
        print(f"   Tool used: {result['tool_choice']}")
        print(f"   Final answer: {result['final_answer']}")
        print("-"*70)