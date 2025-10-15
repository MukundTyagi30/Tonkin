# Tonkin Knowledge Finder - React Frontend

A production-ready React frontend for the Tonkin Knowledge Finder AI-powered project intelligence platform.

## 🚀 Features

### Core Functionality
- **Single Search Bar**: Clean, intuitive search interface with instant feedback
- **Smart Result Cards**: Rich project cards with hierarchical information display
- **Trust Score Visualization**: Animated progress bars with color-coded quality indicators
- **Expert Discovery**: Click-through expert profiles with contact information
- **Lesson Learned Submission**: One-line input for capturing project insights
- **Advanced Filtering**: Side panel with trust score, category, region, and expert filters
- **Recent Search History**: Quick access to previous queries
- **Responsive Design**: Fully optimized for desktop and tablet displays

### UI/UX Highlights
- Modern, clean design with muted corporate color palette
- Smooth animations and transitions using Framer Motion
- Hover tooltips for contextual information
- Professional typography with Inter font family
- Clear visual hierarchy with appropriate font sizing
- Accessible color contrast ratios
- Loading states and success feedback

### Technical Architecture
- **Modular Components**: Each feature is a self-contained React component
- **State Management**: React hooks (useState, useEffect) for local state
- **Styled Components**: CSS-in-JS for scoped, maintainable styling
- **Sample Data**: Comprehensive mock data for testing and demos
- **API-Ready**: Structured to easily integrate with backend endpoints

## 📦 Installation

### Prerequisites
- Node.js 16+ and npm/yarn
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

The app will open at `http://localhost:3000`

## 🏗️ Project Structure

```
frontend/
├── public/
│   └── index.html              # HTML template
├── src/
│   ├── components/
│   │   ├── Header.js           # Main header with branding
│   │   ├── SearchBar.js        # Search input with recent searches
│   │   ├── StatsBar.js         # Results count and search summary
│   │   ├── FilterPanel.js      # Advanced filters sidebar
│   │   ├── ResultsList.js      # Results container
│   │   ├── ResultCard.js       # Individual project card
│   │   ├── TrustBadge.js       # Animated progress bar badge
│   │   ├── LessonInput.js      # Lesson learned submission
│   │   └── ExpertFinder.js     # Expert profile modal
│   ├── data/
│   │   └── sampleData.js       # Mock data for testing
│   ├── styles/
│   │   └── GlobalStyle.js      # Global CSS styles
│   ├── App.js                  # Main application component
│   └── index.js                # React entry point
├── package.json                # Dependencies and scripts
└── README.md                   # This file
```

## 🎨 Component Overview

### Header
- Displays application branding and logo
- Gradient background with Tonkin blue theme

### SearchBar
- Single search input with icon
- Shows total indexed projects
- Displays recent search tags for quick access
- Keyboard shortcut support (Enter to search)

### StatsBar
- Appears after search is performed
- Shows result count and total indexed projects
- Displays current search query

### FilterPanel
- **Trust Score Slider**: Color-coded gradient slider (0-100%)
- **Category Checkboxes**: Multi-select project categories
- **Region Checkboxes**: Multi-select geographical regions
- **Expert Finder**: Quick access to expert profiles
- **Clear Filters**: Reset all filters button
- Sticky positioning on desktop

### ResultCard
- **Project Overview**: Number, title, description
- **Trust & Relevance Scores**: Animated progress bars
- **Metadata Grid**: Client, region, timeline, budget, category
- **Tags**: Disciplines and keywords
- **Expert Team**: Clickable expert cards
- **Lessons Learned**: Display of existing lessons
- **Lesson Input**: Add new lesson learned
- **Feedback Buttons**: Thumbs up/down for relevance
- **Status Badge**: Current project status

### TrustBadge
- Animated progress bar component
- Color-coded based on score:
  - 90-100%: Green (Excellent)
  - 75-89%: Blue (Good)
  - 60-74%: Orange (Fair)
  - Below 60%: Red (Needs Review)
- Hover tooltip with explanation
- Shimmer animation effect

### LessonInput
- Single-line input for quick lesson capture
- Auto-tags with project phase
- Success confirmation message
- Enter key submission support

### ExpertFinder
- Modal overlay with expert profile
- Contact buttons (Email, Slack)
- Performance statistics
- Expertise tags
- Recent projects list
- Smooth animations

## 🔌 API Integration Guide

The frontend is structured to easily connect to your backend API. Here's how to integrate:

### 1. Search Functionality
Replace the `performSearch` function in `App.js`:

```javascript
const performSearch = async (query) => {
  try {
    const response = await axios.post('http://your-api.com/search', {
      query: query,
      filters: filters
    });
    setSearchResults(response.data.results);
  } catch (error) {
    console.error('Search failed:', error);
  }
};
```

### 2. Feedback Submission
Update the `handleFeedback` function in `App.js`:

```javascript
const handleFeedback = async (projectId, isPositive) => {
  try {
    await axios.post('http://your-api.com/feedback', {
      projectId,
      isPositive,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Feedback submission failed:', error);
  }
};
```

### 3. Lesson Submission
Update the `handleLessonSubmit` function in `App.js`:

```javascript
const handleLessonSubmit = async (projectId, lesson) => {
  try {
    await axios.post('http://your-api.com/lessons', {
      projectId,
      ...lesson,
      userId: 'current-user-id' // Get from auth context
    });
  } catch (error) {
    console.error('Lesson submission failed:', error);
  }
};
```

## 🎯 Sample Data

The application includes comprehensive sample data:
- **6 Projects**: Covering various infrastructure types
- **6 Experts**: With realistic profiles and statistics
- **Lessons Learned**: Examples from different project phases
- **Categories & Regions**: Australian infrastructure context

Edit `src/data/sampleData.js` to customize for your needs.

## 🎨 Customization

### Colors
The design uses a cohesive color system. To customize, edit the color values in component files:

- **Primary Blue**: `#3B82F6`
- **Secondary Blue**: `#2563EB`
- **Success Green**: `#10B981`
- **Warning Orange**: `#F59E0B`
- **Error Red**: `#EF4444`

### Typography
The app uses the Inter font family. To change:
1. Update the Google Fonts link in `public/index.html`
2. Modify font-family in `src/styles/GlobalStyle.js`

### Layout
- Adjust `max-width` in styled components for different container widths
- Modify breakpoints in media queries for responsive behavior
- Change grid columns in metadata and filter sections

## 🚀 Deployment

### Build for Production
```bash
npm run build
```

This creates an optimized production build in the `build/` folder.

### Deploy to Hosting
The build folder can be deployed to:
- **Netlify**: Drag and drop the build folder
- **Vercel**: Connect your GitHub repository
- **AWS S3**: Upload build folder to S3 bucket
- **Azure Static Web Apps**: Connect your repository

### Environment Variables
For production, create a `.env` file:
```
REACT_APP_API_URL=https://your-api.com
REACT_APP_AUTH_DOMAIN=your-auth-domain
```

Access in code: `process.env.REACT_APP_API_URL`

## 🧪 Testing

Currently includes sample data for manual testing. To add automated tests:

```bash
npm test
```

Example test structure:
```javascript
// SearchBar.test.js
import { render, screen, fireEvent } from '@testing-library/react';
import SearchBar from './components/SearchBar';

test('submits search query on Enter key', () => {
  const mockSearch = jest.fn();
  render(<SearchBar onSearch={mockSearch} />);
  
  const input = screen.getByPlaceholderText(/search projects/i);
  fireEvent.change(input, { target: { value: 'stormwater' } });
  fireEvent.keyPress(input, { key: 'Enter', code: 13 });
  
  expect(mockSearch).toHaveBeenCalledWith('stormwater');
});
```

## 📱 Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 🔧 Troubleshooting

### Port Already in Use
```bash
# Kill process on port 3000
npx kill-port 3000

# Or start on different port
PORT=3001 npm start
```

### Styling Issues
- Clear browser cache
- Check styled-components version compatibility
- Verify all imports are correct

### Animation Performance
If animations are laggy:
- Reduce `framer-motion` animation complexity
- Use `will-change` CSS property
- Test on target devices

## 📄 License

Proprietary - Tonkin + Taylor

## 👥 Support

For technical support or questions:
- Email: support@tonkin.com.au
- Internal Slack: #knowledge-finder

## 🎉 Demo Ready

This frontend is fully functional with sample data and ready for:
- **Internal demos**: Showcase to stakeholders
- **User testing**: Gather feedback from engineers
- **Integration**: Connect to your backend API
- **Customization**: Adapt to specific requirements

Start the app and try searching for:
- "stormwater" - Find water management projects
- "bridge" - Discover bridge engineering work
- "Melbourne" - Search by location
- Expert names - Find projects by team members

