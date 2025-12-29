# Deployment Guide

## Deployment Architecture

This project consists of three main components:

1. **FastAPI Backend** - REST API server
2. **Streamlit Web UI** - Frontend interface
3. **Vector Store** - ChromaDB with embeddings

## Deployment Options & Costs

### Option 1: Vercel (Frontend Only) + Separate Backend

**Vercel Limitations:**
- Vercel is optimized for Next.js, React, and static sites
- Streamlit apps are not natively supported on Vercel
- FastAPI backend cannot run on Vercel (needs serverless functions refactor)

**Cost:** 
- **Vercel Hobby (Free)**: $0/month
  - 100GB bandwidth
  - Unlimited deployments
  - Perfect for static sites/Next.js apps
  
- **Vercel Pro**: $20/month
  - 1TB bandwidth
  - Team features

**What you CAN deploy on Vercel:**
- A React/Next.js frontend that calls your API
- Would require refactoring the Streamlit UI to React

**Recommended Architecture:**
```
Vercel (React Frontend) → Railway/Render Backend → OpenAI API
```

### Option 2: Railway (Recommended for Full Stack)

**Railway Pricing:**
- **Hobby Plan**: $5/month
  - $5 credit included
  - Pay-as-you-go after ($0.000463/GB RAM-hour)
  - Perfect for small projects

- **Pro Plan**: $20/month
  - $20 credit included
  - Better for production

**What you can deploy:**
- FastAPI backend ✅
- Streamlit app ✅
- ChromaDB (or use external vector DB)

**Estimated Monthly Cost:**
- Backend: ~$5-10/month (depending on usage)
- Database: Included or +$5-10 for external DB
- **Total: ~$10-20/month**

### Option 3: Render

**Render Pricing:**
- **Free Tier**: $0/month
  - Sleeps after 15 min inactivity
  - Good for demos/testing

- **Starter Plan**: $7/month per service
  - Always on
  - 512MB RAM

**What you can deploy:**
- FastAPI backend ✅
- Streamlit app ✅

**Estimated Monthly Cost:**
- Backend: $7/month
- Frontend: $7/month
- **Total: ~$14/month**

### Option 4: Fly.io

**Fly.io Pricing:**
- **Free Tier**: $0/month
  - 3 shared VMs
  - 3GB persistent volumes

- **Pay-as-you-go**: After free tier
  - Very affordable

**What you can deploy:**
- FastAPI backend ✅
- Streamlit app ✅

**Estimated Monthly Cost:**
- **Free tier is generous**: $0-5/month for small usage

### Option 5: Streamlit Cloud (For UI Only)

**Streamlit Cloud Pricing:**
- **Free Tier**: $0/month
  - Public apps only
  - Good for demos

- **Team Plan**: $20/month per user
  - Private apps
  - Better performance

**What you can deploy:**
- Streamlit app only ✅
- Backend would need separate hosting

## Additional Costs

### OpenAI API Costs
- **Embeddings**: ~$0.0001 per 1K tokens
- **GPT-4**: ~$0.03 per 1K input tokens, $0.06 per 1K output tokens
- **Estimated**: $5-50/month depending on usage

### Vector Database (if external)
- **Pinecone**: Free tier available, then $70/month
- **Weaviate Cloud**: Free tier available
- **ChromaDB**: Self-hosted (free) or use embedded version

## Recommended Deployment Strategy

### For Production (Best Performance):
```
1. Railway/Render for FastAPI backend
2. Streamlit Cloud for UI (or Railway)
3. ChromaDB embedded (or external vector DB)
4. Total: ~$15-25/month + OpenAI costs
```

### For Demo/Free Tier:
```
1. Render free tier for backend (sleeps when inactive)
2. Streamlit Cloud free tier for UI
3. ChromaDB embedded
4. Total: $0/month + OpenAI costs (~$5-10/month)
```

## Deployment Steps

### Deploy Backend to Railway

1. Install Railway CLI:
```bash
npm i -g @railway/cli
railway login
```

2. Initialize project:
```bash
cd /path/to/agent-recommender
railway init
```

3. Set environment variables:
```bash
railway variables set OPENAI_API_KEY=your_key
```

4. Deploy:
```bash
railway up
```

### Deploy Streamlit to Streamlit Cloud

1. Push code to GitHub (already done ✅)
2. Go to https://share.streamlit.io
3. Connect your GitHub repo
4. Set config:
   - Main file: `web/app.py`
   - Python version: 3.9+
5. Add secrets:
   - `OPENAI_API_KEY`: your key
   - `API_URL`: your Railway backend URL

### Alternative: Deploy Everything to Railway

1. Create `Procfile`:
```
web: streamlit run web/app.py --server.port=$PORT --server.address=0.0.0.0
api: uvicorn src.api.main:app --host 0.0.0.0 --port $PORT
```

2. Deploy both services to Railway

## Cost Summary

| Option | Monthly Cost | Best For |
|--------|-------------|----------|
| **Free Tier (Demo)** | $0 + OpenAI (~$5-10) | Testing, demos |
| **Railway** | $10-20 + OpenAI | Production |
| **Render** | $14 + OpenAI | Production |
| **Fly.io** | $0-5 + OpenAI | Cost-effective |
| **Vercel + Backend** | $0-20 + Backend ($10-20) | If you refactor to React |

**Total Estimated Cost: $5-30/month + OpenAI API usage**

## Notes

- Vercel is not ideal for this project without significant refactoring
- Railway or Render are the easiest options for full-stack deployment
- Streamlit Cloud is perfect for the UI component
- OpenAI API costs will be the main variable expense

