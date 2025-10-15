# Component Architecture Guide

## 📦 Component Hierarchy

```
App.js (Main Container)
├── Header.js (Fixed Top)
├── SearchBar.js (Search Interface)
│   └── Recent Search Tags
├── StatsBar.js (Results Summary)
└── ContentGrid
    ├── FilterPanel.js (Sidebar)
    │   ├── Trust Score Slider
    │   ├── Category Checkboxes
    │   ├── Region Checkboxes
    │   └── Expert Quick Links
    └── ResultsList.js (Main Area)
        └── ResultCard.js (Repeated for each result)
            ├── TrustBadge.js (Score Visualization)
            ├── Metadata Grid
            ├── Expert Cards
            ├── LessonInput.js (Add Lesson)
            └── Feedback Buttons
            
ExpertFinder.js (Modal Overlay - Triggered by Expert Click)
```

## 🎯 Component Details

### 1. App.js
**Purpose**: Main application container and state manager

**State Variables**:
- `searchQuery`: Current search input
- `searchResults`: Array of matching projects
- `recentSearches`: Last 5 searches
- `filters`: Object containing all filter values
- `hasSearched`: Boolean to show/hide results
- `selectedExpert`: Currently viewing expert profile

**Key Functions**:
- `performSearch(query)`: Execute search with filters
- `handleSearch(query)`: Update state and perform search
- `handleFilterChange(newFilters)`: Update filters and re-search
- `handleExpertSelect(expertName)`: Open expert modal
- `handleFeedback(projectId, isPositive)`: Record result feedback
- `handleLessonSubmit(projectId, lesson)`: Save new lesson

**Props Passed Down**:
```javascript
<SearchBar 
  onSearch={handleSearch}
  recentSearches={recentSearches}
  totalProjects={sampleProjects.length}
/>

<FilterPanel 
  filters={filters}
  onFilterChange={handleFilterChange}
  experts={expertProfiles}
  onExpertSelect={handleExpertSelect}
/>

<ResultsList 
  results={searchResults}
  onFeedback={handleFeedback}
  onLessonSubmit={handleLessonSubmit}
  onExpertClick={handleExpertSelect}
/>

<ExpertFinder 
  expert={selectedExpert}
  onClose={handleExpertClose}
  projects={filteredProjects}
/>
```

---

### 2. Header.js
**Purpose**: Application branding and navigation

**Features**:
- Tonkin logo
- Application title
- Tagline

**Styling**:
- Gradient blue background
- Fixed at top (sticky)
- Responsive text sizing

**No Props Required** (Static component)

---

### 3. SearchBar.js
**Purpose**: Main search interface

**Props**:
```javascript
{
  onSearch: Function,        // Callback when search submitted
  recentSearches: Array,     // Last 5 searches
  totalProjects: Number      // Total indexed projects
}
```

**Features**:
- Search input with icon
- Enter key submission
- Recent search tags (clickable)
- Search button

**Internal State**:
- `query`: Current input value

**Events**:
- `onChange`: Update query state
- `onKeyPress`: Submit on Enter
- `onSubmit`: Trigger search
- Recent tag `onClick`: Set query and search

---

### 4. StatsBar.js
**Purpose**: Display search results summary

**Props**:
```javascript
{
  resultCount: Number,       // Number of results found
  totalProjects: Number,     // Total projects in database
  searchQuery: String        // Current search term
}
```

**Features**:
- Results count with icon
- Search query display
- Total projects indexed
- Animated entrance

**Conditional Rendering**:
Only shows when `hasSearched` is true

---

### 5. FilterPanel.js
**Purpose**: Advanced search filtering

**Props**:
```javascript
{
  filters: {
    minTrustScore: Number,   // 0-1 range
    categories: Array,       // Selected categories
    regions: Array,          // Selected regions
    experts: Array           // Selected experts
  },
  onFilterChange: Function,  // Callback when filters update
  experts: Array,            // All expert profiles
  onExpertSelect: Function   // Callback when expert clicked
}
```

**Features**:
- **Trust Score Slider**: 
  - Range: 0-100%
  - Color-coded gradient
  - Real-time value display
  
- **Category Checkboxes**:
  - Multi-select
  - Scrollable list
  - Auto-filter on change
  
- **Region Checkboxes**:
  - Multi-select
  - Australian regions
  - Auto-filter on change
  
- **Expert Quick Links**:
  - Top 5 experts
  - Avatar initials
  - Click to view profile
  
- **Clear Filters Button**:
  - Only shows when filters active
  - Resets all filters

**Internal Functions**:
```javascript
handleTrustScoreChange(e)     // Update trust score
handleCategoryChange(category) // Toggle category
handleRegionChange(region)     // Toggle region
handleClearFilters()           // Reset all
```

---

### 6. ResultsList.js
**Purpose**: Container for search results

**Props**:
```javascript
{
  results: Array,            // Array of project objects
  onFeedback: Function,      // Feedback callback
  onLessonSubmit: Function,  // Lesson submit callback
  onExpertClick: Function    // Expert click callback
}
```

**Features**:
- Maps over results array
- Staggered animation (delay per card)
- Passes props to ResultCard

---

### 7. ResultCard.js
**Purpose**: Display individual project details

**Props**:
```javascript
{
  project: {
    id: Number,
    projectNumber: String,
    projectName: String,
    description: String,
    client: String,
    region: String,
    category: String,
    phase: String,
    trustScore: Number,
    similarityScore: Number,
    projectLeader: String,
    projectReviewer: String,
    disciplines: Array,
    budget: String,
    status: String,
    lessons: Array,
    tags: Array
  },
  onFeedback: Function,
  onLessonSubmit: Function,
  onExpertClick: Function
}
```

**Internal State**:
- `feedback`: Boolean or null (thumbs up/down state)

**Sections**:
1. **Header**: Project number, title, description
2. **Scores**: Trust badge and relevance badge
3. **Metadata Grid**: Client, region, timeline, budget, category
4. **Tags**: Disciplines and keywords
5. **Experts Section**: Leader and reviewer cards
6. **Lessons Section**: Existing lessons (if any)
7. **Lesson Input**: Add new lesson component
8. **Footer**: Feedback buttons and status badge

**Visual Feedback**:
- Hover effect (lift and border color)
- Left gradient bar on hover
- Expert cards change color on hover
- Feedback buttons toggle active state

---

### 8. TrustBadge.js
**Purpose**: Visualize trust/relevance scores

**Props**:
```javascript
{
  score: Number,           // 0-1 range
  label: String,          // "Trust Score" or "Relevance"
  tooltip: String,        // Explanation text
  color: String           // Optional custom color
}
```

**Features**:
- Animated progress bar fill
- Color-coded by score:
  - 90-100%: Green gradient
  - 75-89%: Blue gradient
  - 60-74%: Orange gradient
  - <60%: Red gradient
- Shimmer animation
- Hover tooltip
- Percentage display

**Styling Algorithm**:
```javascript
if (percentage >= 90) return 'green';
if (percentage >= 75) return 'blue';
if (percentage >= 60) return 'orange';
return 'red';
```

---

### 9. LessonInput.js
**Purpose**: Capture lessons learned

**Props**:
```javascript
{
  projectId: Number,       // Project identifier
  projectPhase: String,    // Current project phase
  onSubmit: Function       // Callback with lesson data
}
```

**Internal State**:
- `lesson`: Input text
- `isSubmitting`: Loading state
- `showSuccess`: Success message visibility

**Features**:
- Single-line text input
- Enter key submission
- Auto-tag with project phase
- Loading state during submit
- Success confirmation (3s)
- Auto-clear after submit

**Submission Data**:
```javascript
{
  text: String,
  phase: String,
  author: String,  // From auth context in production
  date: ISO String
}
```

---

### 10. ExpertFinder.js
**Purpose**: Display expert profiles

**Props**:
```javascript
{
  expert: {
    name: String,
    role: String,
    email: String,
    slack: String,
    expertise: Array,
    projectsLed: Number,
    projectsReviewed: Number,
    avgTrustScore: Number,
    avatar: String
  },
  onClose: Function,
  projects: Array  // Projects involving this expert
}
```

**Features**:
- **Modal Overlay**: Click outside to close
- **Header**: Avatar, name, role
- **Contact Section**: Email and Slack buttons
- **Performance Stats**: 
  - Projects led
  - Reviews completed
  - Average trust score
- **Expertise Tags**: Skills and specializations
- **Recent Projects**: Last 5 projects

**Animations**:
- Fade in overlay
- Scale and slide modal
- Close button rotation

**External Links**:
```javascript
Email: `mailto:${expert.email}`
Slack: `slack://user?team=tonkin&id=${expert.slack}`
```

---

## 🔄 Data Flow

### Search Flow
```
User types in SearchBar
  ↓
SearchBar.onChange updates local state
  ↓
User presses Enter or clicks Search
  ↓
SearchBar.onSearch calls App.handleSearch
  ↓
App.performSearch executes search logic
  ↓
App.setSearchResults updates state
  ↓
ResultsList receives new results
  ↓
ResultCard components re-render
```

### Filter Flow
```
User adjusts FilterPanel controls
  ↓
FilterPanel.handleFilterChange updates local filters
  ↓
FilterPanel.onFilterChange calls App.handleFilterChange
  ↓
App.performSearch re-executes with new filters
  ↓
Results update
```

### Expert Selection Flow
```
User clicks expert name in ResultCard
  ↓
ResultCard.onClick calls App.onExpertClick
  ↓
App.handleExpertSelect sets selectedExpert state
  ↓
ExpertFinder renders with expert data
  ↓
User clicks close or overlay
  ↓
ExpertFinder.onClose clears selectedExpert
  ↓
Modal disappears
```

### Lesson Submission Flow
```
User types lesson in LessonInput
  ↓
User presses Enter or clicks Add
  ↓
LessonInput.handleSubmit packages data
  ↓
LessonInput.onSubmit calls App.handleLessonSubmit
  ↓
App sends to API (or logs in demo mode)
  ↓
LessonInput shows success message
  ↓
Input clears automatically
```

---

## 🎨 Styling Patterns

### Color System
```javascript
// Primary Colors
--primary-blue: #3B82F6
--primary-blue-dark: #2563EB

// Status Colors
--success-green: #10B981
--warning-orange: #F59E0B
--error-red: #EF4444

// Neutrals
--text-primary: #0F172A
--text-secondary: #475569
--text-tertiary: #64748B
--bg-primary: #FFFFFF
--bg-secondary: #F8FAFC
--border: #E2E8F0
```

### Spacing Scale
```javascript
--space-xs: 0.5rem   (8px)
--space-sm: 0.75rem  (12px)
--space-md: 1rem     (16px)
--space-lg: 1.5rem   (24px)
--space-xl: 2rem     (32px)
--space-2xl: 2.5rem  (40px)
```

### Border Radius
```javascript
--radius-sm: 6px
--radius-md: 10px
--radius-lg: 12px
--radius-xl: 16px
--radius-full: 50%
```

### Typography
```javascript
// Font Sizes
--text-xs: 0.75rem   (12px)
--text-sm: 0.875rem  (14px)
--text-base: 1rem    (16px)
--text-lg: 1.125rem  (18px)
--text-xl: 1.5rem    (24px)
--text-2xl: 2rem     (32px)

// Font Weights
--weight-normal: 400
--weight-medium: 500
--weight-semibold: 600
--weight-bold: 700
--weight-extrabold: 800
```

---

## 🔧 Extending Components

### Adding a New Filter Type
1. Add state to `App.js` filters object
2. Add UI control to `FilterPanel.js`
3. Add handler function in `FilterPanel.js`
4. Update filter logic in `App.performSearch`

### Adding a New Metadata Field
1. Add field to sample data in `sampleData.js`
2. Add display in `ResultCard.js` metadata grid
3. Add icon from `react-icons/fi`
4. Style with existing patterns

### Creating a New Component
```javascript
import React from 'react';
import styled from 'styled-components';

const Container = styled.div`
  // Your styles here
`;

const MyComponent = ({ prop1, prop2 }) => {
  return (
    <Container>
      {/* Your JSX here */}
    </Container>
  );
};

export default MyComponent;
```

---

## 🐛 Debugging Tips

### Component Not Rendering
1. Check if component is imported
2. Verify props are passed correctly
3. Check conditional rendering logic
4. Look for console errors

### Styles Not Applying
1. Verify styled-components syntax
2. Check for typos in property names
3. Ensure component is wrapped in styled wrapper
4. Check CSS specificity

### State Not Updating
1. Verify state is declared with useState
2. Check if setter function is called correctly
3. Ensure you're not mutating state directly
4. Use React DevTools to inspect state

### Props Not Received
1. Check parent component is passing props
2. Verify prop names match
3. Use PropTypes or TypeScript for type safety
4. Console.log props in child component

---

## 📚 Best Practices

### Component Organization
- One component per file
- Keep components focused (single responsibility)
- Extract reusable logic into custom hooks
- Use meaningful component and prop names

### Styling
- Use styled-components for all styling
- Create reusable styled components
- Follow mobile-first approach
- Use consistent spacing and colors

### State Management
- Keep state as close to where it's used as possible
- Lift state up when multiple components need it
- Use context for deeply nested props
- Consider Redux for complex state

### Performance
- Use React.memo for expensive components
- Implement virtual scrolling for large lists
- Lazy load images and heavy components
- Debounce search inputs

---

## ✅ Component Checklist

When creating a new component, ensure:
- [ ] Has clear purpose and responsibility
- [ ] Props are documented
- [ ] Internal state is minimal
- [ ] Handles loading and error states
- [ ] Responsive on mobile
- [ ] Accessible (keyboard navigation, ARIA labels)
- [ ] Follows existing styling patterns
- [ ] No console warnings
- [ ] Reusable where possible

