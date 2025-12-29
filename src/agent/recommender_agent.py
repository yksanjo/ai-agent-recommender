"""
LangGraph agent for recommending AI agent use cases.
"""
import os
import json
from typing import TypedDict, Annotated, Sequence, Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

from src.agent.tools import get_tools

load_dotenv()


class AgentState(TypedDict):
    """State for the recommender agent."""
    messages: Annotated[Sequence[BaseMessage], add_messages]


class RecommenderAgent:
    """LangGraph agent for recommending use cases."""
    
    def __init__(self, model_name: str = "gpt-4-turbo-preview", temperature: float = 0.7):
        self.model_name = model_name
        self.temperature = temperature
        self.llm = ChatOpenAI(model=model_name, temperature=temperature)
        self.tools = get_tools()
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph agent graph."""
        # Create the graph
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("agent", self._call_agent)
        workflow.add_node("tools", ToolNode(self.tools))
        
        # Set entry point
        workflow.set_entry_point("agent")
        
        # Add conditional edges
        workflow.add_conditional_edges(
            "agent",
            self._should_continue,
            {
                "continue": "tools",
                "end": END
            }
        )
        
        # Add edge from tools back to agent
        workflow.add_edge("tools", "agent")
        
        # Compile the graph
        return workflow.compile()
    
    def _call_agent(self, state: AgentState) -> AgentState:
        """Call the agent with the current state."""
        messages = state["messages"]
        
        # Add system message if not present
        if not messages or not isinstance(messages[0], SystemMessage):
            system_msg = SystemMessage(content=self._get_system_prompt())
            messages = [system_msg] + list(messages)
        
        response = self.llm_with_tools.invoke(messages)
        return {"messages": [response]}
    
    def _should_continue(self, state: AgentState) -> str:
        """Determine if we should continue or end."""
        messages = state["messages"]
        last_message = messages[-1]
        
        # If there are tool calls, continue to tools
        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            return "continue"
        return "end"
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the agent."""
        return """You are an AI Agent Recommender Assistant. Your role is to help users find the perfect AI agent use case from a database of 500+ projects.

When a user asks for recommendations:
1. Use the search_use_cases tool to find relevant use cases based on their query
2. If the user mentions a specific industry or framework, use those filters
3. Present the recommendations in a clear, helpful format
4. Include the use case name, industry, framework, description, and GitHub link
5. Explain why each recommendation is relevant to the user's needs

Be conversational, helpful, and provide context about why each recommendation might be useful.
If you need to see available options, use get_available_industries or get_available_frameworks tools."""
    
    def recommend(self, query: str, conversation_history: Optional[list] = None) -> str:
        """
        Get recommendations for a user query.
        
        Args:
            query: User's query/question
            conversation_history: Optional list of previous messages for context
        
        Returns:
            Agent's response with recommendations
        """
        # Build messages
        messages = []
        if conversation_history:
            messages.extend(conversation_history)
        
        messages.append(HumanMessage(content=query))
        
        # Run the graph
        config = {"recursion_limit": 50}
        result = self.graph.invoke({"messages": messages}, config=config)
        
        # Get the final response
        final_message = result["messages"][-1]
        
        if isinstance(final_message, AIMessage):
            return final_message.content
        else:
            return str(final_message)
    
    def format_recommendations(self, recommendations_json: str) -> str:
        """Format recommendations JSON into a readable string."""
        try:
            recommendations = json.loads(recommendations_json)
            if not recommendations:
                return "No recommendations found. Try refining your query."
            
            formatted = "Here are my recommendations:\n\n"
            for i, rec in enumerate(recommendations, 1):
                formatted += f"{i}. **{rec.get('use_case', 'Unknown')}**\n"
                formatted += f"   - Industry: {rec.get('industry', 'N/A')}\n"
                formatted += f"   - Framework: {rec.get('framework', 'Unknown')}\n"
                formatted += f"   - Complexity: {rec.get('complexity', 'Medium')}\n"
                formatted += f"   - Description: {rec.get('description', 'N/A')}\n"
                if rec.get('github_link'):
                    formatted += f"   - GitHub: {rec.get('github_link')}\n"
                formatted += f"   - Relevance: {rec.get('relevance_score', 0):.2%}\n\n"
            
            return formatted
        except json.JSONDecodeError:
            return recommendations_json


def create_agent(model_name: str = "gpt-4-turbo-preview", temperature: float = 0.7) -> RecommenderAgent:
    """Factory function to create a recommender agent."""
    return RecommenderAgent(model_name=model_name, temperature=temperature)

