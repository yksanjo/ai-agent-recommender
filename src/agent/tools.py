"""
Tools for the recommender agent.
"""
from typing import List, Dict, Optional
from langchain.tools import tool
from src.rag.retriever import UseCaseRetriever

# Global retriever instance
_retriever = None


def get_retriever() -> UseCaseRetriever:
    """Get or create retriever instance."""
    global _retriever
    if _retriever is None:
        _retriever = UseCaseRetriever()
        _retriever.initialize()
    return _retriever


@tool
def search_use_cases(query: str, max_results: int = 5, industry: Optional[str] = None, 
                     framework: Optional[str] = None) -> str:
    """
    Search for AI agent use cases based on a query.
    
    Args:
        query: Description of what the user is looking for
        max_results: Maximum number of results to return (default: 5)
        industry: Optional industry filter (e.g., "Healthcare", "Finance")
        framework: Optional framework filter (e.g., "CrewAI", "LangGraph")
    
    Returns:
        JSON string with recommended use cases
    """
    retriever = get_retriever()
    
    filters = {}
    if industry:
        filters['industry'] = industry
    if framework:
        filters['framework'] = framework
    
    results = retriever.retrieve(query, k=max_results, filters=filters)
    
    # Format as JSON string for the agent
    import json
    return json.dumps(results, indent=2)


@tool
def get_available_industries() -> str:
    """
    Get list of all available industries in the database.
    
    Returns:
        JSON string with list of industries
    """
    retriever = get_retriever()
    industries = retriever.get_all_industries()
    import json
    return json.dumps(industries, indent=2)


@tool
def get_available_frameworks() -> str:
    """
    Get list of all available frameworks in the database.
    
    Returns:
        JSON string with list of frameworks
    """
    retriever = get_retriever()
    frameworks = retriever.get_all_frameworks()
    import json
    return json.dumps(frameworks, indent=2)


def get_tools() -> List:
    """Get all tools for the agent."""
    return [
        search_use_cases,
        get_available_industries,
        get_available_frameworks
    ]

