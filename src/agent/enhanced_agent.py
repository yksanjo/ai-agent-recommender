"""
Enhanced LangGraph agent with better reasoning, planning, and agentic capabilities.
This agent can help users understand, discover, and even build AI agents.
"""
import os
import json
from typing import TypedDict, Annotated, Sequence, Optional, List, Dict
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langgraph.graph.message import add_messages
try:
    from langgraph.checkpoint.memory import MemorySaver
except ImportError:
    # Fallback for older versions
    MemorySaver = None
from dotenv import load_dotenv

from src.agent.tools import get_tools

load_dotenv()


class AgentState(TypedDict):
    """Enhanced state for the agentic recommender."""
    messages: Annotated[Sequence[BaseMessage], add_messages]
    user_context: Dict  # Store user preferences, history, etc.
    current_plan: Optional[str]  # Current plan if user wants to build an agent


class EnhancedRecommenderAgent:
    """
    Enhanced agentic recommender that can:
    - Recommend AI agent use cases
    - Help users understand agents
    - Help users plan and build their own agents
    - Provide detailed explanations and guidance
    """
    
    def __init__(self, model_name: str = "gpt-4-turbo-preview", temperature: float = 0.7):
        self.model_name = model_name
        self.temperature = temperature
        self.llm = ChatOpenAI(model=model_name, temperature=temperature)
        self.tools = get_tools()
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        self.memory = MemorySaver() if MemorySaver else None
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build an enhanced LangGraph agent with planning capabilities."""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("planner", self._plan)
        workflow.add_node("agent", self._call_agent)
        workflow.add_node("tools", ToolNode(self.tools))
        workflow.add_node("reflector", self._reflect)
        
        # Set entry point
        workflow.set_entry_point("planner")
        
        # Planning flow
        workflow.add_conditional_edges(
            "planner",
            self._should_search_or_build,
            {
                "search": "agent",
                "build": "agent",
                "direct": "agent"
            }
        )
        
        # Agent flow
        workflow.add_conditional_edges(
            "agent",
            self._should_continue,
            {
                "continue": "tools",
                "reflect": "reflector",
                "end": END
            }
        )
        
        # Tools flow
        workflow.add_edge("tools", "agent")
        
        # Reflection flow
        workflow.add_conditional_edges(
            "reflector",
            lambda x: "agent" if x.get("messages", []) else "end",
            {
                "agent": "agent",
                "end": END
            }
        )
        
        if self.memory:
            return workflow.compile(checkpointer=self.memory)
        else:
            return workflow.compile()
    
    def _plan(self, state: AgentState) -> AgentState:
        """Plan the approach based on user query."""
        messages = state.get("messages", [])
        if not messages:
            return state
        
        last_message = messages[-1]
        query = last_message.content if hasattr(last_message, 'content') else str(last_message)
        
        # Analyze query intent
        planning_prompt = f"""Analyze this user query and determine the best approach:

Query: {query}

Determine if the user wants to:
1. SEARCH - Find existing agent use cases
2. BUILD - Get help building/planning their own agent
3. UNDERSTAND - Learn about agents, frameworks, concepts
4. DIRECT - Simple question that can be answered directly

Respond with just one word: SEARCH, BUILD, UNDERSTAND, or DIRECT"""
        
        plan_msg = self.llm.invoke([HumanMessage(content=planning_prompt)])
        plan_type = plan_msg.content.strip().upper()
        
        # Update state with plan
        new_state = state.copy()
        new_state["current_plan"] = plan_type
        
        return new_state
    
    def _should_search_or_build(self, state: AgentState) -> str:
        """Determine next step based on plan."""
        plan = state.get("current_plan", "DIRECT")
        
        if "SEARCH" in plan:
            return "search"
        elif "BUILD" in plan:
            return "build"
        else:
            return "direct"
    
    def _call_agent(self, state: AgentState) -> AgentState:
        """Call the agent with enhanced reasoning."""
        messages = state.get("messages", [])
        plan = state.get("current_plan", "DIRECT")
        
        # Build enhanced system prompt based on plan
        system_prompt = self._get_enhanced_system_prompt(plan)
        
        # Add system message
        if not messages or not isinstance(messages[0], SystemMessage):
            messages = [SystemMessage(content=system_prompt)] + list(messages)
        else:
            messages = [SystemMessage(content=system_prompt)] + messages[1:]
        
        response = self.llm_with_tools.invoke(messages)
        return {"messages": [response]}
    
    def _should_continue(self, state: AgentState) -> str:
        """Determine if we should continue, reflect, or end."""
        messages = state.get("messages", [])
        if not messages:
            return "end"
        
        last_message = messages[-1]
        
        # If there are tool calls, continue to tools
        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            return "continue"
        
        # Check if we should reflect on the response
        if isinstance(last_message, AIMessage):
            content = last_message.content.lower()
            # If response seems incomplete or needs refinement
            if any(phrase in content for phrase in ["let me", "i'll", "i can help"]):
                return "reflect"
        
        return "end"
    
    def _reflect(self, state: AgentState) -> AgentState:
        """Reflect on the conversation and improve response."""
        messages = state.get("messages", [])
        
        reflection_prompt = """Review the conversation so far. Is the response complete and helpful?
        If not, suggest improvements or additional information needed."""
        
        reflection = self.llm.invoke([
            SystemMessage(content="You are a helpful assistant reviewing conversation quality."),
            *messages[-3:],  # Last few messages
            HumanMessage(content=reflection_prompt)
        ])
        
        # Add reflection as a message to continue the conversation
        return {"messages": [reflection]}
    
    def _get_enhanced_system_prompt(self, plan_type: str = "DIRECT") -> str:
        """Get enhanced system prompt based on plan type."""
        
        base_prompt = """You are an advanced AI Agent Advisor - a sophisticated assistant that helps users discover, understand, and build AI agents.

Your capabilities:
1. **Discovery**: Find the perfect AI agent use cases from 500+ projects
2. **Education**: Explain AI agent concepts, frameworks, and best practices
3. **Planning**: Help users plan and design their own AI agents
4. **Guidance**: Provide step-by-step instructions and recommendations

Be conversational, insightful, and proactive. Ask clarifying questions when needed."""
        
        if plan_type == "SEARCH":
            return base_prompt + """

When helping users find agents:
- Use search_use_cases tool to find relevant projects
- Consider industry, framework, and complexity preferences
- Explain WHY each recommendation fits their needs
- Suggest related or alternative options
- Provide actionable next steps"""
        
        elif plan_type == "BUILD":
            return base_prompt + """

When helping users build agents:
- Understand their use case and requirements
- Recommend appropriate frameworks (CrewAI, LangGraph, AutoGen, etc.)
- Suggest architecture and design patterns
- Provide implementation guidance
- Reference similar existing projects for inspiration
- Break down complex tasks into steps"""
        
        elif plan_type == "UNDERSTAND":
            return base_prompt + """

When explaining concepts:
- Use clear, accessible language
- Provide examples and analogies
- Compare different frameworks and approaches
- Explain when to use what
- Link to relevant use cases for context"""
        
        else:
            return base_prompt + """
Answer questions directly and helpfully. If the question is about finding or building agents, guide the user appropriately."""
    
    def chat(self, query: str, thread_id: str = "default", 
             conversation_history: Optional[List] = None) -> Dict:
        """
        Enhanced chat interface that maintains context and provides rich responses.
        
        Returns:
            Dict with 'response', 'recommendations', 'suggestions', 'plan'
        """
        # Build messages
        messages = []
        if conversation_history:
            for msg in conversation_history:
                if msg.get("role") == "user":
                    messages.append(HumanMessage(content=msg.get("content", "")))
                elif msg.get("role") == "assistant":
                    messages.append(AIMessage(content=msg.get("content", "")))
        
        messages.append(HumanMessage(content=query))
        
        # Run the graph
        config = {"recursion_limit": 100}
        if self.memory:
            config["configurable"] = {"thread_id": thread_id}
        
        result = self.graph.invoke(
            {"messages": messages, "user_context": {}, "current_plan": None},
            config=config
        )
        
        # Extract response
        final_messages = result.get("messages", [])
        if not final_messages:
            return {
                "response": "I apologize, but I couldn't generate a response. Please try again.",
                "recommendations": [],
                "suggestions": [],
                "plan": None
            }
        
        # Get the last AI message
        response_text = ""
        recommendations = []
        for msg in reversed(final_messages):
            if isinstance(msg, AIMessage):
                response_text = msg.content
                break
        
        # Try to extract recommendations from tool calls
        for msg in final_messages:
            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                for tool_call in msg.tool_calls:
                    if tool_call.get('name') == 'search_use_cases':
                        # Extract results if available
                        pass
        
        # Generate follow-up suggestions
        suggestions = self._generate_suggestions(query, response_text)
        
        return {
            "response": response_text,
            "recommendations": recommendations,
            "suggestions": suggestions,
            "plan": result.get("current_plan")
        }
    
    def _generate_suggestions(self, query: str, response: str) -> List[str]:
        """Generate helpful follow-up suggestions."""
        prompt = f"""Based on this conversation:
Query: {query}
Response: {response[:200]}...

Generate 3-4 helpful follow-up questions or actions the user might want to take.
Return as a JSON array of strings."""
        
        try:
            suggestions_msg = self.llm.invoke([HumanMessage(content=prompt)])
            suggestions = json.loads(suggestions_msg.content)
            if isinstance(suggestions, list):
                return suggestions[:4]
        except:
            pass
        
        # Default suggestions
        return [
            "Show me more examples",
            "Help me build a similar agent",
            "Explain the framework used",
            "What are the key features?"
        ]


def create_enhanced_agent(model_name: str = "gpt-4-turbo-preview", 
                          temperature: float = 0.7) -> EnhancedRecommenderAgent:
    """Factory function to create an enhanced recommender agent."""
    return EnhancedRecommenderAgent(model_name=model_name, temperature=temperature)

