"""
Tonkin Knowledge Finder - Streamlit Application

A local, offline prototype for finding trusted past projects by searching
SF84 Project Basis Reports using semantic search.
"""

import streamlit as st
import os
import sys
from pathlib import Path
from typing import List, Dict, Any

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
    page_title="Tonkin Knowledge Finder",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .result-card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 20px;
        margin: 10px 0;
        background-color: #f9f9f9;
    }
    .trust-badge {
        display: inline-block;
        padding: 4px 8px;
        margin: 2px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: bold;
        color: white;
    }
    .badge-green { background-color: #28a745; }
    .badge-blue { background-color: #007bff; }
    .badge-orange { background-color: #fd7e14; }
    .badge-purple { background-color: #6f42c1; }
    .badge-teal { background-color: #20c997; }
    .badge-gold { background-color: #ffc107; color: #000; }
    
    .metadata-row {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
        margin: 10px 0;
        font-size: 14px;
    }
    .metadata-item {
        color: #666;
    }
    .similarity-score {
        background-color: #e9ecef;
        padding: 4px 8px;
        border-radius: 4px;
        font-family: monospace;
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


def render_trust_badges(badges: List[Dict[str, str]]) -> str:
    """Render trust badges as HTML."""
    if not badges:
        return ""
    
    badge_html = ""
    for badge in badges:
        color_class = f"badge-{badge.get('color', 'blue')}"
        icon = badge.get('icon', '')
        text = badge.get('text', '')
        badge_html += f'<span class="trust-badge {color_class}">{icon} {text}</span>'
    
    return badge_html


def render_result_card(result: Dict[str, Any], query: str) -> None:
    """Render a single result card."""
    with st.container():
        # Title and similarity score
        col1, col2 = st.columns([3, 1])
        
        with col1:
            project_name = result.get('project_name', 'Unknown Project')
            st.subheader(f"📄 {project_name}")
        
        with col2:
            similarity = result.get('similarity_score', 0)
            st.markdown(
                f'<div class="similarity-score">Score: {similarity:.3f}</div>', 
                unsafe_allow_html=True
            )
        
        # Trust badges
        doc_badges = create_trust_badges(result)
        if doc_badges:
            badge_html = render_trust_badges(doc_badges)
            st.markdown(badge_html, unsafe_allow_html=True)
        
        # Metadata row
        metadata_items = []
        
        if result.get('project_number'):
            metadata_items.append(f"**Project #:** {result['project_number']}")
        
        if result.get('program_region'):
            metadata_items.append(f"**Region:** {result['program_region']}")
        
        if result.get('category'):
            metadata_items.append(f"**Category:** {result['category']}")
        
        if result.get('modified_date'):
            rel_time = get_relative_time(result['modified_date'])
            metadata_items.append(f"**Modified:** {rel_time}")
        
        if metadata_items:
            st.markdown(" | ".join(metadata_items))
        
        # People involved
        people = []
        if result.get('project_leader'):
            people.append(f"**Leader:** {result['project_leader']}")
        if result.get('project_reviewer'):
            people.append(f"**Reviewer:** {result['project_reviewer']}")
        if result.get('client'):
            people.append(f"**Client:** {result['client']}")
        
        if people:
            st.markdown(" | ".join(people))
        
        # Text snippet with highlighting
        snippet = result.get('snippet', '')
        if snippet:
            highlighted_snippet = highlight_query_terms(snippet, query)
            st.markdown(f"*{highlighted_snippet}*")
        
        # Action buttons
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        
        with col1:
            if st.button(f"📁 Open File", key=f"open_{result['id']}"):
                file_path = result.get('file_path', '')
                if file_path and os.path.exists(file_path):
                    success = open_file(file_path)
                    if success:
                        st.success("File opened!")
                    else:
                        st.error("Failed to open file")
                else:
                    st.error("File not found")
        
        with col2:
            if st.button("👍", key=f"thumbs_up_{result['id']}"):
                db = get_database()
                db.store_feedback(
                    result['id'], 
                    st.session_state.get('last_query', ''), 
                    'thumbs_up'
                )
                st.success("Thanks for the feedback!")
        
        with col3:
            if st.button("👎", key=f"thumbs_down_{result['id']}"):
                db = get_database()
                db.store_feedback(
                    result['id'], 
                    st.session_state.get('last_query', ''), 
                    'thumbs_down'
                )
                st.info("Feedback recorded")
        
        with col4:
            if st.button("💡 Lesson", key=f"lesson_{result['id']}"):
                st.session_state[f'show_lesson_{result["id"]}'] = True
        
        # Lesson learned input (appears when button clicked)
        if st.session_state.get(f'show_lesson_{result["id"]}', False):
            lesson_text = st.text_input(
                "Add a lesson learned:",
                key=f"lesson_input_{result['id']}",
                placeholder="What did you learn from this project?"
            )
            
            col_save, col_cancel = st.columns(2)
            with col_save:
                if st.button("Save Lesson", key=f"save_lesson_{result['id']}"):
                    if lesson_text.strip():
                        db = get_database()
                        db.store_feedback(
                            result['id'], 
                            st.session_state.get('last_query', ''), 
                            'lesson',
                            lesson_text.strip()
                        )
                        st.success("Lesson saved!")
                        st.session_state[f'show_lesson_{result["id"]}'] = False
                        st.rerun()
            
            with col_cancel:
                if st.button("Cancel", key=f"cancel_lesson_{result['id']}"):
                    st.session_state[f'show_lesson_{result["id"]}'] = False
                    st.rerun()
        
        st.markdown("---")


def main():
    """Main Streamlit application."""
    # Title and description
    st.title("🔍 Tonkin Knowledge Finder")
    st.markdown("*Find trusted past projects by searching SF84 reports using semantic search*")
    
    # Initialize session state
    if 'search_results' not in st.session_state:
        st.session_state.search_results = []
    if 'last_query' not in st.session_state:
        st.session_state.last_query = ""
    
    # Sidebar with stats and controls
    with st.sidebar:
        st.header("📊 System Status")
        
        # Get system stats
        try:
            db = get_database()
            stats = db.get_stats()
            
            search_engine = get_search_engine()
            index_stats = search_engine.get_index_stats()
            
            st.metric("Total Documents", stats.get('total_documents', 0))
            st.metric("Indexed Documents", index_stats.get('total_documents', 0))
            st.metric("Average Trust Score", f"{stats.get('avg_trust_score', 0):.2f}")
            
            # Index status
            if index_stats.get('embeddings_exist', False):
                st.success("✅ Search index ready")
            else:
                st.warning("⚠️ Search index not found")
                st.info("Run the ingestion script to create the index")
            
        except Exception as e:
            st.error(f"Error loading stats: {str(e)}")
        
        st.markdown("---")
        
        # Search options
        st.header("🔧 Search Options")
        max_results = st.slider("Max Results", 1, 20, 10)
        similarity_threshold = st.slider("Similarity Threshold", 0.0, 1.0, 0.3, 0.05)
        
        # Recent searches
        st.header("🔍 Recent Searches")
        try:
            recent_searches = db.get_search_history(limit=5)
            for search in recent_searches:
                if st.button(f"🔄 {search['query'][:30]}...", key=f"recent_{search['id']}"):
                    st.session_state.search_query = search['query']
                    st.rerun()
        except:
            st.info("No recent searches")
    
    # Main search interface
    st.header("🔍 Search Projects")
    
    # Search input
    search_query = st.text_input(
        "Enter your search query:",
        value=st.session_state.get('search_query', ''),
        placeholder="e.g., stormwater detention in SA, bridge design approved by client",
        help="Use natural language to describe what you're looking for"
    )
    
    # Search examples
    with st.expander("💡 Search Examples"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Project Types:**
            - Stormwater detention projects
            - Bridge design and construction
            - Water treatment facilities
            - Road and highway projects
            """)
        
        with col2:
            st.markdown("""
            **By Criteria:**
            - Projects in South Australia
            - Recent approved designs
            - Projects with specific clients
            - High-quality documented projects
            """)
    
    # Search button and logic
    col1, col2 = st.columns([1, 4])
    
    with col1:
        search_clicked = st.button("🔍 Search", type="primary")
    
    with col2:
        if search_query:
            st.info(f"💡 Searching for: *{search_query}*")
    
    # Perform search
    if search_clicked and search_query.strip():
        st.session_state.last_query = search_query
        
        with st.spinner("Searching documents..."):
            try:
                search_engine = get_search_engine()
                st.write(f"DEBUG: Searching for '{search_query}' with threshold {similarity_threshold}")
                # First get all results with low threshold to see scores
                all_results = search_engine.search(search_query, top_k=max_results, threshold=0.1)
                st.write(f"DEBUG: All results with scores:")
                for r in all_results:
                    st.write(f"  - {r['project_name']}: {r['similarity_score']:.3f}")
                
                results = search_engine.search(
                    search_query, 
                    top_k=max_results,
                    threshold=similarity_threshold
                )
                st.write(f"DEBUG: Found {len(results)} results with threshold {similarity_threshold}")
                st.session_state.search_results = results
                
            except Exception as e:
                st.error(f"Search error: {str(e)}")
                st.session_state.search_results = []
                import traceback
                st.code(traceback.format_exc())
    
    # Display results
    if st.session_state.search_results:
        results = st.session_state.search_results
        query = st.session_state.last_query
        
        st.header(f"📋 Results ({len(results)} found)")
        
        if len(results) > 0:
            st.success(f"Found {len(results)} relevant projects for '{query}'")
            
            # Sort options
            sort_option = st.selectbox(
                "Sort by:",
                ["Relevance (similarity)", "Trust Score", "Date (newest first)", "Project Name"]
            )
            
            # Apply sorting
            if sort_option == "Trust Score":
                results = sorted(results, key=lambda x: x.get('trust_score', 0), reverse=True)
            elif sort_option == "Date (newest first)":
                results = sorted(results, key=lambda x: x.get('modified_date', ''), reverse=True)
            elif sort_option == "Project Name":
                results = sorted(results, key=lambda x: x.get('project_name', ''))
            # Default is by relevance (already sorted by search engine)
            
            # Render result cards
            for result in results:
                render_result_card(result, query)
        
        else:
            st.warning("No results found. Try different keywords or lower the similarity threshold.")
    
    else:
        if search_query:
            st.info("Click the Search button to find projects.")
        else:
            st.info("Enter a search query above and click Search to find relevant projects.")
        
        # Debug info
        st.write(f"DEBUG: search_query='{search_query}', search_clicked={search_clicked}")
        st.write(f"DEBUG: session_state.search_results length = {len(st.session_state.get('search_results', []))}")
        st.write(f"DEBUG: session_state.last_query = '{st.session_state.get('last_query', '')}'")
        if hasattr(st.session_state, 'search_results'):
            st.write(f"DEBUG: search_results = {st.session_state.search_results}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 14px;'>
        Tonkin Knowledge Finder v1.0 | Local Semantic Search | 
        Built with Streamlit, sentence-transformers, and FAISS
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
