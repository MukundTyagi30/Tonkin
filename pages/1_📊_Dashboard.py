"""
Tonkin Knowledge Finder - Dashboard Page
Real-time statistics and analytics from the knowledge base
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path
from datetime import datetime
import sqlite3

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from database import KnowledgeDatabase

# PAGE CONFIG
st.set_page_config(
    page_title="Dashboard | Tonkin Knowledge Finder",
    page_icon="📊",
    layout="wide"
)

# APPLY SAME CSS AS MAIN APP
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    }
    
    #MainMenu, footer, header {
        display: none !important;
    }
    
    .main .block-container {
        padding: 2rem !important;
        max-width: 1400px !important;
        margin: 0 auto !important;
    }
    
    h1 {
        color: #0F172A !important;
        font-weight: 800 !important;
        font-size: 2.5rem !important;
        margin-bottom: 2rem !important;
    }
    
    h2 {
        color: #0F172A !important;
        font-weight: 700 !important;
        font-size: 1.5rem !important;
        margin: 2rem 0 1rem 0 !important;
        padding-bottom: 0.75rem !important;
        border-bottom: 3px solid #1E40AF !important;
    }
    
    /* ═══════════════════════════════════════════════════════════ */
    /*                    SIDEBAR NAVIGATION STYLING              */
    /* ═══════════════════════════════════════════════════════════ */
    
    /* Sidebar navigation - CLEAN MINIMALIST DESIGN */
    [data-testid="stSidebarNav"] {
        background: transparent !important;
        padding: 0 !important;
        margin: 0 0 2rem 0 !important;
        border: none !important;
    }
    
    [data-testid="stSidebarNav"] ul {
        padding: 0 !important;
        gap: 0.5rem !important;
        display: flex !important;
        flex-direction: column !important;
    }
    
    /* Clean navigation links */
    [data-testid="stSidebarNav"] a {
        background: white !important;
        color: #475569 !important;
        font-weight: 600 !important;
        padding: 1rem 1.25rem !important;
        border-radius: 10px !important;
        margin: 0 !important;
        border: 2px solid #E2E8F0 !important;
        transition: all 0.2s ease !important;
        font-size: 0.95rem !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
    }
    
    /* Hover state - subtle */
    [data-testid="stSidebarNav"] a:hover {
        background: #F1F5F9 !important;
        border-color: #CBD5E1 !important;
        color: #0F172A !important;
        transform: translateX(2px) !important;
    }
    
    /* Active page - solid navy blue */
    [data-testid="stSidebarNav"] a[aria-current="page"] {
        background: #1E40AF !important;
        color: white !important;
        border-color: #1E40AF !important;
        font-weight: 700 !important;
        box-shadow: 0 2px 8px rgba(30, 64, 175, 0.25) !important;
    }
    
    /* Icons */
    [data-testid="stSidebarNav"] a span {
        font-size: 1.15rem !important;
    }
    
    /* Remove dividers */
    [data-testid="stSidebarNav"] hr {
        display: none !important;
    }
    
    .stat-card {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        border: 2px solid #E2E8F0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
    }
    
    .stat-value {
        font-size: 3rem;
        font-weight: 800;
        font-family: 'JetBrains Mono', monospace;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        font-size: 0.875rem;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
</style>
""", unsafe_allow_html=True)

def get_database_stats():
    """Get real statistics from the database"""
    try:
        db = KnowledgeDatabase()
        
        # Get total projects (documents)
        documents = db.get_all_documents()
        total_projects = len(documents)
        
        # Get total documents (from embeddings)
        conn = sqlite3.connect(db.db_path)
        cursor = conn.cursor()
        
        # Count embeddings
        cursor.execute("SELECT COUNT(*) FROM embeddings")
        total_embeddings = cursor.fetchone()[0]
        
        # Get unique experts (project leaders and reviewers from documents table)
        cursor.execute("""
            SELECT COUNT(DISTINCT project_leader) + COUNT(DISTINCT project_reviewer) 
            FROM documents 
            WHERE project_leader IS NOT NULL OR project_reviewer IS NOT NULL
        """)
        expert_count = cursor.fetchone()[0]
        total_experts = expert_count if expert_count else 0
        
        # Calculate average trust score from documents table
        cursor.execute("SELECT AVG(trust_score) FROM documents WHERE trust_score IS NOT NULL AND trust_score > 0")
        avg_trust = cursor.fetchone()[0]
        avg_trust_score = round(avg_trust * 100, 1) if avg_trust else 0
        
        # Get feedback count
        cursor.execute("SELECT COUNT(*) FROM feedback")
        total_feedback = cursor.fetchone()[0]
        
        # Get recent searches count
        cursor.execute("SELECT COUNT(*) FROM search_history")
        total_searches = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_projects': total_projects,
            'total_documents': total_embeddings,
            'total_experts': total_experts,
            'avg_trust_score': avg_trust_score,
            'total_feedback': total_feedback,
            'total_searches': total_searches
        }
    except Exception as e:
        st.error(f"Error loading statistics: {str(e)}")
        return {
            'total_projects': 0,
            'total_documents': 0,
            'total_experts': 0,
            'avg_trust_score': 0,
            'total_feedback': 0,
            'total_searches': 0
        }

def main():
    # HEADER
    st.markdown("# 📊 Knowledge Base Dashboard")
    st.markdown("Real-time statistics and insights from the Tonkin Knowledge Finder")
    
    # Get real stats
    stats = get_database_stats()
    
    # MAIN STATISTICS
    st.markdown("## Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card" style="border-color: #93C5FD;">
            <div class="stat-value" style="color: #1E40AF;">{stats['total_projects']}</div>
            <div class="stat-label">Total Projects</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card" style="border-color: #6EE7B7;">
            <div class="stat-value" style="color: #065F46;">{stats['total_documents']}</div>
            <div class="stat-label">Documents Indexed</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card" style="border-color: #A5B4FC;">
            <div class="stat-value" style="color: #3730A3;">{stats['total_experts']}</div>
            <div class="stat-label">Experts</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stat-card" style="border-color: #FCD34D;">
            <div class="stat-value" style="color: #92400E;">{stats['avg_trust_score']}%</div>
            <div class="stat-label">Avg Trust Score</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # USAGE STATISTICS
    st.markdown("## Usage Statistics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card" style="border-color: #C7D2FE;">
            <div class="stat-value" style="color: #4338CA;">{stats['total_searches']}</div>
            <div class="stat-label">Total Searches</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card" style="border-color: #A7F3D0;">
            <div class="stat-value" style="color: #047857;">{stats['total_feedback']}</div>
            <div class="stat-label">Feedback Received</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        engagement_rate = round((stats['total_feedback'] / stats['total_searches'] * 100) if stats['total_searches'] > 0 else 0, 1)
        st.markdown(f"""
        <div class="stat-card" style="border-color: #FDBA74;">
            <div class="stat-value" style="color: #C2410C;">{engagement_rate}%</div>
            <div class="stat-label">Engagement Rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # PROJECT DETAILS
    st.markdown("## Project Details")
    
    try:
        db = KnowledgeDatabase()
        documents = db.get_all_documents()
        
        if documents:
            # Create DataFrame
            df = pd.DataFrame(documents)
            
            # Select and display relevant columns
            display_columns = []
            for col in ['project_number', 'project_name', 'client', 'program_region', 'trust_score', 'category']:
                if col in df.columns:
                    display_columns.append(col)
            
            if display_columns:
                st.dataframe(
                    df[display_columns],
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Trust Score Distribution
            st.markdown("## Trust Score Distribution")
            if 'trust_score' in df.columns:
                trust_counts = {
                    'Excellent (90-100%)': len(df[df['trust_score'] >= 0.9]),
                    'Good (75-89%)': len(df[(df['trust_score'] >= 0.75) & (df['trust_score'] < 0.9)]),
                    'Fair (60-74%)': len(df[(df['trust_score'] >= 0.6) & (df['trust_score'] < 0.75)]),
                    'Needs Review (<60%)': len(df[df['trust_score'] < 0.6])
                }
                
                col1, col2, col3, col4 = st.columns(4)
                cols = [col1, col2, col3, col4]
                colors = ['#10B981', '#3B82F6', '#F59E0B', '#EF4444']
                
                for i, (label, count) in enumerate(trust_counts.items()):
                    with cols[i]:
                        st.markdown(f"""
                        <div class="stat-card">
                            <div class="stat-value" style="color: {colors[i]};">{count}</div>
                            <div class="stat-label">{label}</div>
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.info("No projects found in the database. Run the ingestion script to populate the knowledge base.")
    
    except Exception as e:
        st.error(f"Error loading project details: {str(e)}")
    
    # REFRESH BUTTON
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Refresh Dashboard", type="primary"):
        st.rerun()

if __name__ == "__main__":
    main()

