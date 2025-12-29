#!/usr/bin/env python3
"""
Generate placeholder/mockup screenshots for the README.
This creates simple HTML mockups that can be converted to images.
"""
from pathlib import Path

def create_web_ui_mockup():
    """Create HTML mockup of web UI."""
    html = """<!DOCTYPE html>
<html>
<head>
    <title>AI Agent Recommender - Web UI</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
        h1 { color: #1f77b4; text-align: center; }
        .search-box { padding: 15px; border: 2px solid #ddd; border-radius: 4px; width: 100%; font-size: 16px; margin: 20px 0; }
        .filters { display: flex; gap: 15px; margin: 20px 0; }
        .filter { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 4px; }
        .button { background: #1f77b4; color: white; padding: 12px 24px; border: none; border-radius: 4px; cursor: pointer; }
        .results { margin-top: 30px; }
        .result-card { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 4px; }
        .result-title { font-size: 18px; font-weight: bold; color: #1f77b4; }
        .result-meta { color: #666; font-size: 14px; margin: 5px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 AI Agent Recommender</h1>
        <p style="text-align: center; color: #666;">Discover the perfect AI agent use case from 500+ projects</p>
        
        <input type="text" class="search-box" placeholder="e.g., I need an agent for healthcare diagnostics" value="healthcare diagnostics agent">
        
        <div class="filters">
            <select class="filter">
                <option>All Industries</option>
                <option>Healthcare</option>
                <option>Finance</option>
            </select>
            <select class="filter">
                <option>All Frameworks</option>
                <option>CrewAI</option>
                <option>LangGraph</option>
            </select>
            <button class="button">🔍 Search</button>
        </div>
        
        <div class="results">
            <h2>Recommendations</h2>
            <div class="result-card">
                <div class="result-title">HIA (Health Insights Agent)</div>
                <div class="result-meta">Industry: Healthcare | Framework: LangGraph | Relevance: 95%</div>
                <p>Analyses medical reports and provide health insights.</p>
            </div>
            <div class="result-card">
                <div class="result-title">AI Health Assistant</div>
                <div class="result-meta">Industry: Healthcare | Framework: CrewAI | Relevance: 88%</div>
                <p>Diagnoses and monitors diseases using patient data.</p>
            </div>
        </div>
    </div>
</body>
</html>
"""
    output_path = Path("docs/images/web-ui-mockup.html")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html)
    print(f"✅ Created mockup: {output_path}")
    print("   Open in browser and take a screenshot!")

if __name__ == "__main__":
    create_web_ui_mockup()

