# 🎨 UI Mockup & Visual Guide

This document provides a visual description of what the Tonkin Knowledge Finder UI looks like.

---

## 📱 Full Page Layout

```
┌────────────────────────────────────────────────────────────────────┐
│                                                                    │
│  🗄️  TONKIN KNOWLEDGE FINDER                                      │
│      AI-Powered Project Intelligence & Expertise Discovery        │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
  ↑ Gradient Blue Header (#3B82F6 → #2563EB)

┌────────────────────────────────────────────────────────────────────┐
│  🔍  [Search projects, documents, or expertise...]  [Search]      │
│                                                                    │
│  Recent: [stormwater] [bridge] [Melbourne]                        │
└────────────────────────────────────────────────────────────────────┘
  ↑ White Card with Shadow

┌────────────────────────────────────────────────────────────────────┐
│  ✅ 3 Results Found  |  Searching for: "stormwater"  |  📊 23 Projects │
└────────────────────────────────────────────────────────────────────┘
  ↑ Stats Bar (only appears after search)

┌──────────────────┬─────────────────────────────────────────────────┐
│                  │                                                 │
│  FILTERS         │  SEARCH RESULTS                                │
│                  │                                                 │
│  Trust Score     │  [Result Card 1]                               │
│  ░░░░░░●────      │                                                 │
│  85%             │  [Result Card 2]                               │
│                  │                                                 │
│  Categories      │  [Result Card 3]                               │
│  ☑ Industrial    │                                                 │
│  ☐ Water         │                                                 │
│  ☐ Transport     │                                                 │
│                  │                                                 │
│  Regions         │                                                 │
│  ☑ Victoria      │                                                 │
│  ☐ NSW           │                                                 │
│                  │                                                 │
│  Experts         │                                                 │
│  [SM] Sarah M.   │                                                 │
│  [DC] David C.   │                                                 │
│                  │                                                 │
└──────────────────┴─────────────────────────────────────────────────┘
    Sticky Sidebar       Scrollable Main Area
```

---

## 🃏 Result Card - Detailed View

```
┌────────────────────────────────────────────────────────────────────┐
│ TKN-2024-SW-089                                    Trust  ██████ 92% │
│                                                   Relevance ████ 89% │
│ Sydney Waterfront Stormwater Management System                    │
│                                                                    │
│ Comprehensive stormwater detention and treatment system for       │
│ coastal development                                               │
│                                                                    │
│ ┌────────────────────────────────────────────────────────────┐   │
│ │ 👤 Client              📍 Region         📅 Timeline       │   │
│ │ Sydney Water Corp      New South Wales   Construction      │   │
│ │                                                            │   │
│ │ 💰 Budget              🎯 Category                        │   │
│ │ $12M                   Water Infrastructure               │   │
│ └────────────────────────────────────────────────────────────┘   │
│   ↑ Light Gray Background Box                                    │
│                                                                    │
│ Tags: [Civil] [Hydraulic] [Environmental] #stormwater #detention │
│                                                                    │
│ ───────────────────────────────────────────────────────────────   │
│                                                                    │
│ PROJECT TEAM                                                      │
│                                                                    │
│ ┌────────────────────┐  ┌────────────────────┐                   │
│ │ [JW] James Wilson  │  │ [SM] Sarah Mitchell│                   │
│ │ Project Leader     │  │ Reviewer           │                   │
│ └────────────────────┘  └────────────────────┘                   │
│   ↑ Hover → Blue Background                                      │
│                                                                    │
│ ───────────────────────────────────────────────────────────────   │
│                                                                    │
│ 💬 LESSONS LEARNED                                                │
│                                                                    │
│ │ Integration with existing systems requires detailed            │
│ │ coordination                                                   │
│ │ James Wilson • Design • 15 Apr 2024                           │
│   ↑ Orange/Yellow Background                                     │
│                                                                    │
│ ───────────────────────────────────────────────────────────────   │
│                                                                    │
│ ➕ ADD LESSON LEARNED / DECISION                                  │
│                                                                    │
│ [Share a key insight or decision...      ] [➕ Add Lesson]       │
│                                                                    │
│ ───────────────────────────────────────────────────────────────   │
│                                                                    │
│ [👍 Helpful]  [👎 Not Relevant]              🟢 Active            │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
  ↑ White Card with Border, Hover → Lift up + Blue Border
```

---

## 📊 Trust Badge - Progress Bar Detail

```
Trust Score
87%

████████████████░░░░  ← Gradient Blue Bar (87% filled)

Color Coding:
90-100% → Green Gradient  ████████████████████
75-89%  → Blue Gradient   ██████████████░░░░░░
60-74%  → Orange Gradient ████████░░░░░░░░░░░░
<60%    → Red Gradient    ████░░░░░░░░░░░░░░░░

Hover → Shows tooltip: "Overall project quality and reliability score"
```

---

## 👤 Expert Finder Modal - Full View

```
┌─────────────────────────────────────────────────────┐
│                                           [X Close] │
│  ┌─────────────────────────────────────────────┐   │
│  │                                             │   │
│  │        ┌──────┐                            │   │
│  │        │  SM  │                            │   │
│  │        └──────┘                            │   │
│  │     Sarah Mitchell                         │   │
│  │     Senior Infrastructure Lead             │   │
│  │                                             │   │
│  └─────────────────────────────────────────────┘   │
│    ↑ Gradient Blue Header                          │
│                                                     │
│  CONTACT                                            │
│  ┌────────────────┐  ┌──────────────────┐         │
│  │ ✉️  Email      │  │ 💬 Slack         │         │
│  └────────────────┘  └──────────────────┘         │
│                                                     │
│  PERFORMANCE                                        │
│  ┌─────────┐  ┌──────────┐  ┌────────────┐       │
│  │   12    │  │    28    │  │    91%     │       │
│  │ Projects│  │ Reviews  │  │ Avg Trust  │       │
│  └─────────┘  └──────────┘  └────────────┘       │
│                                                     │
│  EXPERTISE                                          │
│  [Industrial Infrastructure] [Port Engineering]     │
│  [Project Management]                               │
│                                                     │
│  RECENT PROJECTS                                    │
│  │ TKN-2024-MP-150  Melbourne Port Infrastructure  │
│  │ TKN-2024-SW-089  Sydney Waterfront Stormwater  │
│                                                     │
└─────────────────────────────────────────────────────┘
  ↑ White Card, Centered, Dark Overlay Background
```

---

## 🎨 Color Palette Visual

```
Primary Colors:
┌────────┐  #3B82F6  Primary Blue (buttons, links)
│ BLUE   │  #2563EB  Darker Blue (hover)
└────────┘

Status Colors:
┌────────┐  #10B981  Success Green (90%+ trust)
│ GREEN  │  #059669  Darker Green (hover)
└────────┘

┌────────┐  #F59E0B  Warning Orange (60-74% trust)
│ ORANGE │  #D97706  Darker Orange (hover)
└────────┘

┌────────┐  #EF4444  Error Red (<60% trust)
│  RED   │  #DC2626  Darker Red (hover)
└────────┘

Neutrals:
┌────────┐  #0F172A  Text Primary (headings)
│ DARK   │  #475569  Text Secondary (body)
│ GRAY   │  #64748B  Text Tertiary (metadata)
└────────┘

┌────────┐  #FFFFFF  Background Card
│ LIGHT  │  #F8FAFC  Background Page
│ GRAY   │  #F1F5F9  Background Alt
└────────┘

┌────────┐  #E2E8F0  Border Light
│ BORDER │  #CBD5E1  Border Medium
└────────┘
```

---

## 📏 Typography Scale

```
H1 - Project Titles
  Font: Inter
  Size: 24px (1.5rem)
  Weight: 700 (Bold)
  Color: #0F172A
  Example: "Sydney Waterfront Stormwater Management System"

H2 - Section Headers
  Font: Inter
  Size: 18px (1.125rem)
  Weight: 700 (Bold)
  Color: #0F172A
  Example: "PROJECT TEAM"

H3 - Subsection Titles
  Font: Inter
  Size: 16px (1rem)
  Weight: 600 (Semibold)
  Color: #475569
  Example: "LESSONS LEARNED"

Body Text
  Font: Inter
  Size: 16px (1rem)
  Weight: 400 (Regular)
  Color: #475569
  Line Height: 1.6
  Example: "Comprehensive stormwater detention..."

Metadata
  Font: Inter
  Size: 14px (0.875rem)
  Weight: 500 (Medium)
  Color: #64748B
  Example: "Client", "Region", "Budget"

Small Text
  Font: Inter
  Size: 12px (0.75rem)
  Weight: 500 (Medium)
  Color: #64748B
  Example: Labels, timestamps

Monospace (Project Numbers)
  Font: SF Mono, Monaco
  Size: 14px (0.875rem)
  Weight: 600 (Semibold)
  Color: #3B82F6
  Example: "TKN-2024-SW-089"
```

---

## 🎭 Component States

### Buttons

```
Default State:
┌──────────────┐
│   Search     │  Background: #3B82F6, Color: White
└──────────────┘

Hover State:
┌──────────────┐
│   Search     │  Background: #2563EB, Lift up 2px
└──────────────┘  Box Shadow: Larger

Active/Pressed:
┌──────────────┐
│   Search     │  Background: #2563EB, No lift
└──────────────┘

Disabled:
┌──────────────┐
│   Search     │  Background: #CBD5E1, No hover
└──────────────┘
```

### Input Fields

```
Default:
┌────────────────────────────────────┐
│ Search projects...                 │  Border: #E2E8F0
└────────────────────────────────────┘  Background: #F8FAFC

Focus:
┌────────────────────────────────────┐
│ Search projects...                 │  Border: #3B82F6
└────────────────────────────────────┘  Background: White
                                        Blue glow shadow
```

### Cards (Result Cards)

```
Default:
┌──────────────────────────────────┐
│ Project Details...               │  Border: #E2E8F0
│                                  │  Background: White
└──────────────────────────────────┘  Shadow: Small

Hover:
┌──────────────────────────────────┐
│ Project Details...               │  Border: #3B82F6
│                                  │  Lift up 4px
└──────────────────────────────────┘  Shadow: Large
│ Blue gradient bar appears on left
```

### Expert Cards

```
Default:
┌────────────────────┐
│ [SM] Sarah Mitchell│  Background: #F8FAFC
│ Project Leader     │  Border: #E2E8F0
└────────────────────┘

Hover:
┌────────────────────┐
│ [SM] Sarah Mitchell│  Background: #3B82F6
│ Project Leader     │  Text: White
└────────────────────┘  Slide right 4px
```

### Trust Badge Progress Bar

```
Animation Sequence (0.8s):

Initial:
[                    ] 0%

Animating:
[███░░░░░░░░░░░░░░░░] 15%
[███████░░░░░░░░░░░░░] 35%
[█████████████░░░░░░░] 65%

Final:
[███████████████████░] 87%

With shimmer effect moving left to right
```

---

## 📐 Layout Measurements

### Desktop (1440px width)

```
┌─────────────────────────────────────────────────────────────┐
│  Header: Full Width, 120px height                           │
├─────────────────────────────────────────────────────────────┤
│  Max Container: 1400px centered with 40px padding           │
│                                                              │
│  ┌──────────┬──────────────────────────────────────────┐   │
│  │ Sidebar  │  Main Content                            │   │
│  │ 280px    │  Flexible (calc(100% - 280px - 32px))   │   │
│  │          │                                          │   │
│  │ Sticky   │  Scrollable                             │   │
│  │ Top:32px │                                          │   │
│  └──────────┴──────────────────────────────────────────┘   │
│  ↑ 32px gap between columns                                 │
└─────────────────────────────────────────────────────────────┘
```

### Spacing System

```
Extra Small:  8px  (0.5rem)  - Between small elements
Small:       12px  (0.75rem) - Between related items
Medium:      16px  (1rem)    - Standard gap
Large:       24px  (1.5rem)  - Between sections
Extra Large: 32px  (2rem)    - Major section breaks
```

### Card Padding

```
Result Card:
┌─────────────────────────────────┐
│ ← 32px                  32px → │
│ ↑                               │
│ 32px                            │
│                                 │
│ Content Area                    │
│                                 │
│ 32px                            │
│ ↓                               │
└─────────────────────────────────┘

Metadata Grid:
┌─────────────────────────────────┐
│ ← 24px                  24px → │
│ ↑                               │
│ 24px      [Items]               │
│ ↓                               │
└─────────────────────────────────┘
```

---

## 🎬 Animations & Transitions

### Card Entrance
```
Initial:    Opacity 0, Y position +20px
Animate to: Opacity 1, Y position 0
Duration:   300ms
Easing:     Ease out
Stagger:    Each card delays by 100ms (0, 100ms, 200ms, 300ms...)
```

### Button Hover
```
Transform:  translateY(-2px)
Duration:   200ms
Easing:     Ease in-out
Shadow:     Increases from small to medium
```

### Modal Open
```
Overlay:
  Opacity: 0 → 1
  Duration: 200ms

Modal:
  Opacity: 0 → 1
  Scale: 0.95 → 1.0
  Y: +50px → 0
  Duration: 300ms
  Easing: Spring (damping: 25, stiffness: 300)
```

### Progress Bar Fill
```
Width: 0% → Target %
Duration: 800ms
Easing: Ease out

Shimmer Effect:
  Moving gradient overlay
  Duration: 2s
  Loop: Infinite
  Direction: Left to right
```

### Expert Card Hover
```
Transform: translateX(4px)
Background: #F8FAFC → #3B82F6
Text Color: #475569 → White
Duration: 200ms
Easing: Ease in-out
```

---

## 🎯 Interactive Elements

### Search Bar
```
Click: Focus input, blue border, white background
Type: Real-time state update
Enter: Submit search
Recent Tag Click: Fill input and search
```

### Trust Score Slider
```
Drag: Update value in real-time
Release: Trigger filter update
Display: Show current value (87%)
Color: Gradient based on value
```

### Checkboxes
```
Click: Toggle checked state
Effect: Immediate filter update
Visual: Blue checkmark when checked
```

### Feedback Buttons
```
Click: Toggle active state
Active: Blue background, white text
Inactive: Gray background, gray text
Effect: Send feedback to API
```

### Lesson Input
```
Type: Update input value
Enter: Submit lesson
Submit: Show success message (3s)
Auto-clear: After successful submission
```

### Expert Card Click
```
Click: Open expert modal
Modal: Fade in with animation
Background: Dark overlay
Close: Click X or outside modal
```

---

## 📱 Responsive Behavior

### Tablet (768px - 1024px)
```
- Single column layout
- Filter panel stacks on top
- Result cards full width
- Metadata grid: 2 columns instead of 4
- Font sizes: Slightly reduced
- Padding: Reduced to 16px
```

### Mobile (<768px)
```
- All single column
- Filter panel: Collapsible drawer
- Cards: Reduced padding (16px)
- Fonts: Mobile-optimized sizes
- Touch targets: Minimum 44px height
- Buttons: Full width
- Stats bar: Stacked layout
```

---

## ✨ Polish Details

### Shadows
```
Small:  0 1px 3px rgba(0, 0, 0, 0.1)
Medium: 0 4px 6px rgba(0, 0, 0, 0.1)
Large:  0 10px 15px rgba(0, 0, 0, 0.1)
```

### Border Radius
```
Small:  6px  - Tags, badges
Medium: 10px - Inputs, small buttons
Large:  12px - Cards, panels
XLarge: 16px - Major sections
Full:   50%  - Avatars, pills
```

### Focus States
```
All interactive elements have:
- Blue outline (3px solid #3B82F6)
- 2px offset
- Visible on keyboard navigation
```

### Loading States
```
Search button: "Searching..."
Lesson submit: "Saving..."
API calls: Spinner or skeleton screens
```

---

This visual guide should help you understand exactly what the UI looks like and how it behaves! 🎨

