# Quick Start Guide

## Prerequisites

- Python 3.8+
- OpenAI API key

## Installation

1. **Clone and navigate to the project:**
```bash
cd agent-recommender
```

2. **Run the setup script:**
```bash
./setup.sh
```

Or manually:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# Initialize data
python -m src.cli.main setup
```

## Usage

### CLI Interface

**Interactive mode:**
```bash
python -m src.cli.main interactive
```

**Direct search:**
```bash
python -m src.cli.main search -q "healthcare diagnostics agent"
```

**With filters:**
```bash
python -m src.cli.main search -q "trading bot" -i "Finance" -f "LangGraph"
```

**List available options:**
```bash
python -m src.cli.main industries
python -m src.cli.main frameworks
```

**Export results:**
```bash
python -m src.cli.main export -q "customer service" --export-format json --export-path results.json
```

### Web Interface

1. **Start the API server** (in one terminal):
```bash
uvicorn src.api.main:app --reload
```

2. **Start the Streamlit app** (in another terminal):
```bash
streamlit run web/app.py
```

3. Open your browser to `http://localhost:8501`

### API Usage

Start the API server:
```bash
uvicorn src.api.main:app --reload
```

API documentation: `http://localhost:8000/docs`

**Example API call:**
```bash
curl -X POST "http://localhost:8000/api/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "healthcare agent",
    "max_results": 5,
    "industry": "Healthcare"
  }'
```

## Troubleshooting

### "OPENAI_API_KEY not found"
- Make sure you've created a `.env` file with your API key
- Check that `python-dotenv` is installed

### "No module named 'src'"
- Make sure you're running commands from the project root directory
- Activate your virtual environment

### Vector store errors
- Run `python -m src.cli.main setup` to rebuild the vector store
- Check that `data/use_cases.json` exists

## Next Steps

- Explore the code in `src/` directory
- Customize the agent prompts in `src/agent/recommender_agent.py`
- Add your own use cases to the database
- Deploy the API to a cloud service

