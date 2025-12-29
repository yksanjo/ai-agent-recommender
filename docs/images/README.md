# Screenshots Directory

Place your application screenshots here.

## Required Screenshots

1. **web-ui-main.png** - Main Streamlit interface
2. **web-ui-search.png** - Search results page
3. **web-ui-conversation.png** - Conversation mode with AI agent
4. **cli-interactive.png** - CLI interactive mode
5. **api-docs.png** - FastAPI Swagger documentation

## How to Take Screenshots

1. Start the API:
   ```bash
   uvicorn src.api.main:app --reload
   ```

2. Start the Streamlit UI:
   ```bash
   streamlit run web/app.py
   ```

3. Use the helper script:
   ```bash
   ./scripts/take_screenshots.sh
   ```

4. Or manually:
   - Open http://localhost:8501 (Streamlit)
   - Open http://localhost:8000/docs (API docs)
   - Take screenshots and save to this directory

## Image Requirements

- Format: PNG
- Recommended size: 1920x1080 or larger
- Optimize: Use tools like TinyPNG before committing

