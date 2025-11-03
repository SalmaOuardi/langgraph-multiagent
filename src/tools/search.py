"""
Web search tool using Tavily API.

Why Tavily? It's designed for LLM agents - returns clean, formatted results
optimized for RAG and agent use cases.
"""
import os
from typing import List, Dict
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()


class WebSearchTool:
    """
    Web search tool that finds current information online.
    
    Use cases:
    - "What happened in AI this week?"
    - "Who won the World Cup 2023?"
    - "Latest news about LangGraph"
    """
    
    def __init__(self):
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            raise ValueError("TAVILY_API_KEY not found in environment")
        self.client = TavilyClient(api_key=api_key)
    
    def search(self, query: str, max_results: int = 3) -> str:
        """
        Search the web and return formatted results.
        
        Args:
            query: Search query
            max_results: Number of results to return (default 3)
            
        Returns:
            Formatted string with search results
        """
        try:
            # Tavily returns: {'results': [{'title': ..., 'content': ..., 'url': ...}]}
            response = self.client.search(
                query=query,
                max_results=max_results,
                search_depth="basic"  # or "advanced" for deeper search
            )
            
            # Format results for LLM consumption
            formatted_results = []
            for i, result in enumerate(response.get('results', []), 1):
                formatted_results.append(
                    f"[Result {i}]\n"
                    f"Title: {result.get('title', 'N/A')}\n"
                    f"Content: {result.get('content', 'N/A')}\n"
                    f"URL: {result.get('url', 'N/A')}\n"
                )
            
            if not formatted_results:
                return "No results found."
            
            return "\n".join(formatted_results)
        
        except Exception as e:
            return f"Search error: {str(e)}"


# Create singleton instance
web_search_tool = WebSearchTool()


def search_web(query: str) -> str:
    """
    Convenience function for web search.
    This is what the agent will actually call.
    """
    return web_search_tool.search(query)


# Test it
if __name__ == "__main__":
    # Test the search
    result = search_web("LangGraph latest features")
    print(result)