"""
FastAPI backend for the AI Agent Recommender.
"""
import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from src.agent.recommender_agent import create_agent
from src.rag.retriever import UseCaseRetriever

load_dotenv()

app = FastAPI(
    title="AI Agent Recommender API",
    description="API for recommending AI agent use cases from 500+ projects",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
agent = None
retriever = None


def get_agent():
    """Get or create agent instance."""
    global agent
    if agent is None:
        agent = create_agent()
    return agent


def get_retriever():
    """Get or create retriever instance."""
    global retriever
    if retriever is None:
        retriever = UseCaseRetriever()
        retriever.initialize()
    return retriever


# Request/Response models
class SearchRequest(BaseModel):
    query: str = Field(..., description="Search query for finding use cases")
    max_results: int = Field(5, ge=1, le=20, description="Maximum number of results")
    industry: Optional[str] = Field(None, description="Filter by industry")
    framework: Optional[str] = Field(None, description="Filter by framework")


class RecommendationResponse(BaseModel):
    use_case: str
    industry: str
    framework: str
    description: str
    github_link: str
    complexity: str
    relevance_score: float


class SearchResponse(BaseModel):
    query: str
    results: List[RecommendationResponse]
    total: int


class AgentQueryRequest(BaseModel):
    query: str = Field(..., description="Natural language query")
    conversation_history: Optional[List[Dict[str, str]]] = Field(None, description="Previous conversation messages")


class AgentQueryResponse(BaseModel):
    response: str
    recommendations: Optional[List[RecommendationResponse]] = None


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "AI Agent Recommender API",
        "version": "1.0.0",
        "endpoints": {
            "search": "/api/search",
            "agent_query": "/api/agent-query",
            "industries": "/api/industries",
            "frameworks": "/api/frameworks",
            "health": "/health"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/api/search", response_model=SearchResponse)
async def search_use_cases(request: SearchRequest):
    """
    Search for use cases using direct retrieval.
    """
    try:
        retriever = get_retriever()
        
        filters = {}
        if request.industry:
            filters['industry'] = request.industry
        if request.framework:
            filters['framework'] = request.framework
        
        results = retriever.retrieve(
            request.query,
            k=request.max_results,
            filters=filters
        )
        
        # Convert to response model
        recommendations = [
            RecommendationResponse(**result) for result in results
        ]
        
        return SearchResponse(
            query=request.query,
            results=recommendations,
            total=len(recommendations)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/agent-query", response_model=AgentQueryResponse)
async def agent_query(request: AgentQueryRequest):
    """
    Query the agent for intelligent recommendations.
    """
    try:
        agent = get_agent()
        
        # Convert conversation history if provided
        history = None
        if request.conversation_history:
            from langchain_core.messages import HumanMessage, AIMessage
            history = []
            for msg in request.conversation_history:
                if msg.get('role') == 'user':
                    history.append(HumanMessage(content=msg.get('content', '')))
                elif msg.get('role') == 'assistant':
                    history.append(AIMessage(content=msg.get('content', '')))
        
        response = agent.recommend(request.query, conversation_history=history)
        
        # Try to extract recommendations from response
        # This is a simple approach - in production, you might want more sophisticated parsing
        recommendations = None
        try:
            retriever = get_retriever()
            recs = retriever.retrieve(request.query, k=5)
            recommendations = [RecommendationResponse(**r) for r in recs]
        except:
            pass
        
        return AgentQueryResponse(
            response=response,
            recommendations=recommendations
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/industries")
async def get_industries():
    """Get list of all available industries."""
    try:
        retriever = get_retriever()
        industries = retriever.get_all_industries()
        return {"industries": industries, "total": len(industries)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/frameworks")
async def get_frameworks():
    """Get list of all available frameworks."""
    try:
        retriever = get_retriever()
        frameworks = retriever.get_all_frameworks()
        return {"frameworks": frameworks, "total": len(frameworks)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

