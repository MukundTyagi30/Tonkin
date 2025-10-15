# Deploy Your React Frontend to Production

## 🚀 Quick Deploy to Netlify (5 Minutes)

Your React frontend **CANNOT** be deployed to Streamlit Cloud. Here's how to deploy it properly:

### Method 1: Drag & Drop Deploy (Fastest)

1. **Build the React app:**
   ```bash
   cd frontend
   npm install
   npm run build
   ```
   This creates a `frontend/build/` folder with your production app.

2. **Deploy to Netlify:**
   - Go to: https://app.netlify.com/drop
   - Drag the entire `build/` folder onto the page
   - Your app goes live instantly!
   - You'll get a URL like: `https://random-name.netlify.app`

3. **Custom domain (optional):**
   - In Netlify dashboard, go to: Site settings → Domain management
   - Add your custom domain

---

## Method 2: GitHub Auto-Deploy (Recommended for Updates)

### Step 1: Push frontend to GitHub

```bash
cd frontend

# Initialize git (if not already)
git init
git add .
git commit -m "Initial React frontend"

# Create GitHub repo and push
# (Or push to your existing repo)
git remote add origin YOUR_GITHUB_URL
git push -u origin main
```

### Step 2: Connect to Netlify

1. Go to: https://app.netlify.com
2. Click **"Add new site"** → **"Import an existing project"**
3. Choose **GitHub**
4. Select your repository
5. Configure build settings:
   - **Base directory:** `frontend`
   - **Build command:** `npm run build`
   - **Publish directory:** `frontend/build`
6. Click **"Deploy site"**

Now every time you push to GitHub, Netlify automatically rebuilds and deploys!

---

## Method 3: Vercel (Alternative to Netlify)

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd frontend
vercel

# Follow the prompts:
# - Set up and deploy? Y
# - Which scope? (your account)
# - Link to existing project? N
# - What's your project's name? tonkin-knowledge-finder
# - In which directory is your code located? ./
# - Want to override settings? N
```

Vercel deploys your app and gives you a production URL instantly!

---

## 🔗 Connecting Frontend to Backend

Your React app currently uses sample data. To connect it to your Streamlit backend:

### Option A: Keep Backend on Streamlit Cloud

Update `frontend/src/App.js` to point to your Streamlit app:

```javascript
// At the top of App.js
const API_URL = 'https://your-app.streamlit.app';

// Update search function
const performSearch = async (query) => {
  try {
    const response = await axios.post(`${API_URL}/api/search`, {
      query: query,
      filters: filters
    });
    setSearchResults(response.data.results);
  } catch (error) {
    console.error('Search failed:', error);
  }
};
```

**Note:** You'll need to add API endpoints to your Streamlit app for this to work.

### Option B: Separate Backend API

Create a proper backend API (FastAPI, Flask, Express) and deploy it separately:
- Backend → Deploy to Heroku, Railway, or AWS
- Frontend → Deploy to Netlify/Vercel
- They communicate via REST API

---

## 📊 Current Architecture Options

### Architecture 1: Standalone React (Current)
```
React Frontend (Netlify) → Sample Data Built-in
✅ Fast, no backend needed
✅ Great for demos
❌ Data is static
```

### Architecture 2: React + Streamlit Backend
```
React Frontend (Netlify) → Streamlit App (Streamlit Cloud)
⚠️ Possible but tricky (Streamlit not designed as API)
❌ Limited API capabilities
```

### Architecture 3: React + Proper Backend (Recommended)
```
React Frontend (Netlify) → FastAPI Backend (Railway/Heroku) → Database
✅ Full control
✅ Real-time data
✅ Scalable
```

---

## 🎯 Recommended Path

**For immediate deployment:**
1. Build React app: `cd frontend && npm run build`
2. Deploy to Netlify: Drag `build/` folder to https://app.netlify.com/drop
3. Share the Netlify URL with stakeholders
4. Keep using sample data for now

**For production:**
1. Build a proper FastAPI backend (I can help with this)
2. Deploy backend to Railway or Heroku
3. Connect React frontend to backend API
4. Deploy frontend to Netlify/Vercel

---

## ❓ What About Streamlit?

**Streamlit Cloud purpose:**
- Hosts Python Streamlit apps only
- Your `app.py`, `app_enhanced.py` files
- Not designed for React apps

**If you want to keep Streamlit:**
- Your Streamlit app (`app_enhanced.py`) can stay on Streamlit Cloud
- Your React app needs separate deployment (Netlify/Vercel)
- Pick one as your primary interface

---

## 🚀 Deploy Now

Choose your method and let's get your React app live!

**Need help?** Let me know if you want me to:
1. Create deployment scripts
2. Set up a proper backend API
3. Configure environment variables
4. Set up custom domain

