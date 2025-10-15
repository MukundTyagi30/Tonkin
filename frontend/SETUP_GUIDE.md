# Tonkin Knowledge Finder - Quick Setup Guide

## 🚀 Getting Started in 5 Minutes

### Step 1: Prerequisites Check
Ensure you have Node.js installed:
```bash
node --version  # Should be v16 or higher
npm --version   # Should be v7 or higher
```

If not installed, download from: https://nodejs.org/

### Step 2: Install Dependencies
```bash
cd frontend
npm install
```

This will install:
- React 18
- Styled Components
- Framer Motion
- React Icons
- Axios

### Step 3: Start Development Server
```bash
npm start
```

Your browser will automatically open to `http://localhost:3000`

### Step 4: Test the Application
Try these searches in the demo:
1. **"stormwater"** - Find water management projects
2. **"bridge"** - Discover bridge engineering projects
3. **"Melbourne"** - Search by location
4. **"Sarah Mitchell"** - Find projects by expert

### Step 5: Explore Features

#### Search & Filters
- Use the main search bar at the top
- Adjust the **Trust Score slider** to filter by quality
- Select **Categories** (Water Infrastructure, Transport, etc.)
- Choose **Regions** (Victoria, NSW, etc.)
- Click **Expert names** to see their profiles

#### Result Cards
- View project details, trust scores, and relevance
- Click **expert names** to see full profiles with contact info
- Add **lessons learned** at the bottom of each card
- Give **feedback** with thumbs up/down buttons

#### Expert Finder
- Click any expert name in results or the filter panel
- View their performance stats and recent projects
- Access **Email** and **Slack** contact buttons

## 📁 Project Structure Overview

```
frontend/
├── public/              # Static files
├── src/
│   ├── components/      # React components (Header, SearchBar, etc.)
│   ├── data/           # Sample data for testing
│   ├── styles/         # Global styles
│   ├── App.js          # Main application
│   └── index.js        # Entry point
└── package.json        # Dependencies
```

## 🔧 Configuration

### Connecting to Your Backend API

#### Option 1: Environment Variables
Create `.env` file in `frontend/` directory:
```
REACT_APP_API_URL=http://localhost:8000
REACT_APP_AUTH_ENABLED=false
```

#### Option 2: Direct Configuration
Edit `src/App.js` and update the API endpoints:

```javascript
// Replace the performSearch function
const performSearch = async (query) => {
  const response = await axios.post('YOUR_API_URL/search', {
    query: query,
    filters: filters
  });
  setSearchResults(response.data.results);
};
```

### Using Sample Data vs Real API

**Sample Data Mode (Default):**
- No backend required
- Uses `src/data/sampleData.js`
- Perfect for demos and testing

**API Mode:**
- Requires backend server running
- Update API calls in `App.js`
- See `README.md` API Integration section

## 🎨 Customization Quick Tips

### Change Primary Color
In all component files, replace `#3B82F6` with your color:
```javascript
background: #YOUR_COLOR;
```

### Adjust Card Spacing
In `ResultCard.js`:
```javascript
const Card = styled.div`
  padding: 2rem;  // Change this value
  ...
`;
```

### Modify Search Placeholder
In `SearchBar.js`:
```javascript
<SearchInput
  placeholder="Your custom placeholder text..."
/>
```

## 🐛 Common Issues & Solutions

### Issue: Port 3000 Already in Use
**Solution:**
```bash
# Kill existing process
npx kill-port 3000

# Or use different port
PORT=3001 npm start
```

### Issue: Dependencies Won't Install
**Solution:**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules
npm install
```

### Issue: Styling Looks Broken
**Solution:**
```bash
# Clear browser cache
# Or open in incognito/private window
# Verify all dependencies installed:
npm list styled-components framer-motion
```

### Issue: Search Not Working
**Check:**
1. Are you using sample data mode? (Should work by default)
2. If using API: Is your backend server running?
3. Check browser console for errors (F12)
4. Verify API URL in configuration

## 📦 Building for Production

### Create Optimized Build
```bash
npm run build
```

Output will be in `build/` folder.

### Test Production Build Locally
```bash
# Install serve
npm install -g serve

# Serve the build
serve -s build
```

Visit `http://localhost:3000` to test.

### Deploy to Netlify (Free & Easy)
1. Sign up at https://netlify.com
2. Drag and drop your `build/` folder
3. Your app is live!

### Deploy to Vercel
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd frontend
vercel
```

## 🎯 Next Steps

### For Demos
1. Keep sample data mode (no setup required)
2. Customize colors and branding
3. Update sample data with your projects

### For Development
1. Connect to your backend API
2. Add authentication
3. Implement real-time features
4. Add more filters and search options

### For Production
1. Set up proper API integration
2. Add error boundaries
3. Implement analytics
4. Set up CI/CD pipeline
5. Add E2E tests

## 📚 Additional Resources

### Learn React
- Official Tutorial: https://react.dev/learn
- React Hooks: https://react.dev/reference/react

### Styled Components
- Documentation: https://styled-components.com/docs

### Framer Motion
- Documentation: https://www.framer.com/motion/

### Tonkin Internal
- Backend API Docs: [Your internal URL]
- Figma Designs: [Your Figma link]
- Slack Channel: #knowledge-finder

## ✅ Verification Checklist

Before presenting or deploying, verify:

- [ ] Application starts without errors
- [ ] Search returns results
- [ ] Filters work correctly
- [ ] Trust badges display and animate
- [ ] Expert profiles open on click
- [ ] Lesson input submits successfully
- [ ] Feedback buttons toggle correctly
- [ ] Recent searches appear
- [ ] Responsive on different screen sizes
- [ ] No console errors
- [ ] All links/buttons work
- [ ] Colors match branding

## 🆘 Getting Help

### Quick Debugging
```bash
# Check React version
npm list react

# Verify all dependencies
npm list

# Run in verbose mode
npm start --verbose
```

### Need Support?
1. Check this guide first
2. Review `README.md` for detailed docs
3. Search GitHub issues
4. Contact: support@tonkin.com.au
5. Internal Slack: #knowledge-finder

## 🎉 You're Ready!

The frontend is now running and fully functional with sample data. Try searching for projects, filtering results, and exploring expert profiles.

**Happy building! 🚀**

