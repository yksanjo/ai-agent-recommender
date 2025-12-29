"""
Enhanced Streamlit web interface with modern design and better UX.
"""
import os
import sys
import json
import streamlit as st
from typing import List, Dict, Optional
import requests
from dotenv import load_dotenv
import time

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

load_dotenv()

# Page config
st.set_page_config(
    page_title="AI Agent Advisor",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None
)

# Modern CSS styling
st.markdown("""
<style>
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom styling */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .main-container {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    }
    
    .header {
        text-align: center;
        padding: 2rem 0;
    }
    
    .header h1 {
        font-size: 3.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .header p {
        font-size: 1.2rem;
        color: #666;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 15px;
        margin: 1rem 0;
        animation: fadeIn 0.3s;
    }
    
    .chat-message.user {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 20%;
    }
    
    .chat-message.assistant {
        background: #f0f0f0;
        color: #333;
        margin-right: 20%;
    }
    
    .recommendation-card {
        background: white;
        border: 2px solid #e0e0e0;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    .recommendation-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        border-color: #667eea;
    }
    
    .suggestion-chip {
        display: inline-block;
        padding: 0.5rem 1rem;
        margin: 0.25rem;
        background: #f0f0f0;
        border-radius: 20px;
        cursor: pointer;
        transition: all 0.2s;
        border: 2px solid transparent;
    }
    
    .suggestion-chip:hover {
        background: #667eea;
        color: white;
        border-color: #667eea;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
    }
    
    .sidebar .sidebar-content {
        background: white;
        border-radius: 15px;
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'thread_id' not in st.session_state:
    st.session_state.thread_id = f"thread_{int(time.time())}"
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = []


def get_api_url():
    """Get API URL from environment or use default."""
    return os.getenv("API_URL", "http://localhost:8000")


def chat_with_agent(query: str, thread_id: str) -> Dict:
    """Send message to enhanced agent API."""
    try:
        api_url = get_api_url()
        response = requests.post(
            f"{api_url}/api/chat",
            json={
                "query": query,
                "thread_id": thread_id,
                "conversation_history": [
                    {"role": msg["role"], "content": msg["content"]}
                    for msg in st.session_state.messages
                ]
            },
            timeout=60
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {e}")
        return {
            "response": "I'm having trouble connecting. Please make sure the API server is running.",
            "recommendations": [],
            "suggestions": []
        }


def display_message(role: str, content: str):
    """Display a chat message with styling."""
    if role == "user":
        st.markdown(f"""
        <div class="chat-message user">
            <strong>You:</strong><br>
            {content}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message assistant">
            <strong>🤖 AI Agent Advisor:</strong><br>
            {content}
        </div>
        """, unsafe_allow_html=True)


def display_recommendation(rec: Dict, index: int):
    """Display a recommendation card."""
    st.markdown(f"""
    <div class="recommendation-card">
        <h3 style="color: #667eea; margin-top: 0;">{index}. {rec.get('use_case', 'Unknown')}</h3>
        <div style="display: flex; gap: 1rem; margin: 1rem 0;">
            <span style="background: #e8f0fe; padding: 0.25rem 0.75rem; border-radius: 10px; font-size: 0.9rem;">
                🏢 {rec.get('industry', 'N/A')}
            </span>
            <span style="background: #f3e5f5; padding: 0.25rem 0.75rem; border-radius: 10px; font-size: 0.9rem;">
                ⚙️ {rec.get('framework', 'Unknown')}
            </span>
            <span style="background: #e0f2f1; padding: 0.25rem 0.75rem; border-radius: 10px; font-size: 0.9rem;">
                📊 {rec.get('relevance_score', 0):.0%} match
            </span>
        </div>
        <p style="color: #666; line-height: 1.6;">{rec.get('description', 'N/A')}</p>
        {f'<a href="{rec.get("github_link")}" target="_blank" style="color: #667eea; text-decoration: none;">🔗 View on GitHub →</a>' if rec.get('github_link') else ''}
    </div>
    """, unsafe_allow_html=True)


def main():
    """Main application."""
    
    # Header
    st.markdown("""
    <div class="header">
        <h1>🤖 AI Agent Advisor</h1>
        <p>Your intelligent assistant for discovering, understanding, and building AI agents</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        
        # Mode selector
        mode = st.radio(
            "Mode",
            ["💬 Chat", "🔍 Quick Search"],
            help="Chat mode for conversations, Quick Search for fast results"
        )
        
        st.divider()
        
        # Filters (for quick search)
        if mode == "🔍 Quick Search":
            st.markdown("### Filters")
            industries = ["All"] + ["Healthcare", "Finance", "Education", "Retail", "Transportation"]
            selected_industry = st.selectbox("Industry", industries)
            
            frameworks = ["All"] + ["CrewAI", "LangGraph", "AutoGen", "Agno"]
            selected_framework = st.selectbox("Framework", frameworks)
        
        st.divider()
        
        # Actions
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.recommendations = []
            st.rerun()
        
        if st.session_state.recommendations:
            st.download_button(
                label="📥 Export Recommendations",
                data=json.dumps(st.session_state.recommendations, indent=2),
                file_name="recommendations.json",
                mime="application/json",
                use_container_width=True
            )
    
    # Main content
    if mode == "💬 Chat":
        # Chat interface
        st.markdown("### 💬 Conversation")
        
        # Display chat history
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.messages:
                display_message(message["role"], message["content"])
                
                # Show recommendations if available
                if message.get("recommendations"):
                    st.markdown("#### 📋 Recommendations")
                    for i, rec in enumerate(message["recommendations"], 1):
                        display_recommendation(rec, i)
        
        # Chat input
        user_input = st.chat_input("Ask me about AI agents, find use cases, or get help building your own agent...")
        
        if user_input:
            # Add user message
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Get agent response
            with st.spinner("🤔 Thinking..."):
                response_data = chat_with_agent(user_input, st.session_state.thread_id)
                
                # Add assistant response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response_data.get("response", ""),
                    "recommendations": response_data.get("recommendations", []),
                    "suggestions": response_data.get("suggestions", [])
                })
                
                # Update recommendations
                if response_data.get("recommendations"):
                    st.session_state.recommendations = response_data.get("recommendations")
            
            st.rerun()
        
        # Show suggestions if available
        if st.session_state.messages:
            last_message = st.session_state.messages[-1]
            if last_message.get("role") == "assistant" and last_message.get("suggestions"):
                st.markdown("#### 💡 Suggested Follow-ups")
                cols = st.columns(len(last_message["suggestions"]))
                for i, suggestion in enumerate(last_message["suggestions"]):
                    with cols[i]:
                        if st.button(suggestion, key=f"suggestion_{i}", use_container_width=True):
                            st.session_state.messages.append({"role": "user", "content": suggestion})
                            with st.spinner("🤔 Thinking..."):
                                response_data = chat_with_agent(suggestion, st.session_state.thread_id)
                                st.session_state.messages.append({
                                    "role": "assistant",
                                    "content": response_data.get("response", ""),
                                    "recommendations": response_data.get("recommendations", []),
                                    "suggestions": response_data.get("suggestions", [])
                                })
                            st.rerun()
    
    else:
        # Quick search mode
        st.markdown("### 🔍 Quick Search")
        
        query = st.text_input(
            "Search for AI agent use cases",
            placeholder="e.g., healthcare diagnostics, trading bot, customer service..."
        )
        
        if st.button("🔍 Search", use_container_width=True, type="primary") and query:
            with st.spinner("Searching..."):
                try:
                    api_url = get_api_url()
                    response = requests.post(
                        f"{api_url}/api/search",
                        json={
                            "query": query,
                            "max_results": 10,
                            "industry": selected_industry if selected_industry != "All" else None,
                            "framework": selected_framework if selected_framework != "All" else None
                        },
                        timeout=30
                    )
                    response.raise_for_status()
                    data = response.json()
                    results = data.get("results", [])
                    
                    st.session_state.recommendations = results
                    
                    if results:
                        st.success(f"Found {len(results)} recommendations!")
                        for i, rec in enumerate(results, 1):
                            display_recommendation(rec, i)
                    else:
                        st.warning("No results found. Try a different query.")
                except Exception as e:
                    st.error(f"Error: {e}")


if __name__ == "__main__":
    main()

