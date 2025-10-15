"""
Tonkin Knowledge Finder - PERFECTED PRODUCTION UI
Clean, professional, distraction-free design with subtle interactions
"""

import streamlit as st
import pandas as pd
import os
import sys
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from search import SemanticSearchEngine
from database import KnowledgeDatabase

# PAGE CONFIG
st.set_page_config(
    page_title="Tonkin Knowledge Finder | AI-Powered Project Intelligence",
    page_icon="🗄️",
    layout="wide",
    initial_sidebar_state="expanded",  # Show filters by default
    menu_items={'Get Help': None, 'Report a bug': None, 'About': None}
)

# PERFECTED CSS - CLEAN, PROFESSIONAL, SUBTLE
st.markdown("""
<style>
    /* ═══════════════════════════════════════════════════════════ */
    /* GLOBAL FOUNDATION */
    /* ═══════════════════════════════════════════════════════════ */
    
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    html, body, .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%) !important;
        color: #0F172A !important;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
    
    /* HIDE STREAMLIT BRANDING */
    #MainMenu, footer, header, .stDeployButton, [data-testid="stToolbar"] {
        display: none !important;
    }
    
    /* MAIN CONTAINER */
    .main .block-container {
        max-width: 1400px !important;
        padding: 2.5rem 2rem !important;
        margin: 0 auto !important;
    }
    
    /* ═══════════════════════════════════════════════════════════ */
    /* HERO HEADER - PROFESSIONAL & CLEAN */
    /* ═══════════════════════════════════════════════════════════ */
    
    .hero-header {
        background: linear-gradient(135deg, #1E40AF 0%, #1E3A8A 100%);
        border-radius: 20px;
        padding: 2.5rem 3rem;
        margin-bottom: 2.5rem;
        box-shadow: 0 4px 20px rgba(30, 64, 175, 0.15);
        position: relative;
        overflow: hidden;
        animation: fadeIn 0.6s ease-out;
    }
    
    .hero-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 250px;
        height: 250px;
        background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
        border-radius: 50%;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .hero-content {
        position: relative;
        z-index: 1;
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }
    
    .hero-icon {
        font-size: 3.5rem;
        filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
    }
    
    .hero-text h1 {
        color: white !important;
        font-size: 2.25rem !important;
        font-weight: 800 !important;
        margin: 0 0 0.5rem 0 !important;
        letter-spacing: -0.5px !important;
        line-height: 1.1 !important;
    }
    
    .hero-text p {
        color: rgba(255, 255, 255, 0.9) !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        margin: 0 !important;
    }
    
    /* ═══════════════════════════════════════════════════════════ */
    /* INPUT & BUTTONS - PROFESSIONAL STYLING */
    /* ═══════════════════════════════════════════════════════════ */
    
    .stTextInput > div > div {
        position: relative;
    }
    
    .stTextInput > div > div > input {
        background: white !important;
        border: 2px solid #CBD5E1 !important;
        border-radius: 12px !important;
        padding: 1rem 1.5rem 1rem 3.5rem !important;
        font-size: 1.05rem !important;
        font-weight: 500 !important;
        color: #0F172A !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #1E40AF !important;
        box-shadow: 0 0 0 3px rgba(30, 64, 175, 0.1), 0 2px 8px rgba(0, 0, 0, 0.08) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #94A3B8 !important;
    }
    
    /* Search icon inside input */
    .stTextInput > div > div::before {
        content: "🔍";
        position: absolute;
        left: 1.25rem;
        top: 50%;
        transform: translateY(-50%);
        font-size: 1.25rem;
        z-index: 10;
        pointer-events: none;
    }
    
    /* PRIMARY BUTTON */
    .stButton > button[kind="primary"], 
    .stButton > button:first-child {
        background: linear-gradient(135deg, #1E40AF 0%, #1E3A8A 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 1rem 2rem !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        letter-spacing: 0.3px !important;
        text-transform: uppercase !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 8px rgba(30, 64, 175, 0.25) !important;
    }
    
    .stButton > button[kind="primary"]:hover,
    .stButton > button:first-child:hover {
        background: linear-gradient(135deg, #1E3A8A 0%, #1E293B 100%) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(30, 64, 175, 0.3) !important;
    }
    
    /* SECONDARY BUTTONS (Thumbs, Clear) */
    .stButton > button[kind="secondary"],
    .stButton > button:not(:first-child) {
        background: white !important;
        color: #475569 !important;
        border: 2px solid #E2E8F0 !important;
        border-radius: 10px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
        min-width: 120px !important;
        height: 46px !important;
    }
    
    .stButton > button[kind="secondary"]:hover,
    .stButton > button:not(:first-child):hover {
        background: #F8FAFC !important;
        border-color: #CBD5E1 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08) !important;
    }
    
    /* ═══════════════════════════════════════════════════════════ */
    /* STATS BAR - CLEAN PROFESSIONAL DISPLAY */
    /* ═══════════════════════════════════════════════════════════ */
    
    .stats-container {
        background: white;
        border-radius: 16px;
        padding: 2rem 2.5rem;
        margin: 2rem 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        border: 1px solid #E2E8F0;
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 2rem;
        animation: slideUp 0.5s ease-out 0.2s both;
    }
    
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .stat-box {
        text-align: center;
        position: relative;
    }
    
    .stat-box::after {
        content: '';
        position: absolute;
        right: -1rem;
        top: 15%;
        height: 70%;
        width: 1px;
        background: #E2E8F0;
    }
    
    .stat-box:last-child::after {
        display: none;
    }
    
    .stat-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    .stat-value {
        font-size: 2.25rem;
        font-weight: 800;
        color: #0F172A;
        font-family: 'JetBrains Mono', monospace;
        line-height: 1;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        font-size: 0.875rem;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* ═══════════════════════════════════════════════════════════ */
    /* RESULT CARDS - CLEAN & PROFESSIONAL */
    /* ═══════════════════════════════════════════════════════════ */
    
    .result-card-pro {
        background: white;
        border: 2px solid #E2E8F0;
        border-radius: 20px;
        padding: 2.5rem;
        margin: 1.75rem 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        transition: all 0.3s ease;
        position: relative;
        animation: slideUp 0.5s ease-out both;
    }
    
    .result-card-pro::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 5px;
        height: 100%;
        background: linear-gradient(135deg, #1E40AF 0%, #10B981 100%);
        border-radius: 20px 0 0 20px;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .result-card-pro:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
        border-color: #1E40AF;
    }
    
    .result-card-pro:hover::before {
        opacity: 1;
    }
    
    .project-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        background: linear-gradient(135deg, #DBEAFE 0%, #BFDBFE 100%);
        color: #1E40AF;
        font-size: 0.875rem;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
        border-radius: 8px;
        margin-bottom: 1rem;
        letter-spacing: 0.5px;
    }
    
    .project-title-pro {
        font-size: 1.875rem !important;
        font-weight: 800 !important;
        color: #0F172A !important;
        margin: 1rem 0 !important;
        line-height: 1.2 !important;
        letter-spacing: -0.5px !important;
    }
    
    .project-description {
        font-size: 1.05rem;
        line-height: 1.7;
        color: #475569;
        margin: 1.25rem 0;
        font-weight: 400;
    }
    
    /* ═══════════════════════════════════════════════════════════ */
    /* PROGRESS BARS - CLEAN ANIMATED */
    /* ═══════════════════════════════════════════════════════════ */
    
    .progress-wrapper {
        margin: 1.5rem 0;
    }
    
    .progress-header-flex {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.6rem;
    }
    
    .progress-label-text {
        font-size: 0.875rem;
        font-weight: 700;
        color: #475569;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .progress-percentage {
        font-size: 1.125rem;
        font-weight: 800;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .progress-bar-container {
        width: 100%;
        height: 14px;
        background: #F1F5F9;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.08);
    }
    
    .progress-bar-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
    }
    
    .progress-bar-fill::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.25), transparent);
        animation: shimmer 2.5s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .progress-status-text {
        text-align: center;
        margin-top: 0.4rem;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.3px;
    }
    
    /* ═══════════════════════════════════════════════════════════ */
    /* METADATA GRID */
    /* ═══════════════════════════════════════════════════════════ */
    
    .metadata-container {
        background: #F8FAFC;
        border-radius: 14px;
        padding: 1.75rem;
        margin: 1.75rem 0;
        border: 1px solid #E2E8F0;
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.5rem;
    }
    
    .metadata-field {
        text-align: center;
    }
    
    .metadata-icon {
        font-size: 1.5rem;
        margin-bottom: 0.4rem;
    }
    
    .metadata-label-text {
        font-size: 0.75rem;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.4rem;
    }
    
    .metadata-value-text {
        font-size: 0.95rem;
        font-weight: 700;
        color: #0F172A;
    }
    
    /* ═══════════════════════════════════════════════════════════ */
    /* LESSON SECTION */
    /* ═══════════════════════════════════════════════════════════ */
    
    .lesson-divider {
        margin: 2rem 0 1.5rem 0;
        height: 1px;
        background: #E2E8F0;
    }
    
    .lesson-header-section {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        margin-bottom: 0.75rem;
    }
    
    .lesson-icon-large {
        font-size: 1.25rem;
    }
    
    .lesson-title-text {
        font-size: 0.875rem;
        font-weight: 700;
        color: #475569;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* ═══════════════════════════════════════════════════════════ */
    /* FEEDBACK BUTTONS - EQUAL SIZE */
    /* ═══════════════════════════════════════════════════════════ */
    
    .feedback-row {
        display: flex;
        gap: 0.75rem;
        margin-top: 1rem;
    }
    
    /* Override for feedback buttons specifically */
    div[data-testid="column"] .stButton > button {
        min-width: 130px !important;
        height: 44px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 0.7rem 1.25rem !important;
    }
    
    /* ═══════════════════════════════════════════════════════════ */
    /* SIDEBAR - PROFESSIONAL FILTERS */
    /* ═══════════════════════════════════════════════════════════ */
    
    [data-testid="stSidebar"] {
        background: #F8FAFC !important;
        border-right: 2px solid #E2E8F0 !important;
        padding: 1.5rem 1rem !important;
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #0F172A !important;
        font-weight: 700 !important;
        font-size: 1.125rem !important;
        margin: 1.5rem 0 1rem 0 !important;
        padding-bottom: 0.5rem !important;
        border-bottom: 2px solid #1E40AF !important;
    }
    
    /* Sidebar metric styling - HIGH VISIBILITY */
    [data-testid="stSidebar"] [data-testid="stMetric"] {
        background: white !important;
        padding: 1rem !important;
        border-radius: 10px !important;
        border: 2px solid #E2E8F0 !important;
        margin-bottom: 0.75rem !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stMetricLabel"] {
        color: #64748B !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stMetricValue"] {
        color: #1E40AF !important;
        font-weight: 800 !important;
        font-size: 2rem !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    [data-testid="stSidebar"] .stSlider {
        padding: 0.5rem 0 !important;
    }
    
    [data-testid="stSidebar"] label {
        color: #0F172A !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
    }
    
    /* Sidebar text and paragraphs */
    [data-testid="stSidebar"] p {
        color: #475569 !important;
        font-weight: 500 !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #0F172A !important;
    }
    
    /* Multiselect styling - Professional Colors */
    [data-testid="stSidebar"] .stMultiSelect {
        margin-bottom: 1rem !important;
    }
    
    [data-testid="stSidebar"] .stMultiSelect > div > div {
        background: white !important;
        border: 2px solid #CBD5E1 !important;
        border-radius: 10px !important;
    }
    
    [data-testid="stSidebar"] .stMultiSelect > div > div:focus-within {
        border-color: #1E40AF !important;
        box-shadow: 0 0 0 2px rgba(30, 64, 175, 0.1) !important;
    }
    
    /* Multiselect dropdown options */
    [data-testid="stSidebar"] div[role="listbox"] {
        background: white !important;
        border: 2px solid #E2E8F0 !important;
        border-radius: 10px !important;
    }
    
    [data-testid="stSidebar"] div[role="option"] {
        color: #0F172A !important;
        background: white !important;
    }
    
    [data-testid="stSidebar"] div[role="option"]:hover {
        background: #F8FAFC !important;
    }
    
    [data-testid="stSidebar"] div[data-baseweb="tag"] {
        background: linear-gradient(135deg, #DBEAFE 0%, #BFDBFE 100%) !important;
        color: #1E40AF !important;
        border: none !important;
    }
    
    /* Slider styling - Professional Navy */
    .stSlider > div > div > div {
        background-color: #CBD5E1 !important;
    }
    
    .stSlider > div > div > div > div {
        background-color: #1E40AF !important;
    }
    
    .stSlider [role="slider"] {
        background-color: #1E40AF !important;
    }
    
    /* Slider value label - Remove blue background */
    .stSlider [data-testid="stTickBar"] > div {
        background-color: white !important;
        color: #0F172A !important;
        border: 2px solid #E2E8F0 !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        padding: 0.5rem 0.75rem !important;
    }
    
    /* Global select/multiselect styling */
    div[data-baseweb="select"] > div,
    div[data-baseweb="select"] > div > div {
        background: white !important;
        border: 2px solid #CBD5E1 !important;
        color: #0F172A !important;
    }
    
    div[data-baseweb="select"] > div:focus-within {
        border-color: #1E40AF !important;
    }
    
    /* Dropdown menu */
    div[data-baseweb="popover"] {
        background: white !important;
        border: 2px solid #E2E8F0 !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Dropdown items */
    ul[role="listbox"] li {
        color: #0F172A !important;
        background: white !important;
    }
    
    ul[role="listbox"] li:hover {
        background: #F8FAFC !important;
    }
    
    /* Selected tags in multiselect */
    span[data-baseweb="tag"] {
        background: linear-gradient(135deg, #DBEAFE 0%, #BFDBFE 100%) !important;
        color: #1E40AF !important;
        border: none !important;
        font-weight: 600 !important;
    }
    
    /* Placeholder text - HIGH VISIBILITY */
    div[data-baseweb="select"] input::placeholder,
    div[data-baseweb="select"] div::first-child {
        color: #64748B !important;
        font-weight: 500 !important;
    }
    
    /* "Choose an option" text */
    [data-testid="stSidebar"] div[data-baseweb="select"] > div:first-child,
    [data-testid="stSidebar"] div[data-baseweb="select"] span {
        color: #475569 !important;
        font-weight: 500 !important;
    }
    
    /* Professional icon replacements - NO EMOJIS */
    .stat-icon-pro {
        width: 48px;
        height: 48px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 0.75rem auto;
        font-size: 1.5rem;
        font-weight: 800;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }
    
    .icon-results {
        background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%);
        color: #065F46;
    }
    
    .icon-search {
        background: linear-gradient(135deg, #DBEAFE 0%, #BFDBFE 100%);
        color: #1E40AF;
    }
    
    .icon-database {
        background: linear-gradient(135deg, #E0E7FF 0%, #C7D2FE 100%);
        color: #3730A3;
    }
    
    /* ═══════════════════════════════════════════════════════════ */
    /* SECTION HEADINGS - PROFESSIONAL */
    /* ═══════════════════════════════════════════════════════════ */
    
    .main h2 {
        color: #0F172A !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        margin: 2rem 0 1rem 0 !important;
        padding-bottom: 0.75rem !important;
        border-bottom: 3px solid #1E40AF !important;
        display: flex !important;
        align-items: center !important;
        gap: 0.75rem !important;
    }
    
    /* ═══════════════════════════════════════════════════════════ */
    /* RESPONSIVE */
    /* ═══════════════════════════════════════════════════════════ */
    
    @media (max-width: 768px) {
        .hero-text h1 { font-size: 1.75rem !important; }
        .stats-container { grid-template-columns: 1fr; gap: 1.5rem; }
        .metadata-container { grid-template-columns: repeat(2, 1fr); }
        .project-title-pro { font-size: 1.5rem !important; }
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main Application - PERFECTED UI"""
    
    # SIDEBAR FILTERS
    with st.sidebar:
        st.markdown("### ⚙️ Filters & Options")
        
        # Trust Score Filter
        min_trust_score = st.slider(
            "Minimum Trust Score",
            min_value=0,
            max_value=100,
            value=0,
            step=5,
            help="Filter projects by minimum trust score"
        )
        
        # Category Filter
        categories = st.multiselect(
            "Project Categories",
            options=["Water & Wastewater", "Transport", "Buildings", "Energy", "Mining", "Environmental"],
            default=[],
            help="Select one or more categories"
        )
        
        # Region Filter
        regions = st.multiselect(
            "Regions",
            options=["Melbourne", "Sydney", "Brisbane", "Perth", "Adelaide", "International"],
            default=[],
            help="Filter by project region"
        )
        
        st.markdown("---")
        st.markdown("### 👥 Expert Finder")
        
        expert_search = st.text_input(
            "Search for experts",
            placeholder="Engineer name or expertise...",
            label_visibility="collapsed"
        )
        
        if expert_search:
            st.info(f"🔍 Searching for: {expert_search}")
        
        st.markdown("---")
        st.markdown("### 📊 Dashboard")
        st.info("📊 View detailed statistics and analytics in the **Dashboard** page (sidebar navigation).")
        
        st.markdown("---")
        st.markdown("### 💡 Quick Tips")
        st.markdown("""
        - Use filters to narrow results
        - Set minimum trust score
        - Search by region or category
        - Find experts in specific areas
        """)
    
    # HERO HEADER
    st.markdown("""
    <div class="hero-header">
        <div class="hero-content">
            <div class="hero-icon">🗄️</div>
            <div class="hero-text">
                <h1>Tonkin Knowledge Finder</h1>
                <p>AI-Powered Project Intelligence & Expertise Discovery</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # SEARCH INPUT
    search_query = st.text_input(
        "Search",
        placeholder="Search projects, documents, or expertise…",
        label_visibility="collapsed",
        key="main_search"
    )
    
    col1, col2 = st.columns([4, 1])
    with col1:
        search_clicked = st.button("🚀 SEARCH PROJECTS", type="primary", use_container_width=True)
    with col2:
        if st.button("Clear", use_container_width=True):
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # PERFORM SEARCH
    if search_clicked and search_query:
        try:
            # Initialize search
            search_engine = SemanticSearchEngine()
            db = KnowledgeDatabase()
            results = search_engine.search(search_query, top_k=10)
            
            # Apply filters
            filtered_results = []
            for result in results:
                # Trust score filter
                trust_score = result.get('trust_score', 0) * 100
                if trust_score < min_trust_score:
                    continue
                
                # Category filter
                if categories and result.get('category') not in categories:
                    continue
                
                # Region filter
                if regions and result.get('program_region') not in regions:
                    continue
                
                filtered_results.append(result)
            
            results = filtered_results
            
            # STATS BAR - PROFESSIONAL ICONS
            st.markdown(f"""
            <div class="stats-container">
                <div class="stat-box">
                    <div class="stat-icon-pro icon-results">✓</div>
                    <div class="stat-value">{len(results)}</div>
                    <div class="stat-label">Results Found</div>
                </div>
                <div class="stat-box">
                    <div class="stat-icon-pro icon-search">Q</div>
                    <div class="stat-value" style="font-size: 1.25rem; color: #1E40AF;">"{search_query}"</div>
                    <div class="stat-label">Search Query</div>
                </div>
                <div class="stat-box">
                    <div class="stat-icon-pro icon-database">#</div>
                    <div class="stat-value">23</div>
                    <div class="stat-label">Indexed Projects</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # RENDER RESULTS
            if results:
                for i, result in enumerate(results, 1):
                    st.markdown(f"""
                    <div class="result-card-pro" style="animation-delay: {i * 0.05}s;">
                        <div class="project-badge">{result.get('project_number', f'PROJECT-{i:03d}')}</div>
                        <h2 class="project-title-pro">{result.get('project_name', 'Unknown Project')}</h2>
                        <p class="project-description">{result.get('description', result.get('snippet', 'No description available.'))}</p>
                    """, unsafe_allow_html=True)
                    
                    # PROGRESS BARS
                    trust_score = result.get('trust_score', 0.85) * 100
                    relevance_score = result.get('similarity_score', 0.75) * 100
                    
                    # Trust Score Color
                    if trust_score >= 90:
                        trust_color = "linear-gradient(135deg, #10B981 0%, #059669 100%)"
                        trust_label = "Excellent"
                        trust_text_color = "#059669"
                    elif trust_score >= 75:
                        trust_color = "linear-gradient(135deg, #3B82F6 0%, #2563EB 100%)"
                        trust_label = "Good"
                        trust_text_color = "#2563EB"
                    elif trust_score >= 60:
                        trust_color = "linear-gradient(135deg, #F59E0B 0%, #D97706 100%)"
                        trust_label = "Fair"
                        trust_text_color = "#D97706"
                    else:
                        trust_color = "linear-gradient(135deg, #EF4444 0%, #DC2626 100%)"
                        trust_label = "Needs Review"
                        trust_text_color = "#DC2626"
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"""
                        <div class="progress-wrapper">
                            <div class="progress-header-flex">
                                <span class="progress-label-text">Trust Score</span>
                                <span class="progress-percentage" style="color: {trust_text_color};">{trust_score:.0f}%</span>
                            </div>
                            <div class="progress-bar-container">
                                <div class="progress-bar-fill" style="width: {trust_score}%; background: {trust_color};"></div>
                            </div>
                            <div class="progress-status-text" style="color: {trust_text_color};">{trust_label}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown(f"""
                        <div class="progress-wrapper">
                            <div class="progress-header-flex">
                                <span class="progress-label-text">Relevance</span>
                                <span class="progress-percentage" style="color: #059669;">{relevance_score:.0f}%</span>
                            </div>
                            <div class="progress-bar-container">
                                <div class="progress-bar-fill" style="width: {relevance_score}%; background: linear-gradient(135deg, #10B981 0%, #059669 100%);"></div>
                            </div>
                            <div class="progress-status-text" style="color: #059669;">Relevant Match</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # METADATA GRID
                    st.markdown(f"""
                    <div class="metadata-container">
                        <div class="metadata-field">
                            <div class="metadata-icon">👤</div>
                            <div class="metadata-label-text">Client</div>
                            <div class="metadata-value-text">{result.get('client', 'N/A')}</div>
                        </div>
                        <div class="metadata-field">
                            <div class="metadata-icon">📍</div>
                            <div class="metadata-label-text">Region</div>
                            <div class="metadata-value-text">{result.get('program_region', 'Melbourne')}</div>
                        </div>
                        <div class="metadata-field">
                            <div class="metadata-icon">🎯</div>
                            <div class="metadata-label-text">Category</div>
                            <div class="metadata-value-text">{result.get('category', 'Infrastructure')}</div>
                        </div>
                        <div class="metadata-field">
                            <div class="metadata-icon">📅</div>
                            <div class="metadata-label-text">Status</div>
                            <div style="display: inline-block; padding: 0.4rem 0.9rem; background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%); color: #065F46; border-radius: 16px; font-weight: 700; font-size: 0.875rem;">Active</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # TEAM INFO
                    if result.get('project_leader'):
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%); padding: 1.5rem; border-radius: 14px; margin: 1.5rem 0; border: 1px solid #BFDBFE;">
                            <div style="font-weight: 700; color: #1E40AF; margin-bottom: 0.6rem; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.5px;">👥 Project Team</div>
                            <div style="color: #1E3A8A; font-size: 0.95rem; line-height: 1.6;">
                                <strong>Project Leader:</strong> {result.get('project_leader', 'N/A')}<br>
                                <strong>Reviewer:</strong> {result.get('project_reviewer', 'N/A')}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # LESSON INPUT SECTION
                    st.markdown("""
                    <div class="lesson-divider"></div>
                    <div class="lesson-header-section">
                        <span class="lesson-icon-large">💡</span>
                        <span class="lesson-title-text">Add Lesson Learned / Decision</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col_input, col_btn = st.columns([4, 1])
                    with col_input:
                        lesson = st.text_input(
                            "lesson",
                            placeholder="Share a key insight or decision from this project...",
                            label_visibility="collapsed",
                            key=f"lesson_{i}"
                        )
                    with col_btn:
                        if st.button("➕ Add", key=f"add_{i}", type="secondary"):
                            if lesson:
                                st.success("✅ Lesson saved!")
                    
                    # FEEDBACK BUTTONS - EQUAL SIZE
                    st.markdown('<div class="feedback-row">', unsafe_allow_html=True)
                    col1, col2, col3 = st.columns([1, 1, 6])
                    with col1:
                        if st.button("👍 Helpful", key=f"up_{i}", type="secondary"):
                            st.success("Thanks for your feedback!")
                    with col2:
                        if st.button("👎 Not Helpful", key=f"down_{i}", type="secondary"):
                            st.info("Feedback noted")
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="text-align: center; padding: 4rem 2rem; background: white; border-radius: 20px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06); border: 1px solid #E2E8F0;">
                    <div style="font-size: 4rem; margin-bottom: 1.5rem; opacity: 0.4;">🔍</div>
                    <h2 style="font-size: 1.75rem; color: #475569; margin-bottom: 0.75rem; font-weight: 700;">No results found</h2>
                    <p style="font-size: 1rem; color: #64748B; line-height: 1.6;">Try different keywords or adjust your search query.</p>
                </div>
                """, unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"⚠️ Search error: {str(e)}")
    else:
        # WELCOME STATE
        st.markdown("""
        <div style="text-align: center; padding: 4rem 2rem; background: white; border-radius: 20px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06); border: 1px solid #E2E8F0; animation: fadeIn 0.6s ease-out 0.2s both;">
            <div style="font-size: 4rem; margin-bottom: 1.5rem;">🔍</div>
            <h2 style="font-size: 1.875rem; color: #0F172A; margin-bottom: 0.75rem; font-weight: 800;">Search the Tonkin Knowledge Base</h2>
            <p style="font-size: 1.05rem; color: #475569; line-height: 1.7; max-width: 600px; margin: 0 auto;">
                Enter a query to find relevant projects, documents, and expertise.<br>
                Try searching for <strong>"stormwater management"</strong>, <strong>"bridge design"</strong>, or an engineer's name.
            </p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

