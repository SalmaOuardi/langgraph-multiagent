"""
Basic usage example for the multi-tool agent.

This shows the simplest way to use the agent.
"""
import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from agents.multi_tool import create_multi_tool_agent


def main():
    print("="*70)
    print("🤖 Multi-Tool Agent - Basic Usage Example")
    print("="*70)
    
    # Create the agent
    print("\n📦 Creating agent...")
    agent = create_multi_tool_agent()
    print("✅ Agent ready!\n")
    
    # Example questions demonstrating each tool
    examples = [
        {
            "question": "What is 456 * 789?",
            "expected_tool": "calculator",
            "description": "Math calculation"
        },
        {
            "question": "What are the latest features in Python 3.12?",
            "expected_tool": "search",
            "description": "Current information"
        },
        {
            "question": "What is machine learning?",
            "expected_tool": "direct",
            "description": "General knowledge"
        },
    ]
    
    # Run each example
    for i, example in enumerate(examples, 1):
        print(f"\n{'='*70}")
        print(f"Example {i}: {example['description']}")
        print(f"{'='*70}")
        print(f"❓ Question: {example['question']}")
        print(f"🎯 Expected tool: {example['expected_tool']}")
        print(f"\n{'─'*70}")
        
        # Invoke the agent
        result = agent.invoke({"question": example['question']})
        
        # Show results
        print(f"\n📊 Results:")
        print(f"   Tool used: {result['tool_choice']}")
        
        # Check if correct tool was chosen
        if result['tool_choice'] == example['expected_tool']:
            print(f"   ✅ Correct tool selected!")
        else:
            print(f"   ⚠️  Expected {example['expected_tool']}, got {result['tool_choice']}")
        
        print(f"\n💬 Answer:")
        print(f"   {result['final_answer']}")
        print(f"{'─'*70}")
    
    print("\n" + "="*70)
    print("✅ All examples completed!")
    print("="*70)


if __name__ == "__main__":
    main()