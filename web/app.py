"""
Streamlit web interface for the AI Agent Recommender.
"""
import os
import sys
import json
import streamlit as st
from typing import List, Dict, Optional
import requests
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

load_dotenv()

# Page config
st.set_page_config(
    page_title="AI Agent Recommender",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .recommendation-card {
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #ddd;
        margin: 1rem 0;
        background-color: #f9f9f9;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

if 'recommendations' not in st.session_state:
    st.session_state.recommendations = []


def get_api_url():
    """Get API URL from environment or use default."""
    return os.getenv("API_URL", "http://localhost:8000")


def search_use_cases(query: str, max_results: int = 5, industry: Optional[str] = None, 
                    framework: Optional[str] = None) -> List[Dict]:
    """Search for use cases via API."""
    try:
        api_url = get_api_url()
        response = requests.post(
            f"{api_url}/api/search",
            json={
                "query": query,
                "max_results": max_results,
                "industry": industry,
                "framework": framework
            },
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {e}")
        return []


def agent_query(query: str, conversation_history: Optional[List] = None) -> Dict:
    """Query the agent via API."""
    try:
        api_url = get_api_url()
        response = requests.post(
            f"{api_url}/api/agent-query",
            json={
                "query": query,
                "conversation_history": conversation_history or []
            },
            timeout=60
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {e}")
        return {"response": "", "recommendations": []}


def get_industries() -> List[str]:
    """Get list of industries."""
    try:
        api_url = get_api_url()
        response = requests.get(f"{api_url}/api/industries", timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("industries", [])
    except:
        return []


def get_frameworks() -> List[str]:
    """Get list of frameworks."""
    try:
        api_url = get_api_url()
        response = requests.get(f"{api_url}/api/frameworks", timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("frameworks", [])
    except:
        return []


def display_recommendation(rec: Dict, index: int):
    """Display a single recommendation card."""
    with st.container():
        st.markdown(f"### {index}. {rec.get('use_case', 'Unknown')}")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"**Industry:** {rec.get('industry', 'N/A')}")
        with col2:
            st.markdown(f"**Framework:** {rec.get('framework', 'Unknown')}")
        with col3:
            st.markdown(f"**Relevance:** {rec.get('relevance_score', 0):.1%}")
        
        st.markdown(f"**Description:** {rec.get('description', 'N/A')}")
        
        github_link = rec.get('github_link', '')
        if github_link:
            st.markdown(f"**GitHub:** [{github_link}]({github_link})")
        
        st.divider()


def main():
    """Main Streamlit app."""
    # Header
    st.markdown('<div class="main-header">🤖 AI Agent Recommender</div>', unsafe_allow_html=True)
    st.markdown("### Discover the perfect AI agent use case from 500+ projects")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Mode selection
        mode = st.radio(
            "Search Mode",
            ["Direct Search", "AI Agent"],
            help="Direct Search: Fast keyword-based search\nAI Agent: Intelligent conversational search"
        )
        
        # Filters
        st.subheader("Filters")
        
        industries = get_industries()
        selected_industry = st.selectbox(
            "Industry",
            ["All"] + industries,
            index=0
        )
        
        frameworks = get_frameworks()
        selected_framework = st.selectbox(
            "Framework",
            ["All"] + frameworks,
            index=0
        )
        
        max_results = st.slider("Max Results", 1, 20, 5)
        
        # Export buttons
        if st.session_state.recommendations:
            st.subheader("Export")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.download_button(
                    label="📥 JSON",
                    data=json.dumps(st.session_state.recommendations, indent=2),
                    file_name="recommendations.json",
                    mime="application/json"
                )
            with col2:
                # CSV export
                import csv
                import io
                if st.session_state.recommendations:
                    output = io.StringIO()
                    fieldnames = st.session_state.recommendations[0].keys()
                    writer = csv.DictWriter(output, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(st.session_state.recommendations)
                    st.download_button(
                        label="📥 CSV",
                        data=output.getvalue(),
                        file_name="recommendations.csv",
                        mime="text/csv"
                    )
        
        # Clear conversation
        if st.button("🗑️ Clear History"):
            st.session_state.conversation_history = []
            st.session_state.recommendations = []
            st.rerun()
    
    # Main content area
    tab1, tab2 = st.tabs(["🔍 Search", "💬 Conversation"])
    
    with tab1:
        st.header("Search for AI Agent Use Cases")
        
        query = st.text_input(
            "Enter your query",
            placeholder="e.g., I need an agent for healthcare diagnostics"
        )
        
        col1, col2 = st.columns([1, 4])
        with col1:
            search_button = st.button("🔍 Search", type="primary", use_container_width=True)
        
        if search_button and query:
            with st.spinner("Searching..."):
                industry_filter = None if selected_industry == "All" else selected_industry
                framework_filter = None if selected_framework == "All" else selected_framework
                
                results = search_use_cases(
                    query,
                    max_results=max_results,
                    industry=industry_filter,
                    framework=framework_filter
                )
                
                st.session_state.recommendations = results
                
                if results:
                    st.success(f"Found {len(results)} recommendations!")
                    st.header("Recommendations")
                    
                    for i, rec in enumerate(results, 1):
                        display_recommendation(rec, i)
                else:
                    st.warning("No recommendations found. Try a different query.")
        
        elif st.session_state.recommendations:
            st.header("Previous Recommendations")
            for i, rec in enumerate(st.session_state.recommendations, 1):
                display_recommendation(rec, i)
    
    with tab2:
        st.header("Conversational AI Agent")
        st.markdown("Have a conversation with the AI agent to find the perfect use case!")
        
        # Display conversation history
        if st.session_state.conversation_history:
            st.subheader("Conversation History")
            for msg in st.session_state.conversation_history:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                
                if role == "user":
                    with st.chat_message("user"):
                        st.write(content)
                else:
                    with st.chat_message("assistant"):
                        st.markdown(content)
                        
                        # Show recommendations if available
                        if msg.get("recommendations"):
                            st.subheader("Recommended Use Cases")
                            for i, rec in enumerate(msg["recommendations"], 1):
                                display_recommendation(rec, i)
        
        # Chat input
        user_input = st.chat_input("Ask me about AI agent use cases...")
        
        if user_input:
            # Add user message to history
            st.session_state.conversation_history.append({
                "role": "user",
                "content": user_input
            })
            
            # Get agent response
            with st.spinner("Thinking..."):
                # Prepare conversation history for API
                api_history = [
                    {"role": msg["role"], "content": msg["content"]}
                    for msg in st.session_state.conversation_history[:-1]
                ]
                
                response_data = agent_query(user_input, conversation_history=api_history)
                
                # Add assistant response to history
                assistant_response = response_data.get("response", "")
                recommendations = response_data.get("recommendations", [])
                
                st.session_state.conversation_history.append({
                    "role": "assistant",
                    "content": assistant_response,
                    "recommendations": recommendations
                })
                
                st.rerun()


if __name__ == "__main__":
    main()

