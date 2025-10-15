# 🚀 Deploy in 10 Minutes - Quick Reference

## What You Have Now

✅ **React Frontend** (`/frontend/`) - Modern UI with search, filters, and results  
✅ **FastAPI Backend** (`api.py`) - REST API that wraps your search engine  
✅ **Full Integration** - Frontend talks to backend via API calls  
✅ **Ready to Deploy** - All configs and documentation complete  

---

## 🎯 Deployment Steps (Simple Version)

### 1️⃣ Deploy Backend to Railway (3 minutes)

```bash
# Option A: Deploy from GitHub
1. Go to: https://railway.app
2. Click "New Project" → "Deploy from GitHub"
3. Select your repo
4. Railway auto-detects Python and deploys
5. Get your URL: https://your-app.railway.app

# Option B: Railway CLI
railway login
railway init
railway up
```

**Test it works:**
```bash
curl https://your-app.railway.app/health
```

### 2️⃣ Deploy Frontend to Netlify (2 minutes)

```bash
# Build the app
cd frontend
npm install
npm run build

# Deploy
# Drag the 'build' folder to: https://app.netlify.com/drop
```

**Add environment variable in Netlify:**
- Go to: Site Settings → Environment Variables
- Add: `REACT_APP_API_URL` = `https://your-app.railway.app`
- Redeploy

### 3️⃣ Update CORS in Backend

Edit `api.py` line 23-26:
```python
allow_origins=[
    "http://localhost:3000",
    "https://your-actual-netlify-url.netlify.app",  # Add this!
],
```

Push to GitHub → Railway auto-redeploys

---

## 🧪 Test Locally First

### Run Everything Locally

```bash
# Easy way - one command:
bash start_local.sh

# Manual way:
# Terminal 1 - Backend
uvicorn api:app --reload --port 8000

# Terminal 2 - Frontend
cd frontend && npm start
```

Visit: http://localhost:3000

---

## 📚 Full Documentation

- **Comprehensive Guide**: `FULL_STACK_DEPLOYMENT.md`
- **Frontend Details**: `FRONTEND_DEPLOYMENT.md`
- **React Deploy**: `REACT_DEPLOY_INSTRUCTIONS.md`

---

## 🆘 Troubleshooting Quick Fixes

### "CORS Error"
→ Add your Netlify URL to `allow_origins` in `api.py`

### "Search Returns Nothing"
→ Check `REACT_APP_API_URL` env variable in Netlify

### "Backend Won't Start"
→ Check Railway logs, ensure all dependencies in `requirements.txt`

### "Frontend Won't Build"
→ `cd frontend && rm -rf node_modules && npm install && npm run build`

---

## 🎯 What's Next?

1. ✅ Deploy backend to Railway
2. ✅ Deploy frontend to Netlify  
3. ✅ Configure environment variables
4. ✅ Test end-to-end
5. 🎉 Share with users!

**Your Live URLs:**
- Frontend: `https://your-app.netlify.app`
- Backend: `https://your-app.railway.app`
- API Docs: `https://your-app.railway.app/docs`

---

## 💡 Pro Tips

1. **Use GitHub for continuous deployment** - Both Railway and Netlify can auto-deploy on push
2. **Check Railway logs** if backend has issues
3. **Use demo mode** by setting `USE_SAMPLE_DATA = true` in `frontend/src/config.js`
4. **Monitor costs** - Railway free tier is generous but has limits

---

That's it! You now have a full-stack, production-ready knowledge management system. 🎉

