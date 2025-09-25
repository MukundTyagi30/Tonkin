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
    page_title="🔍 Tonkin Knowledge Finder",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS for modern UI with Tonkin branding
st.markdown("""
<style>
    /* Import Tonkin-style fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Main App Styling */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Enhanced Tonkin Brand Colors - Better Contrast & Readability */
    :root {
        --tonkin-primary: #1e3a8a;      /* Rich blue - easier to read */
        --tonkin-secondary: #3b82f6;     /* Bright blue - good contrast */
        --tonkin-accent: #f59e0b;        /* Warm amber - better than orange */
        --tonkin-background: #f8fafc;    /* Soft white background */
        --tonkin-surface: #ffffff;       /* Pure white cards */
        --tonkin-gray-light: #f1f5f9;    /* Light gray borders */
        --tonkin-gray-medium: #64748b;   /* Medium gray text */
        --tonkin-gray-dark: #1e293b;     /* Dark gray headings */
        --tonkin-success: #059669;       /* Emerald green */
        --tonkin-warning: #d97706;       /* Amber warning */
        --tonkin-error: #dc2626;         /* Red error */
        --tonkin-shadow: rgba(0, 0, 0, 0.1);
        --tonkin-shadow-lg: rgba(0, 0, 0, 0.15);
    }
    
    /* Global Typography & Background */
    .stApp {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, var(--tonkin-background) 0%, #e2e8f0 100%);
        color: var(--tonkin-gray-dark);
    }
    
    /* Better text readability */
    .stApp h1, .stApp h2, .stApp h3 {
        color: var(--tonkin-gray-dark);
        font-weight: 600;
    }
    
    .stApp p, .stApp div {
        color: var(--tonkin-gray-medium);
        line-height: 1.6;
    }
    
    /* Header Styling - Enhanced Visual Appeal */
    .main-header {
        background: linear-gradient(135deg, var(--tonkin-primary) 0%, var(--tonkin-secondary) 100%);
        padding: 3rem;
        border-radius: 24px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 20px 40px var(--tonkin-shadow-lg);
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.2);
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
    
    /* Enhanced Result Card - Better Visual Hierarchy */
    .result-card {
        border: 1px solid var(--tonkin-gray-light);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        background: var(--tonkin-surface);
        box-shadow: 0 8px 25px var(--tonkin-shadow);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
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
        box-shadow: 0 20px 50px var(--tonkin-shadow-lg);
        border-color: var(--tonkin-secondary);
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
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
    
    /* Trust Badges - Enhanced Visual Design */
    .trust-badge {
        display: inline-flex;
        align-items: center;
        padding: 10px 16px;
        margin: 6px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        color: white;
        text-transform: uppercase;
        letter-spacing: 0.3px;
        font-family: 'Inter', sans-serif;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        transition: all 0.2s ease;
        border: 2px solid rgba(255, 255, 255, 0.2);
    }
    
    .trust-badge:hover {
        transform: translateY(-2px) scale(1.05);
        box-shadow: 0 6px 20px rgba(0,0,0,0.2);
    }
    
    .badge-green { 
        background: linear-gradient(135deg, var(--tonkin-success) 0%, #10b981 100%);
        border-color: rgba(255, 255, 255, 0.3);
    }
    .badge-blue { 
        background: linear-gradient(135deg, var(--tonkin-primary) 0%, var(--tonkin-secondary) 100%);
        border-color: rgba(255, 255, 255, 0.3);
    }
    .badge-orange { 
        background: linear-gradient(135deg, var(--tonkin-accent) 0%, #f59e0b 100%);
        color: var(--tonkin-gray-dark);
        border-color: rgba(0, 0, 0, 0.1);
    }
    .badge-purple { 
        background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
        border-color: rgba(255, 255, 255, 0.3);
    }
    .badge-teal { 
        background: linear-gradient(135deg, #14b8a6 0%, #0d9488 100%);
        border-color: rgba(255, 255, 255, 0.3);
    }
    .badge-gold { 
        background: linear-gradient(135deg, var(--tonkin-warning) 0%, #b45309 100%);
        color: white;
        border-color: rgba(255, 255, 255, 0.3);
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
    
    /* Similarity Score - Enhanced Visibility */
    .similarity-score {
        background: linear-gradient(135deg, var(--tonkin-primary) 0%, var(--tonkin-secondary) 100%);
        color: white;
        padding: 12px 24px;
        border-radius: 25px;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 600;
        font-size: 16px;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        box-shadow: 0 6px 20px var(--tonkin-shadow-lg);
        border: 2px solid rgba(255, 255, 255, 0.3);
        transition: all 0.2s ease;
    }
    
    .similarity-score:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 25px rgba(30, 58, 138, 0.3);
    }
    
    .similarity-score::before {
        content: '🎯';
        font-size: 14px;
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
    
    /* Stats Cards - Enhanced Visual Appeal */
    .stat-card {
        background: linear-gradient(135deg, var(--tonkin-primary) 0%, var(--tonkin-secondary) 100%);
        padding: 2.5rem;
        border-radius: 24px;
        color: white;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 12px 40px var(--tonkin-shadow-lg);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.2);
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
        transform: translateY(-6px) scale(1.02);
        box-shadow: 0 20px 60px rgba(30, 58, 138, 0.25);
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
    
    /* Project Title with Enhanced Typography */
    .project-title {
        color: var(--tonkin-gray-dark);
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        border-left: 5px solid var(--tonkin-secondary);
        padding-left: 1.5rem;
        position: relative;
        line-height: 1.3;
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
        gap: 8px;
        background: linear-gradient(135deg, var(--tonkin-gray-light) 0%, #e2e8f0 100%);
        color: var(--tonkin-gray-dark);
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        border: 1px solid var(--tonkin-gray-light);
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px var(--tonkin-shadow);
    }
    
    .expert-indicator:hover {
        background: linear-gradient(135deg, var(--tonkin-secondary) 0%, var(--tonkin-primary) 100%);
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
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
    """Render an enhanced result card with modern styling and team collaboration features."""
    
    # Project title with rank and collaboration indicators
    project_name = result.get('project_name', 'Unknown Project')
    
    # Team collaboration indicators
    collaboration_html = ""
    if result.get('project_leader'):
        collaboration_html += f'<span class="expert-indicator" title="Project Leader">👤 {result["project_leader"]}</span>'
    if result.get('project_reviewer'):
        collaboration_html += f'<span class="expert-indicator" title="Project Reviewer">✅ {result["project_reviewer"]}</span>'
    
    st.markdown(f"""
    <div class="project-title">
        #{rank} {project_name}
        <div class="collaboration-indicators">
            {collaboration_html}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Main card container
    with st.container():
        # Top row: Similarity score and trust badges
        col1, col2 = st.columns([1, 3])
        
        with col1:
            similarity = result.get('similarity_score', 0)
            st.markdown(f"""
            <div class="similarity-score">
                Score: {similarity:.3f}
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Trust badges
            doc_badges = create_trust_badges(result)
            if doc_badges:
                badge_html = ""
                for badge in doc_badges:
                    color_class = f"badge-{badge.get('color', 'blue')}"
                    icon = badge.get('icon', '')
                    text = badge.get('text', '')
                    badge_html += f'<span class="trust-badge {color_class}">{icon} {text}</span>'
                st.markdown(badge_html, unsafe_allow_html=True)
        
        # Metadata in clean columns instead of HTML
        st.markdown("**📋 Project Details**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if result.get('project_number'):
                st.markdown(f"**Project Number:** {result.get('project_number')}")
            if result.get('program_region'):
                st.markdown(f"**Region:** {result.get('program_region')}")
            if result.get('category'):
                st.markdown(f"**Category:** {result.get('category')}")
        
        with col2:
            if result.get('client'):
                st.markdown(f"**Client:** {result.get('client')}")
            if result.get('project_leader'):
                st.markdown(f"**Project Leader:** {result.get('project_leader')}")
            if result.get('project_reviewer'):
                st.markdown(f"**Project Reviewer:** {result.get('project_reviewer')}")
        
        with col3:
            if result.get('lead_disciplines'):
                st.markdown(f"**Lead Disciplines:** {result.get('lead_disciplines')}")
            if result.get('trust_score'):
                st.markdown(f"**Trust Score:** {result.get('trust_score', 0):.2f}/1.00")
        
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
        
        # Lesson learned input
        if st.session_state.get(f'show_lesson_{result["id"]}', False):
            with st.expander("💡 Add Lesson Learned", expanded=True):
                lesson_text = st.text_area(
                    "What did you learn from this project?",
                    key=f"lesson_input_{result['id']}",
                    placeholder="Share insights, best practices, or lessons learned..."
                )
                
                col_save, col_cancel = st.columns(2)
                with col_save:
                    if st.button("💾 Save Lesson", key=f"save_lesson_{result['id']}"):
                        if lesson_text.strip():
                            db = get_database()
                            db.store_feedback(result['id'], st.session_state.get('last_query', ''), 'lesson', lesson_text.strip())
                            st.success("✅ Lesson saved!")
                            st.session_state[f'show_lesson_{result["id"]}'] = False
                            st.rerun()
                        else:
                            st.warning("Please enter a lesson learned")
                
                with col_cancel:
                    if st.button("❌ Cancel", key=f"cancel_lesson_{result['id']}"):
                        st.session_state[f'show_lesson_{result["id"]}'] = False
                        st.rerun()
        
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
    """Enhanced main Streamlit application."""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🔍 Tonkin Knowledge Finder</h1>
        <p style="font-size: 1.2rem; margin: 0; opacity: 0.9;">
            Find trusted past projects using AI-powered semantic search
        </p>
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
        
        # Display results
        if st.session_state.search_results:
            results = st.session_state.search_results
            query = st.session_state.last_query
            
            st.markdown(f"## 📋 Search Results ({len(results)} found)")
            
            if len(results) > 0:
                st.success(f"Found **{len(results)}** relevant projects for '*{query}*'")
                
                # Sort options
                sort_option = st.selectbox(
                    "📊 Sort by:",
                    ["Relevance (similarity)", "Trust Score ⭐", "Date (newest first) 📅", "Project Name 📝"],
                    help="Choose how to order the results"
                )
                
                # Apply sorting
                if sort_option.startswith("Trust Score"):
                    results = sorted(results, key=lambda x: x.get('trust_score', 0), reverse=True)
                elif sort_option.startswith("Date"):
                    results = sorted(results, key=lambda x: x.get('modified_date', ''), reverse=True)
                elif sort_option.startswith("Project Name"):
                    results = sorted(results, key=lambda x: x.get('project_name', ''))
                
                # Results summary
                avg_score = sum(r.get('similarity_score', 0) for r in results) / len(results)
                avg_trust = sum(r.get('trust_score', 0) for r in results) / len(results)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Avg Similarity", f"{avg_score:.3f}")
                with col2:
                    st.metric("Avg Trust Score", f"{avg_trust:.2f}")
                with col3:
                    unique_regions = len(set(r.get('program_region') for r in results))
                    st.metric("Regions Found", unique_regions)
                
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
