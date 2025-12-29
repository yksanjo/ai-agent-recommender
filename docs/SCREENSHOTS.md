# Screenshots Guide

## How to Add Screenshots

1. **Take screenshots of your application:**
   - Web UI (Streamlit interface)
   - CLI interface (terminal output)
   - API documentation (Swagger UI)

2. **Save screenshots to `docs/images/` directory:**
   ```bash
   docs/images/
   ├── web-ui-main.png
   ├── web-ui-search.png
   ├── web-ui-conversation.png
   ├── cli-interactive.png
   ├── cli-search.png
   └── api-docs.png
   ```

3. **Update README.md** with image references:
   ```markdown
   ## 🎨 Screenshots

   ### Web Interface
   ![Main Interface](docs/images/web-ui-main.png)
   *Main search interface with filters*

   ![Search Results](docs/images/web-ui-search.png)
   *Search results with recommendations*

   ![Conversation Mode](docs/images/web-ui-conversation.png)
   *AI agent conversation interface*

   ### CLI Interface
   ![Interactive Mode](docs/images/cli-interactive.png)
   *CLI interactive mode*

   ### API Documentation
   ![API Docs](docs/images/api-docs.png)
   *FastAPI Swagger documentation*
   ```

## Screenshot Tips

- **Resolution**: Use at least 1920x1080 for web screenshots
- **Format**: PNG for screenshots (better quality)
- **File Size**: Optimize images (use tools like TinyPNG)
- **Naming**: Use descriptive names (e.g., `web-ui-search-results.png`)

## Quick Screenshot Commands

### macOS
```bash
# Take screenshot of window
cmd + shift + 4, then space, then click window

# Save to docs/images/
mv ~/Desktop/Screen*.png docs/images/web-ui-main.png
```

### Linux
```bash
# Using scrot
scrot -s docs/images/web-ui-main.png
```

### Windows
```bash
# Use Snipping Tool or Win + Shift + S
```

