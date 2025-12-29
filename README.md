# AI Agent Recommender System

An intelligent recommender agent that helps users discover the perfect AI agent use case from the [500+ AI Agents Projects](https://github.com/ashishpatel26/500-AI-Agents-Projects) repository.

> **Note**: This project is built on top of the [500-AI-Agents-Projects](https://github.com/ashishpatel26/500-AI-Agents-Projects) repository. The original repository contains the curated list of use cases, while this project provides an intelligent recommender system to help users discover relevant agents.

## Features

- 🤖 **Intelligent Recommendations**: Uses LangGraph and RAG to understand your needs and recommend relevant AI agent projects
- 🔍 **Semantic Search**: Vector-based search across 500+ use cases
- 💻 **CLI Interface**: Command-line tool for quick queries
- 🌐 **Web Interface**: User-friendly web UI built with Streamlit
- 🎯 **Multi-turn Conversations**: Context-aware recommendations
- 🔧 **Framework Filtering**: Filter by CrewAI, AutoGen, LangGraph, etc.

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

### Web Interface

1. **Start the API server** (required):
```bash
uvicorn src.api.main:app --reload
```

2. **Start the Streamlit app** (in another terminal):
```bash
streamlit run web/app.py
```

3. Open your browser to `http://localhost:8501`

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

## License

MIT

