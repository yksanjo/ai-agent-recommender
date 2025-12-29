# 🤖 AI Agent Advisor

An **intelligent, agentic chatbot** that helps you discover, understand, and build AI agents from 500+ projects. This isn't just a recommender—it's a sophisticated AI advisor that can guide you through the entire journey of working with AI agents.

> **Note**: This project is built on top of the [500-AI-Agents-Projects](https://github.com/ashishpatel26/500-AI-Agents-Projects) repository. The original repository contains the curated list of use cases, while this project provides an intelligent, conversational advisor to help you discover, understand, and build agents.

## ✨ What Makes This Special

- 🧠 **Agentic Intelligence**: Not just search—it plans, reasons, and adapts to your needs
- 💬 **Conversational**: Natural chat interface that understands context and intent
- 🎯 **Multi-Modal**: Can help you discover agents, understand concepts, or build your own
- 🎨 **Beautiful UI**: Modern, gradient-based design with smooth animations
- 🔄 **Context-Aware**: Remembers conversation history and provides relevant follow-ups

## 🎨 Screenshots

> **Note**: Screenshots coming soon! See [docs/SCREENSHOTS.md](docs/SCREENSHOTS.md) for instructions on adding screenshots.

<!-- 
Once you have screenshots, uncomment and update these:

### Web Interface
![Main Interface](docs/images/web-ui-main.png)
*Main search interface with filters*

![Search Results](docs/images/web-ui-search.png)
*Search results with recommendations*

![Conversation Mode](docs/images/web-ui-conversation.png)
*AI agent conversation interface*

### CLI Interface
![Interactive Mode](docs/images/cli-interactive.png)
*CLI interactive mode with rich formatting*

### API Documentation
![API Docs](docs/images/api-docs.png)
*FastAPI Swagger documentation*
-->

## 🚀 Features

### Core Capabilities
- 🧠 **Enhanced Agentic Reasoning**: Advanced LangGraph agent with planning, reflection, and adaptive responses
- 💬 **Intelligent Chatbot**: Conversational interface that understands intent and provides contextual help
- 🔍 **Semantic Search**: Vector-based search across 500+ use cases with relevance scoring
- 🎯 **Multi-Purpose Assistant**: 
  - **Discover** existing agent use cases
  - **Understand** AI agent concepts and frameworks
  - **Build** your own agents with step-by-step guidance
- 🎨 **Modern UI**: Beautiful gradient design with smooth animations and responsive layout
- 💡 **Smart Suggestions**: Proactive follow-up questions and recommendations
- 🔄 **Context Memory**: Maintains conversation history across sessions

### Interfaces
- 🌐 **Enhanced Web UI**: Modern Streamlit interface with chat and quick search modes
- 💻 **CLI Interface**: Command-line tool for power users
- 🔌 **REST API**: Full API for integration with other applications

## Installation

### Quick Setup (Recommended)

```bash
# Run the setup script
./setup.sh
```

### Manual Setup

1. Clone this repository:
```bash
git clone <your-repo-url>
cd agent-recommender
```

2. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

5. Initialize the system:
```bash
python -m src.cli.main setup
```

This will:
- Scrape use cases from the repository
- Process and clean the data
- Build the vector store with embeddings

## Usage

### CLI Interface

**Interactive mode (recommended):**
```bash
python -m src.cli.main interactive
```

**Direct search:**
```bash
python -m src.cli.main search -q "I need an agent for healthcare diagnostics"
```

**With filters:**
```bash
python -m src.cli.main search -q "trading bot" -i "Finance" -f "LangGraph" --max-results 10
```

**List available options:**
```bash
python -m src.cli.main industries
python -m src.cli.main frameworks
```

**Export results:**
```bash
python -m src.cli.main export -q "customer service" --export-format json
```

### Web Interface (Enhanced)

1. **Start the API server** (required):
```bash
uvicorn src.api.main:app --reload
```

2. **Start the enhanced Streamlit app** (in another terminal):
```bash
streamlit run web/enhanced_app.py
```

3. Open your browser to `http://localhost:8501`

**New Features:**
- 💬 **Chat Mode**: Conversational interface with the enhanced agent
- 🔍 **Quick Search**: Fast search with filters
- 💡 **Smart Suggestions**: Follow-up questions appear automatically
- 🎨 **Modern Design**: Beautiful gradient UI with animations

### API Server

```bash
uvicorn src.api.main:app --reload
```

API documentation available at `http://localhost:8000/docs`

**Example API call:**
```bash
curl -X POST "http://localhost:8000/api/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "healthcare agent", "max_results": 5}'
```

## Project Structure

```
agent-recommender/
├── data/
│   ├── use_cases.json          # Parsed repository data
│   └── embeddings/             # Vector store
├── src/
│   ├── agent/                  # LangGraph agent implementation
│   ├── data/                   # Data scraping and processing
│   ├── rag/                    # RAG system
│   ├── cli/                    # CLI interface
│   └── api/                    # FastAPI backend
├── web/
│   └── app.py                  # Streamlit frontend
└── requirements.txt
```

## Deployment

For deployment options and cost analysis, see [DEPLOYMENT.md](DEPLOYMENT.md).

**Quick Summary:**
- **Free Tier**: $0/month (Render + Streamlit Cloud) + OpenAI costs
- **Production**: $10-20/month (Railway/Render) + OpenAI costs
- **Vercel**: Not recommended without refactoring (see deployment guide)

## License

MIT

