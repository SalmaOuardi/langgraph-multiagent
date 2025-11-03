"""
Calculator tool for mathematical operations.

Uses Python's eval() but with safety restrictions.
In production, you'd use a proper math parser like 'simpleeval'.
"""
import re
from typing import Union


class CalculatorTool:
    """
    Safe calculator for basic math operations.
    
    Use cases:
    - "What is 15 * 24 + 50?"
    - "Calculate 2^10"
    - "What's 100 / 7?"
    """
    
    # Allowed operations (whitelist approach for safety)
    ALLOWED_OPERATORS = {'+', '-', '*', '/', '**', '(', ')', '.'}
    ALLOWED_FUNCTIONS = {'abs', 'round', 'min', 'max', 'sum'}
    
    def calculate(self, expression: str) -> str:
        """
        Evaluate a mathematical expression safely.
        
        Args:
            expression: Math expression as string (e.g., "2 + 2")
            
        Returns:
            Result as string, or error message
        """
        try:
            # Clean the expression
            expression = expression.strip()
            
            # Basic safety check: only allow numbers, operators, and spaces
            # This prevents malicious code injection
            allowed_chars = set('0123456789.+-*/() ')
            if not all(c in allowed_chars for c in expression):
                return f"Error: Expression contains invalid characters. Only numbers and +, -, *, /, (), . allowed."
            
            # Evaluate (still use with caution in production!)
            result = eval(expression)
            
            # Format result nicely
            if isinstance(result, float):
                # Round to 2 decimal places for readability
                if result.is_integer():
                    return str(int(result))
                else:
                    return f"{result:.2f}"
            return str(result)
        
        except ZeroDivisionError:
            return "Error: Division by zero"
        except SyntaxError:
            return f"Error: Invalid mathematical expression"
        except Exception as e:
            return f"Error: {str(e)}"


# Create singleton
calculator_tool = CalculatorTool()


def calculate(expression: str) -> str:
    """
    Convenience function for calculations.
    This is what the agent will actually call.
    """
    return calculator_tool.calculate(expression)


# Test it
if __name__ == "__main__":
    # Test cases
    test_cases = [
        "2 + 2",
        "15 * 24 + 50",
        "100 / 3",
        "2 ** 10",
        "10 / 0",  # Should handle error
        "import os",  # Should reject (security)
    ]
    
    for expr in test_cases:
        print(f"{expr} = {calculate(expr)}")