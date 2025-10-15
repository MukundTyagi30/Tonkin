# 🚀 Full-Stack Deployment Guide
## Tonkin Knowledge Finder - React Frontend + Python Backend

This guide will walk you through deploying both the React frontend and Python FastAPI backend to production.

---

## 📋 Architecture Overview

```
┌─────────────────────┐          ┌─────────────────────┐
│   React Frontend    │  ────►   │   FastAPI Backend   │
│   (Netlify/Vercel)  │   API    │   (Railway/Render)  │
│   Port 3000 (dev)   │          │   Port 8000         │
└─────────────────────┘          └─────────────────────┘
         │                                  │
         │                                  ▼
         │                         ┌──────────────────┐
         │                         │   Database       │
         └─────────────────────────│   SQLite/Vector  │
                                   └──────────────────┘
```

**What you have:**
✅ FastAPI backend (`api.py`) - Wraps your search engine  
✅ React frontend (`/frontend/`) - Modern UI with real-time search  
✅ CORS configured - Frontend can talk to backend  
✅ Environment config - Easy to switch between dev/prod  

---

## 🎯 Quick Start (Recommended Path)

### Step 1: Deploy Backend to Railway (5 minutes)

1. **Create Railway account**: https://railway.app
2. **Click "New Project"** → **"Deploy from GitHub repo"**
3. **Connect your GitHub** and select this repository
4. **Configure**:
   - Root directory: `/` (leave blank)
   - Start command: `uvicorn api:app --host 0.0.0.0 --port $PORT`
5. **Add environment variables** (if needed):
   - No special env vars required for basic setup
6. **Deploy** - Railway will:
   - Install dependencies from `requirements.txt`
   - Start your FastAPI server
   - Give you a URL like: `https://your-app.railway.app`

7. **Test the API**:
   ```bash
   curl https://your-app.railway.app/health
   ```
   You should see: `{"status":"healthy",...}`

### Step 2: Deploy Frontend to Netlify (3 minutes)

**Option A: Drag & Drop (Easiest)**

1. Build the React app:
   ```bash
   cd frontend
   npm install
   npm run build
   ```

2. Go to: https://app.netlify.com/drop

3. Drag the `frontend/build/` folder onto the page

4. **Configure environment variable**:
   - Go to: Site settings → Environment variables
   - Add: `REACT_APP_API_URL` = `https://your-app.railway.app`
   - (Use your Railway URL from Step 1)

5. **Rebuild**:
   - Go to: Deploys → Trigger deploy

**Option B: GitHub Auto-Deploy**

1. Push your code to GitHub (if not already)

2. Go to: https://app.netlify.com

3. Click: **"Add new site"** → **"Import an existing project"**

4. Choose: **GitHub** → Select your repo

5. **Build settings**:
   - Base directory: `frontend`
   - Build command: `npm run build`
   - Publish directory: `frontend/build`

6. **Environment variables**:
   - Add: `REACT_APP_API_URL` = `https://your-app.railway.app`

7. **Deploy**

8. **Get your URL**: `https://your-app-name.netlify.app`

### Step 3: Update CORS (Important!)

Update your backend's CORS settings in `api.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-app-name.netlify.app",  # Add your Netlify URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Redeploy the backend after this change.

### Step 4: Test End-to-End

1. Open your Netlify URL: `https://your-app-name.netlify.app`
2. Try a search query (e.g., "stormwater management")
3. Results should load from your Railway backend
4. Check browser console (F12) for any errors

---

## 🎨 Alternative Deployment Options

### Backend Options

#### Option 1: Railway (Recommended) ⭐
- **Pros**: Easy setup, free tier, auto-scaling
- **Deploy**: See Step 1 above
- **Cost**: $5/month after free tier

#### Option 2: Render.com
1. Go to: https://render.com
2. Create new **Web Service**
3. Connect GitHub repo
4. Build command: `pip install -r requirements.txt`
5. Start command: `uvicorn api:app --host 0.0.0.0 --port $PORT`
6. **Cost**: Free tier available (with limitations)

#### Option 3: Heroku
1. Install Heroku CLI
2. ```bash
   heroku create tonkin-knowledge-api
   git push heroku main
   ```
3. **Note**: Heroku no longer has a free tier

#### Option 4: AWS/GCP/Azure
- More complex, but full control
- Use EC2, Cloud Run, or App Service
- See cloud-specific documentation

### Frontend Options

#### Option 1: Netlify (Recommended) ⭐
- See Step 2 above
- **Cost**: Free for most use cases

#### Option 2: Vercel
1. Install Vercel CLI: `npm install -g vercel`
2. ```bash
   cd frontend
   vercel
   ```
3. Follow prompts
4. Add environment variable: `REACT_APP_API_URL`
5. **Cost**: Free for personal projects

#### Option 3: GitHub Pages
1. Install: `npm install --save-dev gh-pages`
2. Update `frontend/package.json`:
   ```json
   "homepage": "https://yourusername.github.io/tonkin-knowledge-finder",
   "scripts": {
     "predeploy": "npm run build",
     "deploy": "gh-pages -d build"
   }
   ```
3. Run: `npm run deploy`
4. **Limitation**: Static hosting only, need separate backend

#### Option 4: AWS S3 + CloudFront
```bash
cd frontend
npm run build
aws s3 sync build/ s3://your-bucket-name --acl public-read
```
Then configure CloudFront for CDN.

---

## 🔧 Local Development Setup

### Run Backend Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Start FastAPI server
uvicorn api:app --reload --port 8000

# Test
curl http://localhost:8000/health
```

Backend will be at: `http://localhost:8000`
API docs at: `http://localhost:8000/docs`

### Run Frontend Locally

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Frontend will be at: `http://localhost:3000`

**Note**: Make sure `frontend/src/config.js` has:
```javascript
export const API_URL = 'http://localhost:8000';
export const USE_SAMPLE_DATA = false;  // Set to true for demo without backend
```

---

## 🔐 Environment Variables

### Backend (Railway/Render)

No special environment variables required for basic setup. Optional:
- `PORT` - Automatically set by hosting platform
- `DATABASE_URL` - If you add PostgreSQL later

### Frontend (Netlify/Vercel)

**Required**:
- `REACT_APP_API_URL` - Your backend URL (e.g., `https://your-app.railway.app`)

**To add in Netlify**:
1. Go to: Site settings → Environment variables
2. Add key-value pair
3. Trigger new deployment

**To add in Vercel**:
1. Go to: Project settings → Environment Variables
2. Add variable
3. Redeploy

---

## 📊 Testing Your Deployment

### Backend Health Check

```bash
# Check if backend is running
curl https://your-backend-url.railway.app/health

# Expected response:
{
  "status": "healthy",
  "search_engine": "initialized",
  "database": "connected",
  "timestamp": "2024-01-15T10:30:00"
}
```

### Search API Test

```bash
# Test search endpoint
curl -X POST https://your-backend-url.railway.app/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "stormwater management",
    "top_k": 5,
    "min_trust_score": 0.0
  }'
```

### Frontend Test Checklist

- [ ] App loads without errors
- [ ] Search bar is functional
- [ ] Search returns results from backend
- [ ] Filters work correctly
- [ ] Feedback buttons work
- [ ] Lesson input works
- [ ] No CORS errors in browser console
- [ ] Loading states appear correctly
- [ ] Mobile responsive design works

---

## 🐛 Troubleshooting

### Error: "CORS policy blocked"

**Problem**: Frontend can't connect to backend

**Solution**:
1. Check `api.py` CORS settings
2. Make sure your Netlify URL is in `allow_origins`
3. Redeploy backend after changes

```python
allow_origins=[
    "http://localhost:3000",
    "https://your-actual-netlify-url.netlify.app",  # Add this!
]
```

### Error: "Search engine not initialized"

**Problem**: Backend can't find embeddings or database

**Solution**:
1. Make sure `data/` folder is included in deployment
2. Check if `embeddings/` folder exists
3. You may need to rebuild embeddings in production:
   ```python
   # Run this once in production
   python create_sample_data.py
   ```

### Error: "Cannot find module axios"

**Problem**: Dependencies not installed

**Solution**:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Frontend shows "Search failed"

**Problem**: Backend URL is wrong or backend is down

**Solution**:
1. Check `REACT_APP_API_URL` environment variable
2. Test backend health: `curl https://your-backend-url/health`
3. Check browser console (F12) for actual error
4. Verify backend is deployed and running

### Railway deployment fails

**Problem**: Missing dependencies or build errors

**Solution**:
1. Check Railway build logs
2. Make sure `requirements.txt` is complete
3. Verify Python version in `runtime.txt`
4. Check that all imports in `api.py` can be resolved

---

## 🚀 Performance Optimization

### Backend

1. **Add caching**:
   ```python
   from functools import lru_cache
   
   @lru_cache(maxsize=100)
   def search_cached(query: str):
       return search_engine.search(query)
   ```

2. **Use production ASGI server**:
   - Already using `uvicorn` ✅
   - Consider adding Gunicorn for multiple workers:
     ```
     gunicorn -w 4 -k uvicorn.workers.UvicornWorker api:app
     ```

3. **Database optimization**:
   - Add database indexes
   - Use connection pooling
   - Consider PostgreSQL instead of SQLite for production

### Frontend

1. **Enable code splitting**:
   ```javascript
   const ExpertFinder = React.lazy(() => import('./components/ExpertFinder'));
   ```

2. **Add service worker** (PWA):
   - React build already generates `service-worker.js`
   - Just need to register it

3. **Optimize images**:
   - Compress avatars and icons
   - Use WebP format
   - Lazy load images

4. **Add caching headers** in `netlify.toml`:
   ```toml
   [[headers]]
     for = "/static/*"
     [headers.values]
       Cache-Control = "public, max-age=31536000, immutable"
   ```

---

## 📦 Database & Data Persistence

### Current Setup (SQLite + FAISS)
- **Good for**: Development, prototypes
- **Limitations**: File-based, not ideal for cloud

### Production Recommendations

1. **PostgreSQL + pgvector**:
   - Add to Railway: Database → New PostgreSQL
   - Update search engine to use pgvector instead of FAISS
   - Benefits: Better for production, supports multiple instances

2. **Pinecone** (Vector Database):
   - Managed vector search
   - Free tier: 1M vectors
   - Update `api.py` to use Pinecone client

3. **Upload data files**:
   - Make sure `data/` and `embeddings/` folders deploy with app
   - Or store in cloud storage (S3, Google Cloud Storage)

---

## 🔄 CI/CD Pipeline

### GitHub Actions (Optional but Recommended)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python -m pytest tests/  # Add tests!

  test-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: cd frontend && npm install && npm run build

  deploy:
    needs: [test-backend, test-frontend]
    runs-on: ubuntu-latest
    steps:
      - run: echo "Tests passed! Railway and Netlify will auto-deploy."
```

---

## 📈 Monitoring & Analytics

### Backend Monitoring

**Add logging**:
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/api/search")
async def search_projects(request: SearchRequest):
    logger.info(f"Search query: {request.query}")
    # ... rest of code
```

**Railway provides**:
- Automatic logs
- Metrics (CPU, memory, requests)
- Crash reporting

### Frontend Analytics

**Add Google Analytics**:
```javascript
// In frontend/public/index.html
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
```

**Or use Plausible** (privacy-friendly):
```html
<script defer data-domain="yourdomain.com" src="https://plausible.io/js/script.js"></script>
```

---

## 🎉 Launch Checklist

Before going live:

### Backend
- [ ] API health endpoint works
- [ ] All endpoints return correct data
- [ ] CORS configured for production URL
- [ ] Error handling implemented
- [ ] Logging configured
- [ ] Environment variables set
- [ ] Database initialized with data

### Frontend
- [ ] Production build succeeds (`npm run build`)
- [ ] API_URL points to production backend
- [ ] All features work end-to-end
- [ ] Mobile responsive
- [ ] No console errors
- [ ] Loading states implemented
- [ ] Error messages user-friendly

### Security
- [ ] CORS restricted to specific domains (not `*`)
- [ ] API rate limiting considered
- [ ] Sensitive data not in public code
- [ ] HTTPS enabled (automatic on Railway/Netlify)

### Documentation
- [ ] README updated with live URLs
- [ ] API documentation available (`/docs` endpoint)
- [ ] User guide created
- [ ] Known issues documented

---

## 🆘 Need Help?

**Common Issues**:
1. **CORS errors**: Update `allow_origins` in `api.py`
2. **Search not working**: Check `REACT_APP_API_URL` is set correctly
3. **Backend crashes**: Check Railway logs for Python errors
4. **Frontend won't build**: Delete `node_modules`, reinstall

**Resources**:
- FastAPI docs: https://fastapi.tiangolo.com
- Railway docs: https://docs.railway.app
- Netlify docs: https://docs.netlify.com
- React docs: https://react.dev

---

## 🎯 Quick Deploy Commands

### Deploy Backend to Railway
```bash
# Push to GitHub (Railway watches repo)
git add .
git commit -m "Deploy backend"
git push origin main

# Railway auto-deploys from GitHub
# Or use Railway CLI:
railway up
```

### Deploy Frontend to Netlify
```bash
# Via Netlify CLI
cd frontend
npm run build
netlify deploy --prod

# Or just push to GitHub (if connected)
git push origin main
```

---

## 🚀 You're Ready to Launch!

Your full-stack Tonkin Knowledge Finder is now:
✅ Backend API deployed and running
✅ React frontend deployed and beautiful  
✅ Both services communicating correctly  
✅ Ready for real users  

**Your URLs**:
- Frontend: `https://your-app.netlify.app`
- Backend API: `https://your-app.railway.app`
- API Docs: `https://your-app.railway.app/docs`

**Next Steps**:
1. Test with real users
2. Gather feedback
3. Monitor performance
4. Add features iteratively

Happy deploying! 🎉

