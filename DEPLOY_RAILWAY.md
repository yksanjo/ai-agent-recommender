# Railway Deployment Guide

## Prerequisites

1. Railway account: https://railway.app
2. GitHub repository (already set up ✅)

## Step 1: Install Railway CLI

```bash
npm install -g @railway/cli
```

## Step 2: Login to Railway

```bash
railway login
```

This will open your browser to authenticate.

## Step 3: Initialize Railway Project

```bash
cd /Users/yoshikondo/agent-recommender
railway init
```

When prompted:
- Select "Create a new project"
- Name it: `ai-agent-recommender` (or your preferred name)

## Step 4: Set Environment Variables

```bash
# Set OpenAI API key
railway variables set OPENAI_API_KEY=your_openai_api_key_here

# Optional: Set other variables
railway variables set OPENAI_MODEL=gpt-4-turbo-preview
railway variables set CHROMA_PERSIST_DIR=/tmp/embeddings
```

## Step 5: Deploy

```bash
railway up
```

This will:
1. Build your application
2. Deploy it to Railway
3. Give you a URL like: `https://ai-agent-recommender-production.up.railway.app`

## Step 6: Set Up Data

After first deployment, you need to initialize the data:

```bash
# Connect to the deployed service
railway run python -m src.cli.main setup
```

Or you can do this locally and upload the data directory.

## Step 7: Deploy Streamlit UI (Optional)

For the Streamlit UI, you have two options:

### Option A: Deploy as separate service on Railway

1. Create a new service in Railway dashboard
2. Use the same repo
3. Set start command: `streamlit run web/app.py --server.port=$PORT --server.address=0.0.0.0`
4. Set environment variable: `API_URL=https://your-backend-url.railway.app`

### Option B: Use Streamlit Cloud (Easier)

1. Go to https://share.streamlit.io
2. Connect your GitHub repo
3. Set:
   - Main file: `web/app.py`
   - Python version: 3.11
4. Add secrets:
   - `OPENAI_API_KEY`: your key
   - `API_URL`: your Railway backend URL

## Monitoring

View logs:
```bash
railway logs
```

View service status:
```bash
railway status
```

## Updating

To update your deployment:
```bash
git push  # Push to GitHub
railway up  # Or Railway will auto-deploy from GitHub
```

## Cost

- **Hobby Plan**: $5/month credit included
- **Pay-as-you-go**: ~$0.000463/GB RAM-hour after credit
- **Estimated**: $5-15/month for this app

## Troubleshooting

### Build fails
- Check Python version in `runtime.txt`
- Ensure all dependencies are in `requirements.txt`

### Environment variables not set
```bash
railway variables
```

### Service not starting
```bash
railway logs --tail 100
```

### Data not persisting
- ChromaDB data in `/tmp` will be lost on restart
- Consider using Railway volumes or external vector DB

