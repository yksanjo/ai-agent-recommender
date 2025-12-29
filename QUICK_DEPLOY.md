# Quick Deploy to Railway

## Step 1: Login to Railway (Interactive)

You need to login interactively. Run this in your terminal:

```bash
railway login
```

This will open your browser. Log in with your Railway account (or create one at https://railway.app).

## Step 2: Run Setup Script

```bash
./setup_railway.sh
```

This will:
- Check Railway CLI
- Initialize project
- Set environment variables

## Step 3: Deploy

```bash
railway up
```

Or connect to GitHub for auto-deploy:
1. Go to https://railway.app/dashboard
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your `ai-agent-recommender` repo
5. Railway will auto-deploy on every push!

## Step 4: Get Your URL

After deployment, Railway will give you a URL like:
```
https://ai-agent-recommender-production.up.railway.app
```

## Step 5: Initialize Data (First Time)

After first deployment, initialize the data:

```bash
railway run python -m src.cli.main setup
```

## For Screenshots

1. **Option A: Use the mockup**
   ```bash
   open docs/images/web-ui-mockup.html
   # Take screenshot of the browser
   ```

2. **Option B: Run locally and screenshot**
   ```bash
   # Terminal 1
   uvicorn src.api.main:app --reload
   
   # Terminal 2
   streamlit run web/app.py
   
   # Then take screenshots of:
   # - http://localhost:8501 (Streamlit UI)
   # - http://localhost:8000/docs (API docs)
   ```

3. **Option C: Use helper script**
   ```bash
   ./scripts/take_screenshots.sh
   ```

Save screenshots to `docs/images/` and update README.md!

