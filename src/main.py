"""
Main entry point for the multi-tool agent.

This provides a simple CLI interface.
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Multi-Tool Agent - LangGraph-based agent with search and calculator"
    )
    parser.add_argument(
        'question',
        nargs='?',
        help='Question to ask the agent (if not provided, starts interactive mode)'
    )
    parser.add_argument(
        '--interactive',
        '-i',
        action='store_true',
        help='Start interactive mode'
    )
    
    args = parser.parse_args()
    
    # Interactive mode
    if args.interactive or not args.question:
        from examples.interactive_cli import main as interactive_main
        interactive_main()
    else:
        # Single question mode
        from src.agents.multi_tool import create_multi_tool_agent
        
        print(f"\n❓ Question: {args.question}\n")
        
        agent = create_multi_tool_agent()
        result = agent.invoke({"question": args.question})
        
        print(f"🤖 Answer: {result['final_answer']}")
        print(f"\n(Used tool: {result['tool_choice']})\n")


if __name__ == "__main__":
    main()