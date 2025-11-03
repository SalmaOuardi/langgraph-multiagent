"""
Interactive CLI for chatting with the multi-tool agent.

Run this to have a conversation with the agent in your terminal.
"""
import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from agents.multi_tool import create_multi_tool_agent


def print_banner():
    """Print welcome banner"""
    banner = """
╔══════════════════════════════════════════════════════════════════════╗
║                   🤖 Multi-Tool Agent CLI                            ║
║                                                                      ║
║  Ask me anything! I can:                                            ║
║  • Search the web for current information                           ║
║  • Calculate mathematical expressions                               ║
║  • Answer general knowledge questions                               ║
║                                                                      ║
║  Commands:                                                          ║
║  • 'quit' or 'exit' - Exit the program                             ║
║  • 'help' - Show this message                                      ║
║  • 'clear' - Clear screen                                          ║
╚══════════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_help():
    """Print help message"""
    help_text = """
📖 HELP

Example questions:
  Math:        "What is 25 * 17 + 100?"
  Web Search:  "What happened in AI this week?"
  Knowledge:   "What is Python?"

The agent will automatically choose the right tool!

Commands:
  quit, exit - Exit the program
  help       - Show this message
  clear      - Clear the screen
    """
    print(help_text)


def clear_screen():
    """Clear the terminal screen"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def format_result(result: dict) -> str:
    """
    Format the agent's result for display.
    
    Args:
        result: Agent result dictionary
        
    Returns:
        Formatted string
    """
    tool_icons = {
        'search': '🔍',
        'calculator': '🔢',
        'direct': '💭'
    }
    
    tool = result.get('tool_choice', 'unknown')
    icon = tool_icons.get(tool, '🤖')
    
    output = f"\n{icon} Tool used: {tool}\n"
    output += f"{'─'*70}\n"
    output += f"{result['final_answer']}\n"
    output += f"{'─'*70}\n"
    
    return output


def main():
    """Main interactive loop"""
    # Print welcome banner
    clear_screen()
    print_banner()
    
    # Create agent
    print("\n📦 Initializing agent...")
    try:
        agent = create_multi_tool_agent()
        print("✅ Agent ready! Type 'help' for instructions.\n")
    except Exception as e:
        print(f"❌ Error creating agent: {e}")
        print("Make sure Ollama is running and Mistral is installed.")
        print("Run: ollama pull mistral")
        sys.exit(1)
    
    # Interactive loop
    question_count = 0
    
    while True:
        try:
            # Get user input
            user_input = input("\n💬 You: ").strip()
            
            # Handle empty input
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if user_input.lower() == 'help':
                print_help()
                continue
            
            if user_input.lower() == 'clear':
                clear_screen()
                print_banner()
                continue
            
            # Process question with agent
            print(f"\n🤖 Agent: Thinking...")
            
            result = agent.invoke({"question": user_input})
            
            # Display result
            print(format_result(result))
            
            question_count += 1
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again or type 'quit' to exit.\n")
    
    # Summary
    if question_count > 0:
        print(f"\n📊 Session summary: {question_count} questions answered")


if __name__ == "__main__":
    main()