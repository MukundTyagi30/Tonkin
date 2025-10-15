"""
Tonkin Knowledge Finder - Enhanced Streamlit Application

A local, offline prototype for finding trusted past projects by searching
SF84 Project Basis Reports using semantic search with enhanced UI.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import sys
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime, timedelta
import random

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from search import SemanticSearchEngine
from database import KnowledgeDatabase
from utils import (
    open_file, format_date, get_relative_time, format_file_size,
    create_trust_badges, highlight_query_terms
)

# Configure Streamlit page
st.set_page_config(
    page_title="Tonkin Knowledge Finder | AI-Powered Project Intelligence",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "Tonkin Knowledge Finder - AI-Powered Project Intelligence & Expertise Discovery"
    }
)

# COMPLETELY REDESIGNED - REACT-STYLE MODERN UI
st.markdown("""
<style>
    /* Import Modern Professional Fonts - React Style */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    /* GLOBAL RESET - Clean Slate */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    }
    
    /* Remove ALL Streamlit Branding */
    #MainMenu, footer, header {
        visibility: hidden !important;
        height: 0 !important;
        margin: 0 !important;
    }
    
    /* REACT-STYLE APP CONTAINER */
    .main .block-container {
        padding: 2rem 3rem !important;
        max-width: 1400px !important;
        margin: 0 auto !important;
        background: #F8FAFC !important;
    }
    
    /* Smooth Modern Scrolling */
    html {
        scroll-behavior: smooth;
        font-size: 16px;
        line-height: 1.6;
    }
    
    body {
        background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%) !important;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
    
    /* DARK/LIGHT THEME SYSTEM - Excellent Visibility & Contrast */
    :root {
        /* Theme Toggle Variables */
        --is-dark: 0; /* 0 for light, 1 for dark */
        
        /* Primary Colors - Bright & Visible */
        --primary: #3B82F6;              /* Bright blue - visible in both themes */
        --primary-hover: #2563EB;        /* Darker blue for hover */
        --primary-light: #60A5FA;        /* Lighter blue */
        
        /* Accent Colors - High contrast */
        --accent-orange: #F97316;        /* Bright orange */
        --accent-green: #10B981;         /* Bright green */
        --accent-amber: #F59E0B;         /* Bright amber */
        --accent-red: #EF4444;           /* Bright red */
        
        /* Border Radius */
        --radius-sm: 0.25rem;
        --radius-md: 0.5rem; 
        --radius-lg: 0.75rem;
        --radius-xl: 1rem;
    }
    
    /* LIGHT THEME - Default */
    :root {
        --bg-primary: #FFFFFF;           /* Pure white */
        --bg-secondary: #F8FAFC;         /* Light gray */
        --bg-tertiary: #F1F5F9;          /* Lighter gray */
        --bg-sidebar: #F8FAFC;           /* Light sidebar */
        --bg-card: #FFFFFF;              /* White cards */
        --bg-hover: #F1F5F9;             /* Hover state */
        
        --text-primary: #0F172A;         /* Dark text */
        --text-secondary: #475569;       /* Medium text */
        --text-tertiary: #64748B;        /* Light text */
        --text-inverse: #FFFFFF;         /* White text */
        
        --border-primary: #E2E8F0;       /* Light borders */
        --border-secondary: #CBD5E1;     /* Medium borders */
        --border-focus: var(--primary);  /* Focus borders */
        
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        
        /* Badge Colors - Light Theme */
        --badge-info-bg: #DBEAFE;
        --badge-info-text: #1E40AF;
        --badge-success-bg: #D1FAE5;
        --badge-success-text: #065F46;
        --badge-warning-bg: #FEF3C7;
        --badge-warning-text: #92400E;
        --badge-error-bg: #FEE2E2;
        --badge-error-text: #991B1B;
    }
    
    /* REMOVED OLD DARK THEME CSS - Using direct injection instead */
    
    /* THEME TOGGLE BUTTON */
    .theme-toggle {
        position: fixed;
        top: 1rem;
        right: 1rem;
        z-index: 1000;
        background: var(--bg-card) !important;
        border: 2px solid var(--border-primary) !important;
        border-radius: var(--radius-lg) !important;
        padding: 0.75rem !important;
        box-shadow: var(--shadow-lg) !important;
        transition: all 0.2s ease !important;
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        cursor: pointer !important;
        min-width: 120px !important;
        text-align: center !important;
    }
    
    .theme-toggle:hover {
        background: var(--bg-hover) !important;
        border-color: var(--primary) !important;
        transform: translateY(-2px) !important;
        box-shadow: var(--shadow-xl) !important;
    }
    
    /* GLOBAL APP STYLING - Excellent Contrast with Proper Theme Support */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        background: var(--bg-primary) !important;
        color: var(--text-primary) !important;
        font-size: 16px;
        line-height: 1.6;
        transition: all 0.3s ease;
    }
    
    /* SIMPLIFIED THEMING - All theme switching now done via direct CSS injection */
    
    /* TYPOGRAPHY - High Contrast & Clear */
    .stApp h1, .stApp h2, .stApp h3 {
        color: var(--text-primary) !important;
        font-weight: 700 !important;
        letter-spacing: -0.025em;
        margin-bottom: 1rem;
    }
    
    .stApp h1 { font-size: 2.5rem !important; line-height: 1.2; }
    .stApp h2 { font-size: 2rem !important; line-height: 1.3; }
    .stApp h3 { font-size: 1.75rem !important; line-height: 1.4; }
    
    .stApp p, .stApp div, .stApp span {
        color: var(--text-secondary) !important;
        line-height: 1.6;
        font-weight: 500 !important;
        font-size: 16px !important;
    }
    
    .stApp strong {
        color: var(--text-primary) !important;
        font-weight: 700 !important;
    }
    
    /* BUTTONS - Super Visible & High Contrast */
    .stButton > button {
        background: var(--primary) !important;
        color: var(--text-inverse) !important;
        border: 2px solid var(--primary) !important;
        border-radius: var(--radius-lg) !important;
        padding: 1rem 2rem !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        transition: all 0.2s ease !important;
        box-shadow: var(--shadow-md) !important;
        min-height: 48px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    .stButton > button:hover {
        background: var(--primary-hover) !important;
        transform: translateY(-2px) !important;
        box-shadow: var(--shadow-lg) !important;
        border-color: var(--primary-hover) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0px) !important;
        box-shadow: var(--shadow-md) !important;
    }
    
    .stButton > button:focus {
        outline: 3px solid var(--primary) !important;
        outline-offset: 2px !important;
    }
    
    /* HEADER - Stunning Gradient with High Contrast */
    .main-header {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-hover) 100%);
        padding: 3rem 2rem;
        border-radius: var(--radius-xl);
        margin-bottom: 2rem;
        color: var(--text-inverse) !important;
        text-align: center;
        box-shadow: var(--shadow-lg);
        position: relative;
        overflow: hidden;
        border: 2px solid var(--border-primary);
    }
    
    .main-header h1 {
        color: var(--text-inverse) !important;
        font-size: 3rem !important;
        font-weight: 800 !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .main-header p {
        color: var(--text-inverse) !important;
        font-size: 1.25rem !important;
        font-weight: 500 !important;
        opacity: 0.95;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M 10 0 L 0 0 0 10" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="1"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
        opacity: 0.1;
    }
    
    .main-header h1 {
        position: relative;
        z-index: 1;
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        position: relative;
        z-index: 1;
        font-size: 1.2rem;
        opacity: 0.95;
    }
    
    /* RESULT CARDS - High Contrast & Clear Visibility */
    .result-card {
        border: 2px solid var(--border-primary);
        border-radius: var(--radius-xl);
        padding: 2rem;
        margin: 1.5rem 0;
        background: var(--bg-card) !important;
        box-shadow: var(--shadow-md);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .result-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 5px;
        height: 100%;
        background: linear-gradient(to bottom, var(--tonkin-secondary), var(--tonkin-accent));
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .result-card:hover {
        transform: translateY(-6px);
        box-shadow: var(--shadow-lg);
        border-color: var(--primary);
        background: var(--bg-hover) !important;
    }
    
    .result-card:hover::before {
        opacity: 1;
    }
    
    /* Mobile Responsive Adjustments */
    @media (max-width: 768px) {
        .result-card {
            padding: 1rem;
            margin: 0.75rem 0;
            border-radius: 12px;
        }
        
        .main-header {
            padding: 1.5rem;
            margin-bottom: 1rem;
        }
        
        .main-header h1 {
            font-size: 1.8rem;
        }
        
        .main-header p {
            font-size: 1rem;
        }
    }
    
    /* TRUST BADGES - Super Visible with High Contrast */
    .trust-badge {
        display: inline-flex;
        align-items: center;
        padding: 0.75rem 1.25rem;
        margin: 0.5rem;
        border-radius: var(--radius-lg);
        font-size: 0.875rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-family: 'Inter', sans-serif;
        box-shadow: var(--shadow-md);
        transition: all 0.2s ease;
        border: 2px solid transparent;
    }
    
    .trust-badge:hover {
        transform: translateY(-2px) scale(1.05);
        box-shadow: var(--shadow-lg);
    }
    
    /* HIGH CONTRAST BADGE COLORS */
    .badge-success, .badge-green { 
        background: var(--badge-success-bg) !important;
        color: var(--badge-success-text) !important;
        border-color: var(--accent-green);
    }
    .badge-info, .badge-blue { 
        background: var(--badge-info-bg) !important;
        color: var(--badge-info-text) !important;
        border-color: var(--primary);
    }
    .badge-warning, .badge-orange, .badge-gold { 
        background: var(--badge-warning-bg) !important;
        color: var(--badge-warning-text) !important;
        border-color: var(--accent-amber);
    }
    .badge-error { 
        background: var(--badge-error-bg) !important;
        color: var(--badge-error-text) !important;
        border-color: var(--accent-red);
    }
    .badge-purple { 
        background: #F3E8FF !important;
        color: #581C87 !important;
        border-color: #A855F7;
    }
    .badge-teal { 
        background: #CCFBF1 !important;
        color: #0F766E !important;
        border-color: var(--accent-green);
    }
    
    /* Mobile Badge Adjustments */
    @media (max-width: 768px) {
        .trust-badge {
            padding: 6px 12px;
            font-size: 11px;
            margin: 2px;
        }
    }
    
    /* Metadata Styling */
    .metadata-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 12px;
        margin: 15px 0;
        padding: 15px;
        background: #f8f9fa;
        border-radius: 10px;
    }
    
    .metadata-item {
        color: #495057;
        font-size: 14px;
    }
    
    .metadata-label {
        font-weight: 600;
        color: #1f4e79;
    }
    
    /* Modern Similarity Score - Clean Professional Design */
    .similarity-score {
        background: var(--tonkin-primary);
        color: var(--text-inverse);
        padding: 0.75rem 1.25rem;
        border-radius: var(--radius-lg);
        font-family: 'JetBrains Mono', 'SF Mono', 'Monaco', monospace;
        font-weight: 600;
        font-size: 1rem;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        box-shadow: var(--shadow-md);
        border: 1px solid var(--tonkin-primary);
        transition: all 0.15s ease-in-out;
    }
    
    .similarity-score:hover {
        transform: scale(1.05);
        box-shadow: var(--shadow-lg);
        background: var(--tonkin-primary-dark);
        border-color: var(--tonkin-primary-dark);
    }
    
    .similarity-score::before {
        content: '🎯';
        font-size: 1rem;
    }
    
    /* Mobile Score Adjustments */
    @media (max-width: 768px) {
        .similarity-score {
            padding: 8px 16px;
            font-size: 12px;
        }
    }
    
    /* Search Bar Enhancement */
    .search-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    
    /* Filter Panel */
    .filter-panel {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    /* Modern Stats Cards - Clean Professional Design */
    .stat-card {
        background: linear-gradient(135deg, var(--tonkin-primary) 0%, var(--tonkin-primary-dark) 100%);
        padding: 2rem;
        border-radius: var(--radius-xl);
        color: var(--text-inverse);
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: var(--shadow-lg);
        transition: all 0.2s ease-in-out;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .stat-card::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        pointer-events: none;
    }
    
    .stat-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-xl);
    }
    
    .stat-number {
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        font-family: 'Inter', sans-serif;
        position: relative;
        z-index: 1;
    }
    
    .stat-label {
        font-size: 1rem;
        opacity: 0.95;
        margin-top: 0.5rem;
        font-weight: 500;
        position: relative;
        z-index: 1;
    }
    
    /* Mobile Stats Adjustments */
    @media (max-width: 768px) {
        .stat-card {
            padding: 1.5rem;
        }
        
        .stat-number {
            font-size: 2rem;
        }
        
        .stat-label {
            font-size: 0.9rem;
        }
    }
    
    /* Action Buttons */
    .action-btn {
        background: linear-gradient(45deg, #1f4e79, #2980b9);
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 25px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .action-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(31, 78, 121, 0.4);
    }
    
    /* PROJECT TITLES - Maximum Visibility */
    .project-title {
        color: var(--text-primary) !important;
        font-size: 1.75rem !important;
        font-weight: 800 !important;
        margin-bottom: 1.5rem;
        border-left: 6px solid var(--primary);
        padding-left: 2rem;
        position: relative;
        line-height: 1.3;
        letter-spacing: -0.025em;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    }
    
    .collaboration-indicators {
        display: flex;
        gap: 12px;
        margin-top: 8px;
        flex-wrap: wrap;
    }
    
    .expert-indicator {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: var(--tonkin-gray-100);
        color: var(--text-secondary);
        padding: 0.5rem 1rem;
        border-radius: var(--radius-lg);
        font-size: 0.875rem;
        font-weight: 500;
        border: 1px solid var(--tonkin-gray-200);
        transition: all 0.15s ease-in-out;
        box-shadow: var(--shadow-sm);
    }
    
    .expert-indicator:hover {
        background: var(--tonkin-primary);
        color: var(--text-inverse);
        transform: translateY(-1px);
        box-shadow: var(--shadow-md);
        border-color: var(--tonkin-primary);
    }
    
    /* Mobile Project Title */
    @media (max-width: 768px) {
        .project-title {
            font-size: 1.2rem;
        }
        
        .collaboration-indicators {
            gap: 8px;
        }
        
        .expert-indicator {
            font-size: 11px;
            padding: 4px 8px;
        }
    }
    
    /* Snippet Text */
    .project-snippet {
        background: #f8f9fa;
        border-left: 3px solid #2980b9;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 10px 10px 0;
        font-style: italic;
        color: #495057;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_search_engine():
    """Get cached search engine instance."""
    return SemanticSearchEngine()

@st.cache_resource
def get_database():
    """Get cached database instance."""
    return KnowledgeDatabase()

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_all_projects():
    """Get all projects with caching."""
    db = get_database()
    return db.get_all_documents()

def create_dashboard():
    """Create dashboard with project statistics."""
    st.markdown("## 📊 Project Dashboard")
    
    projects = get_all_projects()
    df = pd.DataFrame(projects)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{len(projects)}</div>
            <div class="stat-label">Total Projects</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_score = df['trust_score'].mean()
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{avg_score:.2f}</div>
            <div class="stat-label">Avg Trust Score</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        regions = df['program_region'].nunique()
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{regions}</div>
            <div class="stat-label">Regions</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        categories = df['category'].nunique()
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{categories}</div>
            <div class="stat-label">Categories</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Projects by Region
        region_counts = df['program_region'].value_counts()
        fig1 = px.pie(
            values=region_counts.values,
            names=region_counts.index,
            title="📍 Projects by Region",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig1.update_layout(height=400)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Trust Score Distribution
        fig2 = px.histogram(
            df, 
            x='trust_score', 
            title="⭐ Trust Score Distribution",
            nbins=10,
            color_discrete_sequence=['#2980b9']
        )
        fig2.update_layout(height=400)
        st.plotly_chart(fig2, use_container_width=True)
    
    # Category breakdown
    category_counts = df['category'].value_counts()
    fig3 = px.bar(
        x=category_counts.index,
        y=category_counts.values,
        title="🏗️ Projects by Category",
        color=category_counts.values,
        color_continuous_scale='viridis'
    )
    fig3.update_xaxes(tickangle=45)
    fig3.update_layout(height=500, showlegend=False)
    st.plotly_chart(fig3, use_container_width=True)

def render_enhanced_result_card(result: Dict[str, Any], query: str, rank: int) -> None:
    """Render an enhanced result card with React-inspired professional styling."""
    
    # Professional Card Container Start
    st.markdown(f"""
    <div style="
        background: white;
        border: 2px solid #E2E8F0;
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    " class="result-card">
        <div style="position: absolute; top: 0; left: 0; width: 6px; height: 100%; background: linear-gradient(to bottom, #3B82F6, #10B981);"></div>
    """, unsafe_allow_html=True)
    
    # Project Number (Blue, Monospace)
    project_number = result.get('project_number', 'Unknown')
    project_name = result.get('project_name', 'Unknown Project')
    
    st.markdown(f"""
    <div style="margin-left: 1rem;">
        <div style="font-size: 0.875rem; font-weight: 600; color: #3B82F6; margin-bottom: 0.5rem; font-family: 'SF Mono', Monaco, monospace;">
            {project_number}
        </div>
        <h2 style="font-size: 1.5rem; font-weight: 700; color: #0F172A; margin: 0 0 0.75rem 0; line-height: 1.3;">
            {project_name}
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Main card container
    with st.container():
        # Top row: Similarity score and trust badges
        col1, col2 = st.columns([1, 3])
        
        with col1:
            # Trust Score as Progress Bar (React-style - NO EMOJIS)
            trust_score = result.get('trust_score', 0) * 100  # Convert to percentage
            
            # Color coding based on score
            if trust_score >= 90:
                bar_color = "linear-gradient(90deg, #10B981 0%, #059669 100%)"  # Green
                bar_label = "Excellent"
            elif trust_score >= 75:
                bar_color = "linear-gradient(90deg, #3B82F6 0%, #2563EB 100%)"  # Blue
                bar_label = "Good"
            elif trust_score >= 60:
                bar_color = "linear-gradient(90deg, #F59E0B 0%, #D97706 100%)"  # Orange
                bar_label = "Fair"
            else:
                bar_color = "linear-gradient(90deg, #EF4444 0%, #DC2626 100%)"  # Red
                bar_label = "Needs Review"
            
            st.markdown(f"""
            <div style="margin-bottom: 1rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <span style="font-size: 0.75rem; font-weight: 600; color: #64748B; text-transform: uppercase; letter-spacing: 0.5px;">Trust Score</span>
                    <span style="font-size: 1rem; font-weight: 700; color: #3B82F6;">{trust_score:.0f}%</span>
                </div>
                <div style="width: 100%; height: 12px; background: #E2E8F0; border-radius: 6px; overflow: hidden; position: relative;">
                    <div style="height: 100%; width: {trust_score}%; background: {bar_color}; border-radius: 6px; transition: width 0.8s ease;"></div>
                </div>
                <div style="text-align: center; font-size: 0.75rem; color: #64748B; margin-top: 0.25rem;">{bar_label}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Similarity Score as Progress Bar (React-style)
            similarity = result.get('similarity_score', 0) * 100  # Convert to percentage
            
            st.markdown(f"""
            <div style="margin-bottom: 1rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <span style="font-size: 0.75rem; font-weight: 600; color: #64748B; text-transform: uppercase; letter-spacing: 0.5px;">Relevance</span>
                    <span style="font-size: 1rem; font-weight: 700; color: #10B981;">{similarity:.0f}%</span>
                </div>
                <div style="width: 100%; height: 12px; background: #E2E8F0; border-radius: 6px; overflow: hidden; position: relative;">
                    <div style="height: 100%; width: {similarity}%; background: linear-gradient(90deg, #10B981 0%, #059669 100%); border-radius: 6px; transition: width 0.8s ease;"></div>
                </div>
                <div style="text-align: center; font-size: 0.75rem; color: #64748B; margin-top: 0.25rem;">Match Quality</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Professional Metadata Grid (React-style)
        st.markdown("""
        <div style="background: #F8FAFC; padding: 1.5rem; border-radius: 12px; border: 1px solid #F1F5F9; margin: 1rem 0;">
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div style="margin-bottom: 0.75rem;">
                <div style="font-size: 0.75rem; font-weight: 600; color: #64748B; text-transform: uppercase; margin-bottom: 0.25rem;">👤 Client</div>
                <div style="font-size: 0.95rem; color: #0F172A; font-weight: 600;">{result.get('client', 'N/A')}</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div>
                <div style="font-size: 0.75rem; font-weight: 600; color: #64748B; text-transform: uppercase; margin-bottom: 0.25rem;">📍 Region</div>
                <div style="font-size: 0.95rem; color: #0F172A; font-weight: 600;">{result.get('program_region', 'N/A')}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="margin-bottom: 0.75rem;">
                <div style="font-size: 0.75rem; font-weight: 600; color: #64748B; text-transform: uppercase; margin-bottom: 0.25rem;">📅 Timeline</div>
                <div style="font-size: 0.95rem; color: #0F172A; font-weight: 600;">{result.get('phase', 'N/A')}</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div>
                <div style="font-size: 0.75rem; font-weight: 600; color: #64748B; text-transform: uppercase; margin-bottom: 0.25rem;">💰 Budget</div>
                <div style="font-size: 0.95rem; color: #0F172A; font-weight: 600;">{result.get('budget', 'N/A')}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style="margin-bottom: 0.75rem;">
                <div style="font-size: 0.75rem; font-weight: 600; color: #64748B; text-transform: uppercase; margin-bottom: 0.25rem;">🎯 Category</div>
                <div style="font-size: 0.95rem; color: #0F172A; font-weight: 600;">{result.get('category', 'N/A')}</div>
            </div>
            """, unsafe_allow_html=True)
            
            disciplines = result.get('lead_disciplines', 'N/A')
            st.markdown(f"""
            <div>
                <div style="font-size: 0.75rem; font-weight: 600; color: #64748B; text-transform: uppercase; margin-bottom: 0.25rem;">🔧 Disciplines</div>
                <div style="font-size: 0.85rem; color: #0F172A; font-weight: 500;">{disciplines}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            # Status Badge
            status = result.get('status', 'Active')
            if status == 'Active':
                status_color = "#D1FAE5"
                status_text_color = "#065F46"
            elif status == 'Completed':
                status_color = "#DBEAFE"
                status_text_color = "#1E40AF"
            else:
                status_color = "#FEF3C7"
                status_text_color = "#92400E"
            
            st.markdown(f"""
            <div style="text-align: center; margin-top: 1rem;">
                <div style="
                    padding: 0.5rem 1rem;
                    background: {status_color};
                    color: {status_text_color};
                    border-radius: 20px;
                    font-size: 0.875rem;
                    font-weight: 600;
                    display: inline-block;
                ">{status}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Project snippet
        snippet = result.get('snippet', '')
        if snippet:
            highlighted_snippet = highlight_query_terms(snippet, query)
            st.markdown(f"""
            <div class="project-snippet">
                📄 <strong>Project Overview:</strong><br>
                {highlighted_snippet}
            </div>
            """, unsafe_allow_html=True)
        
        # Team Collaboration Section
        st.markdown("**👥 Team & Collaboration**")
        
        col1, col2 = st.columns(2)
        with col1:
            # Expert Contact Cards
            if result.get('project_leader') or result.get('project_reviewer'):
                st.markdown("**🎯 Contact Experts:**")
                
                if result.get('project_leader'):
                    if st.button(f"📞 Contact {result['project_leader']} (Leader)", key=f"contact_leader_{result['id']}", help="Connect with project leader"):
                        st.info(f"💼 {result['project_leader']} led this project. Contact via internal directory or Teams.")
                
                if result.get('project_reviewer'):
                    if st.button(f"📞 Contact {result['project_reviewer']} (Reviewer)", key=f"contact_reviewer_{result['id']}", help="Connect with project reviewer"):
                        st.info(f"✅ {result['project_reviewer']} reviewed this project. Great for technical questions!")
        
        with col2:
            # Project Sharing
            if st.button(f"📤 Share Project", key=f"share_{result['id']}", help="Share this project with team"):
                share_url = f"tonkin-kb://project/{result['id']}"
                st.success(f"📋 Project link copied! Share: {result['project_name']}")
                st.code(share_url)
        
        # Action buttons row
        col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 2])
        
        with col1:
            if st.button(f"📁 Open Document", key=f"open_{result['id']}", help="Open the original document"):
                file_path = result.get('file_path', '')
                if file_path and os.path.exists(file_path):
                    success = open_file(file_path)
                    if success:
                        st.success("✅ Document opened!")
                    else:
                        st.error("❌ Failed to open document")
                else:
                    st.warning("⚠️ Document file not found")
        
        with col2:
            if st.button("👍", key=f"thumbs_up_{result['id']}", help="Mark as helpful"):
                db = get_database()
                db.store_feedback(result['id'], st.session_state.get('last_query', ''), 'thumbs_up')
                st.success("👍 Thanks!")
        
        with col3:
            if st.button("👎", key=f"thumbs_down_{result['id']}", help="Mark as not helpful"):
                db = get_database()
                db.store_feedback(result['id'], st.session_state.get('last_query', ''), 'thumbs_down')
                st.info("👎 Noted")
        
        with col4:
            if st.button("💡", key=f"lesson_{result['id']}", help="Add lesson learned"):
                st.session_state[f'show_lesson_{result["id"]}'] = True
        
        with col5:
            # File info
            file_size = result.get('file_size', 0)
            modified_date = result.get('modified_date')
            if modified_date:
                rel_time = get_relative_time(modified_date)
                st.caption(f"📅 Modified {rel_time} • 💾 {format_file_size(file_size)}")
        
        # Professional Lesson Learned Input (React-style - One Line at Bottom)
        st.markdown("""
        <div style="margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid #E2E8F0;">
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.75rem;">
                <span style="font-size: 1rem; color: #F59E0B;">💡</span>
                <span style="font-size: 0.875rem; font-weight: 600; color: #475569; text-transform: uppercase; letter-spacing: 0.5px;">
                    ADD LESSON LEARNED / DECISION
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col_input, col_button = st.columns([4, 1])
        
        with col_input:
            lesson_text = st.text_input(
                "Lesson",
                key=f"lesson_input_{result['id']}",
                placeholder="Share a key insight or decision from this project...",
                label_visibility="collapsed"
            )
        
        with col_button:
            if st.button("➕ Add Lesson", key=f"add_lesson_{result['id']}", use_container_width=True):
                if lesson_text.strip():
                    db = get_database()
                    # Auto-tag with project metadata
                    phase = result.get('phase', 'Unknown')
                    leader = result.get('project_leader', 'Unknown')
                    tagged_lesson = f"[{phase}] {lesson_text.strip()} - {leader}"
                    db.store_feedback(result['id'], st.session_state.get('last_query', ''), 'lesson', tagged_lesson)
                    st.success("✅ Lesson saved and tagged!")
                    st.session_state[f'lesson_input_{result["id"]}'] = ""
                    st.rerun()
                else:
                    st.warning("Please enter a lesson")
        
        # Close card container
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("---")

def apply_filters(projects: List[Dict], filters: Dict) -> List[Dict]:
    """Apply filters to project list."""
    filtered = projects
    
    if filters.get('regions'):
        filtered = [p for p in filtered if p.get('program_region') in filters['regions']]
    
    if filters.get('categories'):
        filtered = [p for p in filtered if p.get('category') in filters['categories']]
    
    if filters.get('min_trust_score') is not None:
        filtered = [p for p in filtered if p.get('trust_score', 0) >= filters['min_trust_score']]
    
    if filters.get('leaders'):
        filtered = [p for p in filtered if p.get('project_leader') in filters['leaders']]
    
    return filtered

def main():
    """Enhanced main Streamlit application with dark/light theme toggle."""
    
    # Initialize theme in session state
    if 'dark_theme' not in st.session_state:
        st.session_state.dark_theme = False
    
    # Apply theme class to body using JavaScript
    theme_class = "dark-theme" if st.session_state.dark_theme else ""
    
    # Apply theme using direct CSS injection - MUCH MORE RELIABLE
    if st.session_state.dark_theme:
        st.markdown(f"""
        <style>
            /* FORCE DARK THEME ON ALL ELEMENTS */
            .stApp, .main, .block-container, div[data-testid="stAppViewContainer"] {{
                background-color: #0F172A !important;
                color: #F8FAFC !important;
            }}
            
            .stSidebar, .stSidebar > div {{
                background-color: #1E293B !important;
                color: #F8FAFC !important;
            }}
            
            /* Override all text elements for dark theme */
            .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {{
                color: #F8FAFC !important;
            }}
            
            .stApp p, .stApp div, .stApp span, .stApp label {{
                color: #CBD5E1 !important;
            }}
            
            .stMarkdown {{
                color: #F8FAFC !important;
            }}
            
            /* Dark theme form elements - FORCE WHITE BACKGROUNDS */
            .stTextInput > div > div > input,
            .stSelectbox > div > div,
            .stSelectbox > div > div > div,
            .stSelectbox div[data-baseweb="select"] > div,
            div[data-baseweb="select"] > div,
            div[data-testid="stSelectbox"] > div > div,
            .stSelectbox select {{
                background-color: #FFFFFF !important;
                color: #0F172A !important;
                border: 2px solid #3B82F6 !important;
                border-radius: 8px !important;
                padding: 0.75rem !important;
                font-weight: 500 !important;
                font-size: 14px !important;
            }}
            
            .stSelectbox > div > div:hover,
            div[data-baseweb="select"] > div:hover {{
                border-color: #2563EB !important;
                box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3) !important;
            }}
            
            /* Force selectbox dropdown options to be white too */
            .stSelectbox div[role="listbox"],
            .stSelectbox div[role="option"] {{
                background-color: #FFFFFF !important;
                color: #0F172A !important;
            }}
            
            /* Search example buttons - FORCE bright green styling in dark theme */
            .search-example-btn,
            div[data-testid="stExpander"] .stButton button,
            .stExpander .stButton button {{
                background-color: #10B981 !important;
                color: #FFFFFF !important;
                border: 2px solid #10B981 !important;
                border-radius: 20px !important;
                padding: 0.5rem 1rem !important;
                font-weight: 500 !important;
                font-size: 13px !important;
                margin: 0.25rem !important;
            }}
            
            .search-example-btn:hover,
            div[data-testid="stExpander"] .stButton button:hover,
            .stExpander .stButton button:hover {{
                background-color: #059669 !important;
                border-color: #059669 !important;
                transform: translateY(-1px) !important;
                box-shadow: 0 3px 10px rgba(16, 185, 129, 0.4) !important;
            }}
            
            /* Dark theme cards and containers */
            div[data-testid="stExpander"] {{
                background-color: #1E293B !important;
                border-color: #334155 !important;
            }}
            
            .result-card {{
                background-color: #1E293B !important;
                border-color: #334155 !important;
            }}
            
            /* Dark theme buttons - Bright and visible */
            .stButton button {{
                background-color: #3B82F6 !important;
                color: #FFFFFF !important;
                border: 2px solid #3B82F6 !important;
                border-radius: 8px !important;
                padding: 0.75rem 1.5rem !important;
                font-weight: 600 !important;
                font-size: 14px !important;
                transition: all 0.2s ease !important;
            }}
            
            .stButton button:hover {{
                background-color: #2563EB !important;
                border-color: #2563EB !important;
                transform: translateY(-1px) !important;
                box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4) !important;
            }}
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <style>
            /* FORCE LIGHT THEME ON ALL ELEMENTS */
            .stApp, .main, .block-container, div[data-testid="stAppViewContainer"] {{
                background-color: #FFFFFF !important;
                color: #0F172A !important;
            }}
            
            .stSidebar, .stSidebar > div {{
                background-color: #F8FAFC !important;
                color: #0F172A !important;
            }}
            
            /* Override all text elements for light theme */
            .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {{
                color: #0F172A !important;
            }}
            
            .stApp p, .stApp div, .stApp span, .stApp label {{
                color: #475569 !important;
            }}
            
            .stMarkdown {{
                color: #0F172A !important;
            }}
            
            /* Light theme form elements - FORCE WHITE BACKGROUNDS */
            .stTextInput > div > div > input,
            .stSelectbox > div > div,
            .stSelectbox > div > div > div,
            .stSelectbox div[data-baseweb="select"] > div,
            div[data-baseweb="select"] > div,
            div[data-testid="stSelectbox"] > div > div,
            .stSelectbox select {{
                background-color: #FFFFFF !important;
                color: #0F172A !important;
                border: 2px solid #3B82F6 !important;
                border-radius: 8px !important;
                padding: 0.75rem !important;
                font-weight: 500 !important;
                font-size: 14px !important;
                box-shadow: 0 1px 3px rgba(59, 130, 246, 0.1) !important;
            }}
            
            .stSelectbox > div > div:hover,
            div[data-baseweb="select"] > div:hover {{
                border-color: #2563EB !important;
                box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2) !important;
            }}
            
            /* Force selectbox dropdown options to be white too */
            .stSelectbox div[role="listbox"],
            .stSelectbox div[role="option"] {{
                background-color: #FFFFFF !important;
                color: #0F172A !important;
            }}
            
            /* Search example buttons - FORCE bright green styling in light theme */
            .search-example-btn,
            div[data-testid="stExpander"] .stButton button,
            .stExpander .stButton button {{
                background-color: #10B981 !important;
                color: #FFFFFF !important;
                border: 2px solid #10B981 !important;
                border-radius: 20px !important;
                padding: 0.5rem 1rem !important;
                font-weight: 500 !important;
                font-size: 13px !important;
                margin: 0.25rem !important;
                box-shadow: 0 1px 3px rgba(16, 185, 129, 0.2) !important;
            }}
            
            .search-example-btn:hover,
            div[data-testid="stExpander"] .stButton button:hover,
            .stExpander .stButton button:hover {{
                background-color: #059669 !important;
                border-color: #059669 !important;
                transform: translateY(-1px) !important;
                box-shadow: 0 3px 10px rgba(16, 185, 129, 0.3) !important;
            }}
            
            /* Light theme cards and containers */
            div[data-testid="stExpander"] {{
                background-color: #FFFFFF !important;
                border-color: #E2E8F0 !important;
            }}
            
            .result-card {{
                background-color: #FFFFFF !important;
                border-color: #E2E8F0 !important;
            }}
            
            /* Light theme buttons - Clean and professional */
            .stButton button {{
                background-color: #3B82F6 !important;
                color: #FFFFFF !important;
                border: 2px solid #3B82F6 !important;
                border-radius: 8px !important;
                padding: 0.75rem 1.5rem !important;
                font-weight: 600 !important;
                font-size: 14px !important;
                transition: all 0.2s ease !important;
                box-shadow: 0 2px 4px rgba(59, 130, 246, 0.1) !important;
            }}
            
            .stButton button:hover {{
                background-color: #2563EB !important;
                border-color: #2563EB !important;
                transform: translateY(-1px) !important;
                box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2) !important;
            }}
        </style>
        """, unsafe_allow_html=True)
    
    # Theme toggle in sidebar with enhanced styling
    with st.sidebar:
        st.markdown("---")
        theme_text = "🌞 Switch to Light Mode" if st.session_state.dark_theme else "🌙 Switch to Dark Mode"
        theme_emoji = "🌞" if st.session_state.dark_theme else "🌙"
        
        st.markdown(f"### {theme_emoji} **Theme Control**")
        
        # Big, visible theme toggle button
        if st.button(theme_text, key="theme_toggle", use_container_width=True):
            st.session_state.dark_theme = not st.session_state.dark_theme
            st.rerun()
        
        current_theme = "🌙 **Dark Theme Active**" if st.session_state.dark_theme else "☀️ **Light Theme Active**"
        
        if st.session_state.dark_theme:
            st.success(current_theme)
        else:
            st.info(current_theme)
        
        st.markdown("---")
    
    # Enhanced Professional Header (React-style)
    st.markdown("""
    <div class="main-header">
        <div style="display: flex; align-items: center; gap: 1.5rem;">
            <div style="font-size: 3rem;">🗄️</div>
            <div>
                <h1 style="margin: 0; font-size: 2.5rem; font-weight: 800; letter-spacing: -0.5px;">
                    Tonkin Knowledge Finder
                </h1>
                <p style="font-size: 1.125rem; margin: 0.5rem 0 0 0; opacity: 0.95; font-weight: 500;">
                    AI-Powered Project Intelligence & Expertise Discovery
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'search_results' not in st.session_state:
        st.session_state.search_results = []
    if 'last_query' not in st.session_state:
        st.session_state.last_query = ""
    if 'view_mode' not in st.session_state:
        st.session_state.view_mode = "Search"
    
    # Navigation tabs
    tab1, tab2 = st.tabs(["🔍 Search Projects", "📊 Dashboard"])
    
    with tab2:
        create_dashboard()
    
    with tab1:
        # Get all projects for filters
        all_projects = get_all_projects()
        df = pd.DataFrame(all_projects)
        
        # Sidebar with enhanced filters and stats
        with st.sidebar:
            st.markdown("### 🎛️ Search & Filter Options")
            
            # Quick stats
            search_engine = get_search_engine()
            index_stats = search_engine.get_index_stats()
            
            if index_stats.get('embeddings_exist', False):
                st.success(f"✅ {index_stats.get('total_documents', 0)} projects indexed")
            else:
                st.warning("⚠️ Search index not found")
            
            st.markdown("---")
            
            # Search settings
            st.markdown("#### 🔧 Search Settings")
            max_results = st.slider("Max Results", 5, 50, 15)
            similarity_threshold = st.slider("Similarity Threshold", 0.0, 1.0, 0.3, 0.05)
            
            st.markdown("---")
            
            # Advanced filters
            st.markdown("#### 🎯 Advanced Filters")
            
            # Region filter
            regions = sorted(df['program_region'].unique())
            selected_regions = st.multiselect("Regions", regions, help="Filter by Australian states/territories")
            
            # Category filter
            categories = sorted(df['category'].unique())
            selected_categories = st.multiselect("Project Categories", categories, help="Filter by project type")
            
            # Trust score filter
            min_trust_score = st.slider("Minimum Trust Score", 0.0, 1.0, 0.0, 0.05, help="Show only high-quality projects")
            
            # Project leader filter
            leaders = sorted(df['project_leader'].dropna().unique())
            selected_leaders = st.multiselect("Project Leaders", leaders, help="Filter by project leader")
            
            # Apply filters
            filters = {
                'regions': selected_regions,
                'categories': selected_categories,
                'min_trust_score': min_trust_score if min_trust_score > 0 else None,
                'leaders': selected_leaders
            }
            
            st.markdown("---")
            
            # Recent searches
            st.markdown("#### 🔍 Recent Searches")
            try:
                db = get_database()
                recent_searches = db.get_search_history(limit=5)
                for search in recent_searches:
                    if st.button(f"🔄 {search['query'][:25]}...", key=f"recent_{search['id']}", help=f"Search: {search['query']}"):
                        st.session_state.search_query = search['query']
                        st.rerun()
            except:
                st.info("No recent searches")
            
            st.markdown("---")
            
            # Team Expertise Finder
            st.markdown("#### 👥 Expert Finder")
            all_projects = get_all_projects()
            
            # Extract unique experts
            experts = set()
            for project in all_projects:
                if project.get('project_leader'):
                    experts.add(project['project_leader'])
                if project.get('project_reviewer'):
                    experts.add(project['project_reviewer'])
            
            if experts:
                expert_filter = st.selectbox("Find by expert:", ["All"] + sorted(list(experts)), key="expert_filter")
                if expert_filter != "All":
                    expert_projects = [p for p in all_projects 
                                     if p.get('project_leader') == expert_filter or p.get('project_reviewer') == expert_filter]
                    st.success(f"**{len(expert_projects)}** projects")
                    for proj in expert_projects[:2]:  # Show top 2
                        role = "Leader" if proj.get('project_leader') == expert_filter else "Reviewer"
                        if st.button(f"📋 {proj['project_name'][:15]}... ({role})", key=f"expert_proj_{proj['id']}", use_container_width=True):
                            st.session_state.search_results = [proj]
                            st.session_state.last_query = f"projects by {expert_filter}"
                            st.rerun()
            
            st.markdown("---")
            
            # Quick Topics
            st.markdown("#### 🔥 Quick Search")
            quick_topics = ["Stormwater", "Bridges", "Water Treatment", "Energy"]
            
            for topic in quick_topics:
                if st.button(f"{topic}", key=f"quick_{topic}", help=f"Search {topic} projects", use_container_width=True):
                    st.session_state.search_query = topic.lower()
                    st.rerun()
        
        # Main search interface
        st.markdown("""
        <div class="search-container">
        """, unsafe_allow_html=True)
        
        st.markdown("### 🔍 Search Projects")
        
        # Search input with enhanced styling
        search_query = st.text_input(
            "Enter your search query:",
            value=st.session_state.get('search_query', ''),
            placeholder="e.g., stormwater detention SA, bridge design NSW, renewable energy projects",
            help="Use natural language to describe what you're looking for",
            label_visibility="collapsed"
        )
        
        # Search examples in expandable section
        with st.expander("💡 Search Examples & Tips"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                **🏗️ By Project Type:**
                - `stormwater management SA`
                - `bridge design NSW`
                - `renewable energy projects`
                - `water treatment facilities`
                - `smart city infrastructure`
                """)
            
            with col2:
                st.markdown("""
                **👥 By People & Criteria:**
                - `projects by Sarah Mitchell`
                - `high quality infrastructure`
                - `recent approved designs`
                - `Melbourne metro projects`
                - `coastal protection works`
                """)
        
        # Search button
        search_clicked = st.button("🔍 Search Projects", type="primary", use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Perform search
        if search_clicked and search_query.strip():
            st.session_state.last_query = search_query
            
            with st.spinner("🔍 Searching projects..."):
                try:
                    search_engine = get_search_engine()
                    results = search_engine.search(search_query, top_k=max_results, threshold=similarity_threshold)
                    
                    # Apply additional filters
                    if any(filters.values()):
                        results = apply_filters(results, filters)
                    
                    st.session_state.search_results = results
                    
                except Exception as e:
                    st.error(f"❌ Search error: {str(e)}")
                    st.session_state.search_results = []
        
        # Display results with React-style instant feedback
        if st.session_state.search_results:
            results = st.session_state.search_results
            query = st.session_state.last_query
            total_indexed = len(all_projects)
            
            # React-Style Instant Feedback Stats Bar
            st.markdown(f"""
            <div style="
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 1rem 1.5rem;
                background: white;
                border-radius: 12px;
                margin: 1.5rem 0;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                border: 1px solid #E2E8F0;
            ">
                <div style="display: flex; align-items: center; gap: 0.75rem;">
                    <div style="font-size: 1.5rem; color: #10B981;">✅</div>
                    <div>
                        <div style="font-size: 1.25rem; font-weight: 700; color: #0F172A;">{len(results)}</div>
                        <div style="font-size: 0.875rem; color: #64748B; font-weight: 500;">Results Found</div>
                    </div>
                </div>
                
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span style="font-weight: 500; color: #475569;">Searching for:</span>
                    <span style="font-weight: 700; color: #3B82F6;">"{query}"</span>
                </div>
                
                <div style="display: flex; align-items: center; gap: 0.75rem;">
                    <div style="font-size: 1.5rem; color: #64748B;">📊</div>
                    <div>
                        <div style="font-size: 1.25rem; font-weight: 700; color: #0F172A;">{total_indexed}</div>
                        <div style="font-size: 0.875rem; color: #64748B; font-weight: 500;">Indexed Projects</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if len(results) > 0:
                # Sort options (compact)
                sort_option = st.selectbox(
                    "📊 Sort by:",
                    ["Relevance (similarity)", "Trust Score", "Date (newest)", "Project Name"],
                    help="Choose how to order the results",
                    label_visibility="collapsed"
                )
                
                # Apply sorting
                if "Trust" in sort_option:
                    results = sorted(results, key=lambda x: x.get('trust_score', 0), reverse=True)
                elif "Date" in sort_option:
                    results = sorted(results, key=lambda x: x.get('modified_date', ''), reverse=True)
                elif "Name" in sort_option:
                    results = sorted(results, key=lambda x: x.get('project_name', ''))
                
                st.markdown("---")
                
                # Render enhanced result cards
                for i, result in enumerate(results, 1):
                    render_enhanced_result_card(result, query, i)
            
            else:
                st.warning("🔍 No results found. Try different keywords, lower the similarity threshold, or adjust your filters.")
        
        elif search_query and search_clicked:
            st.info("👆 Click the Search button to find projects.")
        
        else:
            # Show some featured projects when no search
            st.markdown("### ⭐ Featured High-Quality Projects")
            
            featured = sorted(all_projects, key=lambda x: x.get('trust_score', 0), reverse=True)[:3]
            
            for i, project in enumerate(featured, 1):
                st.markdown(f"**{i}. {project.get('project_name')}**")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.caption(f"🌏 {project.get('program_region')}")
                with col2:
                    st.caption(f"🏗️ {project.get('category')}")
                with col3:
                    st.caption(f"⭐ {project.get('trust_score', 0):.2f} trust score")
                
                if st.button(f"View Project", key=f"featured_{project['id']}"):
                    st.session_state.search_results = [project]
                    st.session_state.last_query = project.get('project_name', '')
                    st.rerun()
                
                st.markdown("---")
    
    # Enhanced footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 2rem; background: #f8f9fa; border-radius: 10px; margin-top: 2rem;'>
        <h4 style='color: #1f4e79; margin-bottom: 1rem;'>🔍 Tonkin Knowledge Finder v2.0</h4>
        <p style='color: #666; margin: 0;'>
            🚀 Powered by AI Semantic Search • 🏗️ 23 Engineering Projects • 🌏 8 Australian Regions<br>
            📚 Built with Streamlit, sentence-transformers, and FAISS • 💡 Find. Learn. Build Better.
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
