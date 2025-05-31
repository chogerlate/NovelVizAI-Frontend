#!/usr/bin/env python3
"""
Novel Companion AI - Streamlit Application
A comprehensive AI-driven reading assistant with intelligent chapter summarization,
dynamic character mapping, and interactive story companion features.
"""

import streamlit as st
import time
from datetime import datetime
from typing import Dict, List, Optional, Union, Any
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
import networkx as nx
from config import API_BASE_URL, API_TIMEOUT, MAX_CHAT_MESSAGES

from api.core import NovelCompanionAPIClient
from utils.css_engine import apply_css
# Initialize API client
api_client = NovelCompanionAPIClient()

# Configure page settings
st.set_page_config(
    page_title="Novel Companion AI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/chogerlate/NovelVizAI-Frontend',
        'Report a bug': "https://github.com/chogerlate/NovelVizAI-Frontend/issues",
        'About': "Novel Companion AI - Your intelligent reading assistant powered by advanced NLP and Large Language Models."
    }
)

def load_chapter_analysis(chapter_id: str, novel_id: str) -> Optional[Dict]:
    """Load chapter analysis data from API or local cache"""
    if not chapter_id:
        return None
    
    # Try to get from API first
    analysis = api_client.get_chapter_analysis(chapter_id)
    if analysis:
        return analysis
    
    # Convert API chapter data to analysis format if needed
    chapters = api_client.get_novel_chapters(novel_id)
    chapter = next((ch for ch in chapters if ch.get('id') == chapter_id), None)
    
    if chapter:
        return convert_api_chapter_to_analysis(chapter, novel_id)
    
    return None

def convert_api_chapter_to_analysis(chapter: Dict, novel_id: str) -> Dict:
    """Convert API chapter data to analysis format"""
    novel = api_client.get_novel_by_id(novel_id)
    
    return {
        "chapter_analysis": {
            "metadata": {
                "novel_id": novel_id,
                "chapter_id": chapter.get('id', ''),
                "novel_title": novel.get('title', 'Unknown') if novel else 'Unknown',
                "chapter_number": chapter.get('chapter_number', 0),
                "chapter_title": chapter.get('title', 'Unknown Chapter'),
                "word_count": chapter.get('word_count', 0),
                "estimated_reading_time": chapter.get('reading_time_minutes', 0),
                "is_processed": chapter.get('is_processed', False),
                "created_at": chapter.get('created_at', ''),
                "updated_at": chapter.get('updated_at', ''),
                "processing_timestamp": chapter.get('processing_timestamp', '')
            },
            "summary": {
                "concise": chapter.get('summary', 'No summary available.'),
                "detailed": chapter.get('summary', 'No detailed summary available.'),
                "key_events": chapter.get('key_events', [])
            },
            "sentiment_analysis": {
                "overall_tone": "Unknown",
                "sentiment_score": chapter.get('sentiment_score'),
                "emotional_arc": [],
                "character_sentiments": {}
            },
            "themes": [
                {"theme": theme, "relevance": 0.5, "evidence": "Analysis pending"}
                for theme in chapter.get('themes', [])
            ],
            "literary_elements": {
                "foreshadowing": [],
                "symbolism": []
            }
        },
        "character_mapping": {
            "characters": [
                {
                    "name": char,
                    "role": "Unknown",
                    "first_appearance": f"Chapter {chapter.get('chapter_number', 0)}",
                    "description": "Character analysis pending",
                    "key_traits": [],
                    "quotes": [],
                    "development_status": "Pending analysis"
                }
                for char in chapter.get('characters_mentioned', [])
            ],
            "relationships": [],
            "network_data": {"nodes": [], "links": []}
        },
        "interactive_companion": {
            "chapter_context": {
                "setting": "Unknown",
                "timeline_position": "Unknown",
                "narrative_importance": "Unknown"
            },
            "key_questions": [],
            "suggested_discussion_points": [],
            "vocabulary_notes": [],
            "cultural_context": []
        }
    }

def get_available_novels() -> List[Dict]:
    """Get list of available novels from API."""
    try:
        novels = api_client.get_novels(limit=50)
        return novels
    except Exception as e:
        st.error(f"Error fetching novels: {e}")
        return []

def get_novel_chapters(novel_id: str) -> List[Dict]:
    """Get chapters for a specific novel."""
    try:
        chapters = api_client.get_novel_chapters(novel_id, limit=100)
        return chapters
    except Exception as e:
        st.error(f"Error fetching chapters: {e}")
        return []

def initialize_session_state():
    if 'current_novel_id' not in st.session_state:
        st.session_state.current_novel_id = None
    if 'current_chapter_id' not in st.session_state:
        st.session_state.current_chapter_id = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'api_connection_status' not in st.session_state:
        st.session_state.api_connection_status = None

def create_header():
    """Create the main header section."""
    st.markdown('<h1 class="title-gradient">📚 Novel Companion AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Your intelligent reading assistant powered by advanced NLP and Large Language Models</p>', unsafe_allow_html=True)
    
    # Feature overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🔍 Chapter Analysis</h3>
            <p>Deep analysis with sentiment tracking, theme identification, and literary element detection.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>👥 Character Mapping</h3>
            <p>Dynamic character profiles with relationship networks and development tracking.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>🤖 AI Companion</h3>
            <p>Interactive AI assistant for deep literary discussions and contextual insights.</p>
        </div>
        """, unsafe_allow_html=True)

def create_sidebar():
    """Create the sidebar with novel selection and file upload."""
    with st.sidebar:
        # API Connection Status
        check_api_connection()
        
        st.markdown("## 📖 Novel Selection")
        
        # Novel selection
        available_novels = get_available_novels()
        novel_options = {}
        
        # Helper function for safe field access
        def safe_get(data: Dict, *keys) -> Any:
            """Safely get value from dict using multiple possible keys (including aliases)"""
            for key in keys:
                if key in data and data[key] is not None:
                    return data[key]
            return None
        
        for novel in available_novels:
            novel_title = safe_get(novel, 'title') or 'Unknown'
            novel_author = safe_get(novel, 'author') or ''
            novel_id = safe_get(novel, 'id', '_id') or ''
            novel_type = safe_get(novel, 'type') or ''
            novel_year = safe_get(novel, 'year')
            
            # Create a more informative display name
            display_parts = [novel_title]
            if novel_author:
                display_parts.append(f"by {novel_author}")
            if novel_year:
                display_parts.append(f"({novel_year})")
            if novel_type:
                display_parts.append(f"[{novel_type}]")
                
            display_name = " ".join(display_parts)
            novel_options[display_name] = novel_id
        
        if novel_options:
            selected_novel_display = st.selectbox(
                "Select Novel",
                list(novel_options.keys()),
                help="Choose a novel to analyze"
            )
            selected_novel_id = novel_options[selected_novel_display]
            
            # Update session state
            if st.session_state.current_novel_id != selected_novel_id:
                st.session_state.current_novel_id = selected_novel_id
                st.session_state.current_chapter_id = None  # Reset chapter selection
                st.rerun()
            
            # Chapter selection for the selected novel
            if selected_novel_id:
                chapters = get_novel_chapters(selected_novel_id)
                chapter_options = {}
                
                for chapter in chapters:
                    chapter_title = safe_get(chapter, 'title') or 'Unknown Chapter'
                    chapter_num = safe_get(chapter, 'chapter_number') or 0
                    chapter_id = safe_get(chapter, 'id', '_id') or ''
                    is_processed = safe_get(chapter, 'is_processed') or False
                    word_count = safe_get(chapter, 'word_count')
                    
                    # Create informative chapter display
                    display_parts = [f"Ch {chapter_num}: {chapter_title}"]
                    if word_count:
                        display_parts.append(f"({word_count:,} words)")
                    if is_processed:
                        display_parts.append("✓")
                    else:
                        display_parts.append("○")
                        
                    display_name = " ".join(display_parts)
                    chapter_options[display_name] = chapter_id
                
                if chapter_options:
                    selected_chapter_display = st.selectbox(
                        "Select Chapter",
                        list(chapter_options.keys()),
                        help="Choose a chapter to analyze (✓ = processed, ○ = pending)"
                    )
                    st.session_state.current_chapter_id = chapter_options[selected_chapter_display]
                else:
                    st.warning("No chapters found for this novel")
                    st.session_state.current_chapter_id = None
        else:
            st.warning("No novels found. Upload a novel to get started!")
            st.session_state.current_novel_id = None
            st.session_state.current_chapter_id = None
        
        st.markdown("---")
        
        # File upload section
        st.markdown("## 📤 Upload Novel")
        
        with st.form("upload_form"):
            uploaded_file = st.file_uploader(
                "Upload a text file",
                type=['txt', 'md'],
                help="Upload a novel for analysis"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                novel_title = st.text_input("Novel Title", placeholder="Enter title")
            with col2:
                novel_author = st.text_input("Author", placeholder="Enter author")
            
            # Additional novel metadata
            col1, col2 = st.columns(2)
            with col1:
                novel_type = st.selectbox("Type", ["Novel", "Light Novel", "Web Novel", "Short Story", "Other"], index=0)
            with col2:
                novel_year = st.number_input("Year", min_value=1800, max_value=2024, value=None, placeholder="Optional")
                
            novel_description = st.text_area("Description (Optional)", placeholder="Brief description of the novel")
            
            submit_button = st.form_submit_button("Upload Novel")
            
            if submit_button and uploaded_file:
                with st.spinner("Uploading novel..."):
                    file_content = uploaded_file.read()
                    
                    # Prepare upload data with new schema fields
                    upload_data = {
                        'title': novel_title or uploaded_file.name,
                        'author': novel_author,
                        'type': novel_type,
                        'description': novel_description
                    }
                    
                    if novel_year:
                        upload_data['year'] = novel_year
                    
                    result = api_client.upload_novel_file(
                        file_content=file_content,
                        filename=uploaded_file.name,
                        **upload_data
                    )
                    
                    if result:
                        st.success(f"✅ Uploaded {uploaded_file.name} successfully!")
                        st.success(f"Novel ID: {result.get('novel_id', 'Unknown')}")
                        
                        # Refresh the page to show new novel
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.error("Failed to upload novel")
        
        st.markdown("---")
        
        # Enhanced novel stats
        if st.session_state.current_novel_id:
            novel = api_client.get_novel_by_id(st.session_state.current_novel_id)
            if novel:
                st.markdown("## 📊 Novel Information")
                
                # Display novel metadata using safe_get
                novel_title = safe_get(novel, 'title')
                novel_author = safe_get(novel, 'author')
                novel_type = safe_get(novel, 'type')
                novel_year = safe_get(novel, 'year')
                novel_description = safe_get(novel, 'description')
                average_rating = safe_get(novel, 'average_rating', 'averageRating')
                vote_count = safe_get(novel, 'vote_count', 'voteCount')
                status_in_coo = safe_get(novel, 'status_in_coo', 'statusInCOO')
                genres = safe_get(novel, 'genres') or []
                tags = safe_get(novel, 'tags') or []
                
                # Basic info
                if novel_title:
                    st.markdown(f"**📚 {novel_title}**")
                if novel_author:
                    st.markdown(f"✍️ {novel_author}")
                if novel_type:
                    st.markdown(f"📖 {novel_type}")
                if novel_year:
                    st.markdown(f"📅 {novel_year}")
                
                # Ratings
                if average_rating is not None:
                    st.metric("⭐ Rating", f"{average_rating:.1f}/10")
                if vote_count:
                    st.metric("🗳️ Votes", f"{vote_count:,}")
                
                # Status
                if status_in_coo:
                    st.markdown(f"**Status:** {status_in_coo}")
                
                # Get chapters to calculate stats
                chapters = get_novel_chapters(st.session_state.current_novel_id)
                total_chapters = len(chapters)
                total_words = sum(safe_get(ch, 'word_count') or 0 for ch in chapters)
                processed_chapters = sum(1 for ch in chapters if safe_get(ch, 'is_processed'))
                estimated_reading_time = total_words / 200 if total_words > 0 else 0
                
                st.markdown("### 📈 Statistics")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Chapters", total_chapters)
                    st.metric("Processed", f"{processed_chapters}/{total_chapters}")
                with col2:
                    st.metric("Total Words", f"{total_words:,}")
                    st.metric("Est. Time", f"{estimated_reading_time:.0f} min")
                
                # Genres and tags
                if genres:
                    st.markdown("**🎭 Genres:**")
                    for genre in genres:
                        st.markdown(f"• {genre}")
                        
                if tags:
                    st.markdown("**🏷️ Tags:**")
                    # Display tags as badges
                    tags_html = ""
                    for tag in tags[:5]:  # Show first 5 tags
                        tags_html += f'<span class="theme-badge">{tag}</span>'
                    if len(tags) > 5:
                        tags_html += f'<span class="theme-badge">+{len(tags)-5} more</span>'
                    st.markdown(tags_html, unsafe_allow_html=True)
                
                # Description
                if novel_description:
                    st.markdown("**📝 Description:**")
                    st.markdown(f"*{novel_description[:200]}{'...' if len(novel_description) > 200 else ''}*")
                
                # Show current chapter stats if selected
                if st.session_state.current_chapter_id:
                    current_chapter = next((ch for ch in chapters if safe_get(ch, 'id', '_id') == st.session_state.current_chapter_id), None)
                    if current_chapter:
                        st.markdown("### 📝 Current Chapter")
                        chapter_word_count = safe_get(current_chapter, 'word_count')
                        chapter_reading_time = safe_get(current_chapter, 'reading_time_minutes')
                        chapter_is_processed = safe_get(current_chapter, 'is_processed')
                        
                        if chapter_word_count:
                            st.metric("Chapter Words", f"{chapter_word_count:,}")
                        if chapter_reading_time:
                            st.metric("Reading Time", f"{chapter_reading_time} min")
                        elif chapter_word_count:
                            st.metric("Est. Time", f"{(chapter_word_count / 200):.1f} min")
                        
                        # Processing status
                        status_color = "🟢" if chapter_is_processed else "🟡"
                        status_text = "Processed" if chapter_is_processed else "Pending Analysis"
                        st.markdown(f"{status_color} **Status:** {status_text}")
        
        # Quick actions
        st.markdown("---")
        st.markdown("### ⚡ Quick Actions")
        
        if st.button("🔄 Refresh Data"):
            # Clear cached data
            st.session_state.api_connection_status = None
            st.rerun()
        
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.success("Chat history cleared!")
            
        # Show API info
        st.markdown("---")
        st.markdown("### ℹ️ API Info")
        st.markdown(f"**Base URL:** `{API_BASE_URL}`")
        st.markdown(f"**Timeout:** {API_TIMEOUT}s")
        st.markdown(f"**Max Chat:** {MAX_CHAT_MESSAGES} messages")

def check_api_connection():
    """Check API connection status and display indicator."""
    if st.session_state.api_connection_status is None:
        try:
            # Test API connection
            response = api_client.session.get(f"{api_client.base_url}/", timeout=5)
            if response.status_code == 200:
                st.session_state.api_connection_status = "connected"
            else:
                st.session_state.api_connection_status = "error"
        except Exception:
            st.session_state.api_connection_status = "disconnected"
    
    # Display connection status
    if st.session_state.api_connection_status == "connected":
        st.success("🟢 API Connected")
    elif st.session_state.api_connection_status == "error":
        st.warning("🟡 API Error")
    else:
        st.error("🔴 API Disconnected")
        st.markdown(f"**API URL:** `{API_BASE_URL}`")
        if st.button("🔄 Retry Connection"):
            st.session_state.api_connection_status = None
            st.rerun()

def chapter_summarization_tab():
    """Create the chapter summarization interface."""
    st.markdown("## 📖 Intelligent Chapter Analysis")
    
    if not st.session_state.current_novel_id:
        st.warning("Please select a novel from the sidebar to begin analysis.")
        return
    
    if not st.session_state.current_chapter_id:
        st.warning("Please select a chapter from the sidebar to begin analysis.")
        return
    
    analysis = load_chapter_analysis(st.session_state.current_chapter_id, st.session_state.current_novel_id)
    if not analysis:
        st.error("Could not load chapter analysis data.")
        return
    
    # Safely get nested data with default empty dictionaries
    chapter_data = analysis.get('chapter_analysis', {})
    if not chapter_data:
        st.error("No chapter analysis data available.")
        return
        
    metadata = chapter_data.get('metadata', {})
    summary_data = chapter_data.get('summary', {})
    sentiment_data = chapter_data.get('sentiment_analysis', {})
    themes = chapter_data.get('themes', [])
    literary_elements = chapter_data.get('literary_elements', {})
    
    # Header with metadata and processing status
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"""
        <div class="summary-box">
            <h3>📝 {metadata.get('chapter_title', 'Unknown Chapter')}</h3>
            <p><strong>Novel:</strong> {metadata.get('novel_title', 'Unknown')}</p>
            <p><strong>Chapter {metadata.get('chapter_number', 0)}</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Check for actual content instead of is_processed flag
        has_summary = bool(summary_data.get('concise', '').strip())
        has_sentiment = bool(sentiment_data.get('overall_tone', '') or sentiment_data.get('sentiment_score') is not None)
        is_processed = has_summary and has_sentiment
        
        status_color = "🟢" if is_processed else "🟡"
        status_text = "Analysis Complete" if is_processed else "Analysis in Progress"
        st.markdown(f"""
        <div class="metric-card">
            <h4>Status</h4>
            <p>{status_color} {status_text}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Word count and reading time
        word_count = metadata.get('word_count', 0)
        reading_time = metadata.get('estimated_reading_time', 0)
        st.metric("Words", f"{word_count:,}" if word_count else "Unknown")
        st.metric("Est. Time", f"{reading_time:.1f} min" if reading_time else "Unknown")
    
    with col3:
        # Timestamps
        created_at = metadata.get('created_at')
        updated_at = metadata.get('updated_at')
        processing_timestamp = metadata.get('processing_timestamp')
        
        if created_at:
            st.markdown(f"**Created:** {created_at[:10] if isinstance(created_at, str) else 'Unknown'}")
        if updated_at:
            st.markdown(f"**Updated:** {updated_at[:10] if isinstance(updated_at, str) else 'Unknown'}")
        if processing_timestamp:
            st.markdown(f"**Processed:** {processing_timestamp[:10] if isinstance(processing_timestamp, str) else 'Unknown'}")
        
        if st.button("🔄 Refresh Analysis", type="primary"):
            st.rerun()
    
    # Show processing alert if not processed
    if not is_processed:
        st.info("🔄 This chapter is being analyzed. Some insights may be limited.")
    
    # Content preview section (new feature)
    content_preview = summary_data.get('content_preview')
    if content_preview:
        with st.expander("📄 Content Preview", expanded=False):
            st.markdown(f"""
            <div class="quote-box">
                {content_preview}
            </div>
            """, unsafe_allow_html=True)
    
    # Summary sections
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📝 Concise Summary")
        st.markdown(f"""
        <div class="summary-box">
            {summary_data.get('concise', 'No summary available.')}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🎯 Key Events")
        key_events = summary_data.get('key_events', [])
        if key_events:
            for i, event in enumerate(key_events, 1):
                st.markdown(f"{i}. {event}")
        else:
            st.info("No key events identified yet.")
    
    with col2:
        st.markdown("### 📖 Detailed Summary")
        st.markdown(f"""
        <div class="summary-box">
            {summary_data.get('detailed', 'No detailed summary available.')}
        </div>
        """, unsafe_allow_html=True)
    
    # Enhanced Sentiment Analysis
    st.markdown("### 🎭 Sentiment Analysis")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        overall_tone = sentiment_data.get('overall_tone', 'Unknown')
        sentiment_score = sentiment_data.get('sentiment_score')
        
        st.markdown(f"**Overall Tone:** {overall_tone}")
        if sentiment_score is not None:
            st.metric("Sentiment Score", f"{sentiment_score:.3f}")
            
            # Sentiment visualization
            score_color = "green" if sentiment_score > 0.1 else "red" if sentiment_score < -0.1 else "gray"
            st.markdown(f"""
            <div style="background: linear-gradient(90deg, red 0%, gray 50%, green 100%); height: 20px; border-radius: 10px; position: relative;">
                <div style="position: absolute; left: {((sentiment_score + 1) / 2) * 100}%; top: -5px; color: black; font-weight: bold;">●</div>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 0.8em; margin-top: 5px;">
                <span>Negative</span><span>Neutral</span><span>Positive</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Sentiment score not available for this chapter.")
    
    with col2:
        # Emotional arc visualization
        emotional_arc = sentiment_data.get('emotional_arc', [])
        if emotional_arc and len(emotional_arc) > 0:
            try:
                emotions_df = pd.DataFrame(emotional_arc)
                if not emotions_df.empty and 'emotion' in emotions_df.columns and 'intensity' in emotions_df.columns:
                    fig = px.bar(emotions_df, x='emotion', y='intensity', 
                                title="Emotional Intensity",
                                color='intensity',
                                color_continuous_scale='viridis',
                                height=300)
                    fig.update_layout(showlegend=False, margin=dict(l=0, r=0, t=30, b=0))
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Emotional arc data format not supported.")
            except Exception as e:
                st.info("Could not display emotional arc chart.")
        else:
            st.info("No emotional arc data available.")
    
    with col3:
        # Character sentiments
        char_sentiments = sentiment_data.get('character_sentiments', {})
        
        if char_sentiments:
            st.markdown("**👥 Character Emotions:**")
            for char_name, char_data in char_sentiments.items():
                # Handle different data structures
                if isinstance(char_data, dict):
                    dominant_emotions = char_data.get('dominant_emotions', [])
                    emotional_state = char_data.get('emotional_state', '')
                    
                    st.markdown(f"**{char_name}:**")
                    
                    # Display emotions as tags
                    if dominant_emotions:
                        emotions_html = ""
                        for emotion in dominant_emotions:
                            emotions_html += f'<span class="emotion-tag">{emotion}</span>'
                    st.markdown(emotions_html, unsafe_allow_html=True)
                    
                    # Display emotional state
                    if emotional_state:
                        st.markdown(f"*{emotional_state}*")
                else:
                    # Handle simple string format
                    st.markdown(f"**{char_name}:** {char_data}")
        else:
            st.info("No character sentiment data available for this chapter.")
            
            # Show emotional arc instead if available
            if emotional_arc:
                st.markdown("**📊 Overall Emotional Arc:**")
                for emotion_data in emotional_arc[:3]:  # Show top 3 emotions
                    if isinstance(emotion_data, dict):
                        emotion = emotion_data.get('emotion', 'Unknown')
                        intensity = emotion_data.get('intensity', 0)
                        if isinstance(intensity, (int, float)):
                            st.markdown(f"• **{emotion}:** {intensity:.1%} intensity")
                        else:
                            st.markdown(f"• **{emotion}:** {intensity}")
                    else:
                        st.markdown(f"• {emotion_data}")
            else:
                st.info("No emotional data available for this chapter.")
    
    # Themes
    st.markdown("### 🎨 Themes Analysis")
    if themes:
        theme_cols = st.columns(min(len(themes), 3))
        for i, theme in enumerate(themes):
            with theme_cols[i % len(theme_cols)]:
                if isinstance(theme, dict):
                    theme_name = theme.get('theme', 'Unknown Theme')
                    relevance = theme.get('relevance', 0)
                    evidence = theme.get('evidence', 'No evidence provided.')
                    
                    st.markdown(f"""
                    <div class="feature-card">
                        <h4>{theme_name}</h4>
                        <p><strong>Relevance:</strong> {relevance:.1%}</p>
                        <p>{evidence}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    # Handle simple string themes
                    st.markdown(f"""
                    <div class="feature-card">
                        <h4>{theme}</h4>
                        <p>Theme identified in chapter</p>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.info("No theme data available for this chapter.")
    
    # Enhanced Literary Elements
    st.markdown("### 🎭 Literary Elements")
    
    # Check if we have literary elements data
    if literary_elements:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔮 Foreshadowing")
            foreshadowing = literary_elements.get('foreshadowing', [])
            if foreshadowing:
                for item in foreshadowing:
                    if isinstance(item, dict):
                        text = item.get('text', '')
                        significance = item.get('significance', '')
                        st.markdown(f"""
                        <div class="quote-box">
                            "{text}"
                            <br><small><strong>Significance:</strong> {significance}</small>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        # Handle simple string format
                        st.markdown(f"""
                        <div class="quote-box">
                            "{item}"
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("No foreshadowing elements identified.")
        
        with col2:
            st.markdown("#### 🎨 Symbolism")
            symbolism = literary_elements.get('symbolism', [])
            if symbolism:
                for item in symbolism:
                    if isinstance(item, dict):
                        symbol = item.get('symbol', '')
                        meaning = item.get('meaning', '')
                        st.markdown(f"**{symbol}:** {meaning}")
                    else:
                        # Handle simple string format
                        st.markdown(f"• {item}")
            else:
                st.info("No symbolic elements identified.")
            
            # Display narrative voice if available
            narrative_voice = literary_elements.get('narrative_voice')
            if narrative_voice:
                st.markdown(f"**📝 Narrative Voice:** {narrative_voice}")
            
            # Display other literary elements if available
            other_elements = {k: v for k, v in literary_elements.items() 
                             if k not in ['foreshadowing', 'symbolism', 'narrative_voice']}
            if other_elements:
                st.markdown("#### 📚 Other Literary Elements")
                for element_name, element_value in other_elements.items():
                    if isinstance(element_value, list) and element_value:
                        st.markdown(f"**{element_name.title()}:**")
                        for item in element_value:
                            st.markdown(f"• {item}")
                    elif element_value:
                        st.markdown(f"**{element_name.title()}:** {element_value}")
    else:
        st.info("No literary elements data available for this chapter.")
    
    # Analysis actions
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔄 Regenerate Summary"):
            with st.spinner("Regenerating chapter summary..."):
                result = api_client.summarize_chapter(st.session_state.current_chapter_id, "detailed")
                if result:
                    st.success("Summary regenerated successfully!")
                    st.rerun()
                else:
                    st.error("Failed to regenerate summary.")
    
    with col2:
        if st.button("📊 Detailed Analysis"):
            st.info("Detailed analysis feature coming soon!")
    
    with col3:
        if st.button("💾 Export Analysis"):
            # Create downloadable analysis report
            analysis_text = f"""
# Chapter Analysis Report

## {metadata.get('novel_title', 'Unknown')} - Chapter {metadata.get('chapter_number', 0)}
### {metadata.get('chapter_title', 'Unknown Chapter')}

**Status:** {status_text}
**Word Count:** {word_count:,}
**Reading Time:** {reading_time:.1f} minutes

## Summary
{summary_data.get('detailed', 'No summary available.')}

## Key Events
{chr(10).join([f"• {event}" for event in key_events])}

## Themes
{chr(10).join([f"• {theme.get('theme', '')}: {theme.get('evidence', '')}" for theme in themes])}

## Sentiment: {overall_tone}
{f"Score: {sentiment_score:.3f}" if sentiment_score is not None else "Score: Not available"}

---
Generated by Novel Companion AI
"""
            
            st.download_button(
                label="📄 Download Report",
                data=analysis_text,
                file_name=f"chapter_{metadata.get('chapter_number', 0)}_analysis.txt",
                mime="text/plain"
            )
    
    with col4:
        # Debug data structure viewer
        with st.expander("🔍 Debug Data", expanded=False):
            st.markdown("**Raw Analysis Structure:**")
            st.json(analysis)

def character_mapping_tab():
    """Create the character mapping interface."""
    st.markdown("## 👥 Dynamic Character Mapping")
    
    if not st.session_state.current_novel_id:
        st.warning("Please select a novel from the sidebar to view character data.")
        return
    
    if not st.session_state.current_chapter_id:
        st.warning("Please select a chapter from the sidebar to view character data.")
        return
    
    analysis = load_chapter_analysis(st.session_state.current_chapter_id, st.session_state.current_novel_id)
    if not analysis:
        st.error("Could not load character analysis data.")
        return
    
    # Safely get nested data with default empty dictionaries
    character_data = analysis.get('character_mapping', {})
    if not character_data:
        st.error("No character mapping data available.")
        return
        
    characters = character_data.get('characters', [])
    relationships = character_data.get('relationships', [])
    network_data = character_data.get('network_data', {})
    
    if not characters:
        st.warning("No character data available for this chapter.")
        st.info("💡 Try selecting a different chapter or check if the chapter has been processed.")
        return
    
    # Color schemes for different relationship types and character roles (moved to top)
    relationship_colors = {
        'ally': '#2E8B57',      # Sea Green
        'enemy': '#DC143C',     # Crimson  
        'family': '#4169E1',    # Royal Blue
        'friend': '#32CD32',    # Lime Green
        'romantic': '#FF69B4',  # Hot Pink
        'mentor': '#9932CC',    # Dark Violet
        'rival': '#FF8C00',     # Dark Orange
        'neutral': '#708090',   # Slate Gray
        'unknown': '#A9A9A9',   # Dark Gray
        'colleagues': '#4682B4', # Steel Blue
        'protective': '#228B22', # Forest Green
        'opposition': '#8B0000', # Dark Red
        'direct communication': '#20B2AA', # Light Sea Green
        'direct interaction': '#FF6347', # Tomato
        'failed negotiation': '#B22222'  # Fire Brick
    }
    
    # Character role colors
    role_colors = {
        'protagonist': '#FFD700',    # Gold
        'antagonist': '#8B0000',     # Dark Red
        'supporting': '#4682B4',     # Steel Blue
        'minor': '#DDA0DD',          # Plum
        'narrator': '#20B2AA',       # Light Sea Green
        'background': '#D3D3D3',     # Light Gray
        'unknown': '#D3D3D3'         # Light Gray
    }
    
    # Character overview
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 📋 Character List")
        if characters:
            character_names = [char.get('name', 'Unknown') for char in characters]
            selected_character = st.radio(
                "Select Character",
                character_names,
                help="Choose a character to view detailed information"
            )
        else:
            st.warning("No character data available for this chapter.")
            st.info("💡 Try selecting a different chapter or check if the chapter has been processed.")
            return
        
        # Network stats
        st.markdown("### 📈 Network Stats")
        st.metric("Total Characters", len(characters))
        st.metric("Relationships", len(relationships))
        st.metric("Network Nodes", len(network_data.get('nodes', [])))
    
    with col2:
        # Selected character details
        selected_char_data = next((char for char in characters if char.get('name') == selected_character), None)
        
        if selected_char_data:
            st.markdown(f"""
            <div class="character-card">
                <h3>🎭 {selected_char_data.get('name', 'Unknown')}</h3>
                <p><strong>Role:</strong> {selected_char_data.get('role', 'Unknown')}</p>
                <p><strong>First Appearance:</strong> {selected_char_data.get('first_appearance', 'Unknown')}</p>
                <p><strong>Description:</strong> {selected_char_data.get('description', 'No description available.')}</p>
                <p><strong>Development Status:</strong> {selected_char_data.get('development_status', 'Unknown')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Character traits and quotes
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.markdown("#### 🌟 Key Traits")
                traits = selected_char_data.get('key_traits', [])
                if traits:
                    # Display traits as badges
                    traits_html = ""
                    for trait in traits:
                        traits_html += f'<span class="trait-badge">{trait}</span>'
                    st.markdown(traits_html, unsafe_allow_html=True)
                else:
                    st.info("No traits identified yet.")
            
            with col_b:
                st.markdown("#### 💬 Notable Quotes")
                quotes = selected_char_data.get('quotes', [])
                if quotes:
                    for quote in quotes:
                        st.markdown(f"""
                        <div class="quote-box">
                            "{quote}"
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No quotes recorded yet.")
    
    # Relationships section
    st.markdown("### 💞 Character Relationships")
    
    if relationships:
        # Create a grid layout for relationships
        rel_cols = st.columns(3)
        for idx, rel in enumerate(relationships):
            with rel_cols[idx % 3]:
                characters_involved = rel.get('characters', [])
                if len(characters_involved) >= 2:
                    relationship_type = rel.get('relationship_type', 'Unknown')
                    dynamics = rel.get('dynamics', 'No description')
                    significance = rel.get('significance', 'No significance noted')
                    sentiment = rel.get('sentiment', 'Unknown')
                    interaction_count = rel.get('interaction_count', 0)
                    
                    # Get color based on relationship type
                    rel_color = relationship_colors.get(relationship_type.lower(), relationship_colors['unknown'])
                    
                    st.markdown(f"""
                    <div class="relationship-card" style="border-left: 4px solid {rel_color};">
                        <h4>{' ↔ '.join(characters_involved)}</h4>
                        <p><strong>Type:</strong> <span class="relationship-type" style="background-color: {rel_color};">{relationship_type}</span></p>
                        <p><strong>Dynamics:</strong> {dynamics}</p>
                        <p><strong>Significance:</strong> {significance}</p>
                        <p><strong>Sentiment:</strong> {sentiment}</p>
                        <p><strong>Interactions:</strong> {interaction_count}</p>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.info("No relationships identified for this chapter.")
    
    # Network visualization
    st.markdown("### 🕸️ Character Network Visualization")
    
    # Create network data from relationships
    G = nx.Graph()
    
    # First collect all unique character names from both characters list and relationships
    all_characters = set()
    # Add characters from the main character list
    for char in characters:
        char_name = char.get('name', 'Unknown')
        all_characters.add(char_name.split('(')[0].strip())
    
    # Add characters from relationships
    for rel in relationships:
        chars = rel.get('characters', [])
        for char in chars:
            all_characters.add(char.strip())
    
    # Create a mapping of normalized names to actual names
    name_mapping = {}
    # First add from main character list
    for char in characters:
        char_name = char.get('name', 'Unknown')
        normalized_name = char_name.split('(')[0].strip()
        name_mapping[normalized_name] = char_name
        
        char_role = char.get('role', 'unknown').lower()
        G.add_node(char_name, 
                  role=char_role,
                  traits=char.get('key_traits', []),
                  description=char.get('description', ''))
    
    # Add any missing characters from relationships
    for char_name in all_characters:
        if char_name not in name_mapping:
            name_mapping[char_name] = char_name
            # Add node with default attributes
            G.add_node(char_name,
                      role='unknown',
                      traits=[],
                      description='Character from relationship data')
    
    # Debug print
    st.write("Characters added to graph:", list(G.nodes()))
    st.write("Name mapping:", name_mapping)
    
    # Add edges (relationships) with debug prints
    st.write("Processing relationships:", relationships)
    for rel in relationships:
        chars = rel.get('characters', [])
        st.write("Processing relationship:", chars)
        if len(chars) >= 2:
            # Get the full character names from the mapping
            char1 = name_mapping.get(chars[0].strip())
            char2 = name_mapping.get(chars[1].strip())
            
            st.write(f"Mapped names: {char1} → {char2}")
            
            # Make sure both characters exist in the graph
            if char1 and char2 and char1 in G.nodes() and char2 in G.nodes():
                relationship_type = rel.get('relationship_type', 'unknown')
                G.add_edge(char1, 
                          char2, 
                          type=relationship_type,
                          weight=rel.get('interaction_count', 1),
                          dynamics=rel.get('dynamics', ''),
                          sentiment=rel.get('sentiment', ''))
                st.write(f"Added edge between {char1} and {char2} with type {relationship_type}")
            else:
                st.warning(f"Could not add edge between {chars[0]} and {chars[1]} - mapped to {char1} and {char2}")
    
    st.write("Edges in graph:", list(G.edges(data=True)))
    
    if len(G.nodes()) > 0:
        # Create Plotly figure with larger size and better spacing
        pos = nx.spring_layout(G, k=2, iterations=100)  # Increased spacing and iterations
        
        # Initialize the figure with larger size
        fig = go.Figure()
        
        # Create edges (relationships) - Draw them first so they're behind nodes
        for edge in G.edges(data=True):
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            
            rel_type = edge[2].get('type', 'unknown')
            edge_color = relationship_colors.get(rel_type.lower(), relationship_colors['unknown'])
            edge_width = max(2, edge[2].get('weight', 1) * 2)  # Make edges thicker
            
            # Create curved edges for better visibility
            # Calculate the midpoint with an offset for curve
            mid_x = (x0 + x1) / 2
            mid_y = (y0 + y1) / 2
            # Add some curvature
            curve_x = mid_x + (y1 - y0) * 0.2
            curve_y = mid_y - (x1 - x0) * 0.2
            
            # Create edge path with curve
            path_x = [x0, curve_x, x1]
            path_y = [y0, curve_y, y1]
            
            hover_text = f"<b>{edge[0]} ↔ {edge[1]}</b><br>" + \
                        f"Relationship: {edge[2].get('type', 'Unknown')}<br>" + \
                        f"Dynamics: {edge[2].get('dynamics', 'Unknown')}<br>" + \
                        f"Sentiment: {edge[2].get('sentiment', 'Unknown')}"
            
            # Add edge trace
            fig.add_trace(go.Scatter(
                x=path_x,
                y=path_y,
                mode='lines',
                line=dict(
                    width=edge_width,
                    color=edge_color,
                    dash='solid' if rel_type.lower() in ['protective colleagues', 'ally', 'friend', 'family'] else 'dot'
                ),
                hoverinfo='text',
                text=hover_text,
                name=rel_type,
                showlegend=True
            ))
            
            # Add relationship label at midpoint
            fig.add_trace(go.Scatter(
                x=[curve_x],
                y=[curve_y],
                mode='text',
                text=[rel_type],
                textposition='middle center',
                textfont=dict(size=10, color=edge_color),
                hoverinfo='skip',
                showlegend=False
            ))
        
        # Create nodes (characters)
        for node in G.nodes(data=True):
            x, y = pos[node[0]]
            
            role = node[1].get('role', 'unknown')
            node_color = role_colors.get(role, role_colors['unknown'])
            
            # Size based on number of connections
            size = len(list(G.neighbors(node[0])))
            node_size = max(30, size * 20)  # Make nodes bigger
            
            # Create hover text with traits
            traits = node[1].get('traits', [])
            traits_text = "<br>• " + "<br>• ".join(traits) if traits else "No traits identified"
            hover_text = f"<b>{node[0]}</b><br>" + \
                        f"Role: {role.title()}<br>" + \
                        f"Connections: {size}<br>" + \
                        f"Traits:<br>{traits_text}"
            
            # Add node
            fig.add_trace(go.Scatter(
                x=[x],
                y=[y],
                mode='markers+text',
                marker=dict(
                    size=node_size,
                    color=node_color,
                    line=dict(width=2, color='white'),
                    opacity=0.9,
                    symbol='circle'
                ),
                text=[node[0]],
                textposition="middle center",
                textfont=dict(
                    size=12,
                    color='white',
                    family='Arial Black'
                ),
                hoverinfo='text',
                hovertext=hover_text,
                name=role.title(),
                showlegend=True
            ))
        
        # Update layout for better visualization
        fig.update_layout(
            title=dict(
                text="Character Relationship Network",
                x=0.5,
                y=0.95,
                font=dict(size=24)
            ),
            showlegend=True,
            legend=dict(
                title="Relationships & Roles",
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=1.05,
                bordercolor="white",
                borderwidth=1
            ),
            hovermode='closest',
            margin=dict(b=20, l=20, r=150, t=40),  # Adjusted margins for legend
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            plot_bgcolor='rgba(0,0,0,0)',
            width=1000,  # Larger width to accommodate legend
            height=800   # Larger height for better visibility
        )
        
        # Add hover effects
        fig.update_traces(
            hoverlabel=dict(
                bgcolor="white",
                font_size=12,
                font_family="Arial"
            )
        )
        
        # Display the network
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No character network data available for visualization.")

def story_companion_tab():
    """Create the interactive story companion interface."""
    st.markdown("## 💬 Interactive Story Companion")
    
    if not st.session_state.current_novel_id:
        st.warning("Please select a novel from the sidebar to start the AI companion.")
        return
    
    analysis = load_chapter_analysis(st.session_state.current_chapter_id, st.session_state.current_novel_id)
    if not analysis:
        st.error("Could not load chapter analysis for AI companion.")
        return
    
    interactive_data = analysis.get('interactive_companion', {})
    chapter_context = interactive_data.get('chapter_context', {})
    key_questions = interactive_data.get('key_questions', [])
    discussion_points = interactive_data.get('suggested_discussion_points', [])
    vocab_notes = interactive_data.get('vocabulary_notes', [])
    cultural_context = interactive_data.get('cultural_context', [])
    
    # Chat interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🤖 AI Reading Assistant")
        
        # Chapter context
        st.markdown("#### 📍 Chapter Context")
        st.markdown(f"""
        <div class="summary-box">
            <p><strong>Setting:</strong> {chapter_context.get('setting', 'Unknown')}</p>
            <p><strong>Timeline Position:</strong> {chapter_context.get('timeline_position', 'Unknown')}</p>
            <p><strong>Narrative Importance:</strong> {chapter_context.get('narrative_importance', 'Unknown')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display chat history
        chat_container = st.container()
        
        with chat_container:
            for message in st.session_state.chat_history:
                if message['role'] == 'user':
                    st.markdown(f"""
                    <div class="chat-message user-message">
                        <strong>You:</strong> {message['content']}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="chat-message ai-message">
                        <strong>Novel Companion AI:</strong> {message['content']}
                    </div>
                    """, unsafe_allow_html=True)
        
        # Chat input
        user_input = st.chat_input("Ask me anything about this chapter...")
        
        if user_input:
            # Add user message
            st.session_state.chat_history.append({
                'role': 'user',
                'content': user_input,
                'timestamp': datetime.now()
            })
            
            # Manage chat history length
            manage_chat_history()

            # Generate AI response using the API
            with st.spinner("🤔 Thinking..."):
                try:
                    # Use the API to get a response
                    api_response = api_client.chat_about_novel(
                        novel_id=st.session_state.current_novel_id,
                        message=user_input
                    )
                    
                    if api_response:
                        ai_response = api_response.get("response", "I'm sorry, I couldn't generate a response.")
                        references = api_response.get("references", [])
                        suggested_questions = api_response.get("suggested_questions", [])
                        
                        # Add references to the response if available
                        if references:
                            ai_response += "\n\n**References:**\n" + "\n".join([f"• {ref}" for ref in references])
                        
                        # Store suggested questions for later use
                        if suggested_questions:
                            st.session_state.suggested_questions = suggested_questions
                    else:
                        # Fallback response based on chapter data if API fails
                        chapter_analysis = analysis.get('chapter_analysis', {})
                        themes = chapter_analysis.get('themes', [])
                        characters = analysis.get('character_mapping', {}).get('characters', [])
                        summary = chapter_analysis.get('summary', {})
                        
                        if "character" in user_input.lower():
                            char_names = [char.get('name', '') for char in characters]
                            ai_response = f"This chapter features {', '.join(char_names)}. Each character plays a crucial role in developing the narrative. Would you like me to analyze a specific character's motivations or development?"
                        elif "theme" in user_input.lower():
                            theme_list = [theme.get('theme', '') for theme in themes[:3]]
                            ai_response = f"The major themes in this chapter include: {', '.join(theme_list)}. These themes work together to create a rich narrative tapestry. Which theme would you like to explore deeper?"
                        elif "summary" in user_input.lower():
                            ai_response = summary.get('detailed', 'This chapter contains significant plot developments and character interactions that advance the overall narrative.')
                        else:
                            ai_response = f"That's an interesting question about this chapter. Based on the context of {chapter_context.get('setting', 'this setting')}, I can help you explore the narrative elements, character motivations, and thematic significance. What specific aspect would you like to dive deeper into?"
                
                except Exception as e:
                    st.error(f"Error getting AI response: {e}")
                    ai_response = "I'm sorry, I encountered an error while processing your question. Please try again or rephrase your question."
            
            # Add AI response
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': ai_response,
                'timestamp': datetime.now()
            })
            
            # Manage chat history length
            manage_chat_history()
            
            st.rerun()
    
    with col2:
        st.markdown("### 🎯 Chapter Insights")
        
        # Key questions from the analysis
        if key_questions:
            st.markdown("#### ❓ Key Questions")
            for i, question in enumerate(key_questions[:3], 1):
                if st.button(f"Q{i}: {question[:50]}...", key=f"question_{i}"):
                    st.session_state.chat_history.append({
                        'role': 'user',
                        'content': question,
                        'timestamp': datetime.now()
                    })
                    st.rerun()
        
        # Discussion points
        if discussion_points:
            st.markdown("#### 💭 Discussion Points")
            for i, point in enumerate(discussion_points[:3], 1):
                if st.button(f"Discuss: {point[:40]}...", key=f"discussion_{i}"):
                    st.session_state.chat_history.append({
                        'role': 'user',
                        'content': f"Let's discuss {point}",
                        'timestamp': datetime.now()
                    })
                    st.rerun()
        
        # Vocabulary notes
        if vocab_notes:
            st.markdown("#### 📚 Vocabulary Notes")
            for note in vocab_notes:
                with st.expander(note.get('term', 'Unknown Term')):
                    st.markdown(note.get('definition', 'No definition available.'))
        
        # Cultural context
        if cultural_context:
            st.markdown("#### 🌍 Cultural Context")
            for context in cultural_context:
                with st.expander(context.get('reference', 'Cultural Reference')):
                    st.markdown(context.get('explanation', 'No explanation available.'))
        
        st.markdown("---")
        
        # Clear chat
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()

def analytics_dashboard():
    """Enhanced analytics dashboard with comprehensive data visualization."""
    st.markdown("# 📊 Analytics Dashboard")
    
    if not st.session_state.current_novel_id:
        st.warning("⚠️ Please select a novel from the sidebar to view analytics")
        return
    
    # Get novel and chapters data
    try:
        novel = api_client.get_novel_by_id(st.session_state.current_novel_id)
        chapters = get_novel_chapters(st.session_state.current_novel_id)
        
        if not novel:
            st.error("❌ Could not load novel data")
            return
            
        if not chapters:
            st.warning("📚 No chapters found for this novel")
            return
            
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        return
    
    # Helper function for safe data access
    def safe_get(data: Dict, *keys, default=None) -> Any:
        """Safely get value from dict using multiple possible keys"""
        if not isinstance(data, dict):
            return default
        for key in keys:
            if key in data and data[key] is not None:
                return data[key]
        return default
    
    # Novel overview
    st.markdown("## 📚 Novel Overview")
    
    novel_title = safe_get(novel, 'title', default='Unknown Novel')
    novel_author = safe_get(novel, 'author', default='Unknown Author')
    average_rating = safe_get(novel, 'average_rating', 'averageRating')
    vote_count = safe_get(novel, 'vote_count', 'voteCount')
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**📖 Title:** {novel_title}")
        st.markdown(f"**✍️ Author:** {novel_author}")
    with col2:
        if average_rating is not None:
            st.metric("⭐ Average Rating", f"{float(average_rating):.1f}/10")
        if vote_count is not None:
            st.metric("🗳️ Vote Count", f"{int(vote_count):,}")
    
    # Process chapter data with error handling
    chapter_data = []
    total_words = 0
    processed_chapters = 0
    
    for chapter in chapters:
        try:
            chapter_number = safe_get(chapter, 'chapter_number', default=0)
            chapter_title = safe_get(chapter, 'title', default='Untitled')
            word_count = safe_get(chapter, 'word_count', default=0)
            is_processed = safe_get(chapter, 'is_processed', default=False)
            reading_time = safe_get(chapter, 'reading_time_minutes')
            
            # Calculate reading time if not provided
            if reading_time is None and word_count > 0:
                reading_time = word_count / 200  # 200 words per minute
            elif reading_time is None:
                reading_time = 0
            
            chapter_data.append({
                'Chapter': int(chapter_number) if chapter_number else 0,
                'Title': str(chapter_title)[:30] + ('...' if len(str(chapter_title)) > 30 else ''),
                'Word Count': int(word_count) if word_count else 0,
                'Reading Time (min)': float(reading_time),
                'Processed': bool(is_processed)
            })
            
            # Accumulate stats
            total_words += int(word_count) if word_count else 0
            if is_processed:
                processed_chapters += 1
                
        except Exception as e:
            st.warning(f"⚠️ Error processing chapter data: {str(e)}")
            continue
    
    if not chapter_data:
        st.warning("📊 No valid chapter data available for analytics")
        return
    
    # Create DataFrame with error handling
    try:
        chapters_df = pd.DataFrame(chapter_data)
        total_chapters = len(chapters_df)
        avg_chapter_length = chapters_df['Word Count'].mean() if not chapters_df.empty else 0
        
    except Exception as e:
        st.error(f"❌ Error creating analytics data: {str(e)}")
        return
    
    # Key metrics
    st.markdown("## 📈 Key Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📚 Total Chapters", total_chapters)
    with col2:
        st.metric("✅ Processed", f"{processed_chapters}/{total_chapters}")
    with col3:
        st.metric("📝 Total Words", f"{total_words:,}")
    with col4:
        st.metric("📊 Avg Chapter Length", f"{avg_chapter_length:.0f} words")
    
    # Visualizations
    st.markdown("## 📊 Data Visualizations")
    
    if not chapters_df.empty:
        try:
            col1, col2 = st.columns(2)
            
            with col1:
                # Word count bar chart
                fig_words = px.bar(
                    chapters_df, 
                    x='Chapter', 
                    y='Word Count',
                    title="📝 Word Count by Chapter",
                    hover_data=['Title'],
                    color='Processed',
                    color_discrete_map={True: '#2E8B57', False: '#DC143C'},
                    labels={'Word Count': 'Words', 'Chapter': 'Chapter Number'}
                )
                fig_words.update_layout(
                    height=400,
                    xaxis_title="Chapter Number",
                    yaxis_title="Word Count"
                )
                st.plotly_chart(fig_words, use_container_width=True)
            
            with col2:
                # Reading time line chart
                fig_time = px.line(
                    chapters_df, 
                    x='Chapter', 
                    y='Reading Time (min)',
                    title="⏱️ Reading Time by Chapter",
                    markers=True,
                    hover_data=['Title'],
                    labels={'Reading Time (min)': 'Minutes', 'Chapter': 'Chapter Number'}
                )
                fig_time.update_layout(
                    height=400,
                    xaxis_title="Chapter Number",
                    yaxis_title="Reading Time (minutes)"
                )
                st.plotly_chart(fig_time, use_container_width=True)
            
            # Processing status pie chart
            if processed_chapters > 0 or (total_chapters - processed_chapters) > 0:
                status_data = {
                    'Status': ['Processed', 'Pending'],
                    'Count': [processed_chapters, total_chapters - processed_chapters]
                }
                
                fig_pie = px.pie(
                    values=status_data['Count'],
                    names=status_data['Status'],
                    title="📋 Chapter Processing Status",
                    color_discrete_map={'Processed': '#2E8B57', 'Pending': '#DC143C'}
                )
                fig_pie.update_layout(height=400)
                st.plotly_chart(fig_pie, use_container_width=True)
                
        except Exception as e:
            st.error(f"❌ Error creating visualizations: {str(e)}")
    
    # Reading statistics
    st.markdown("## 📚 Reading Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    try:
        with col1:
            estimated_reading_time = total_words / 200 if total_words > 0 else 0  # 200 words per minute
            if estimated_reading_time > 60:
                st.metric("📖 Est. Total Reading Time", f"{estimated_reading_time / 60:.1f} hours")
            else:
                st.metric("📖 Est. Total Reading Time", f"{estimated_reading_time:.0f} minutes")
        
        with col2:
            if average_rating is not None:
                st.metric("⭐ Average Rating", f"{float(average_rating):.1f}/10")
            else:
                st.metric("⭐ Average Rating", "N/A")
        
        with col3:
            if vote_count is not None:
                st.metric("🗳️ Vote Count", f"{int(vote_count):,}")
            else:
                st.metric("🗳️ Vote Count", "N/A")
                
    except Exception as e:
        st.warning(f"⚠️ Error displaying reading statistics: {str(e)}")
    
    # Detailed chapter table
    st.markdown("## 📋 Chapter Details")
    
    if not chapters_df.empty:
        try:
            # Display the dataframe with proper formatting
            st.dataframe(
                chapters_df,
                column_config={
                    "Chapter": st.column_config.NumberColumn("Ch #", width="small", format="%d"),
                    "Title": st.column_config.TextColumn("Title", width="large"),
                    "Word Count": st.column_config.NumberColumn("Words", width="medium", format="%d"),
                    "Reading Time (min)": st.column_config.NumberColumn("Time (min)", width="medium", format="%.1f"),
                    "Processed": st.column_config.CheckboxColumn("✅ Processed", width="small")
                },
                hide_index=True,
                use_container_width=True
            )
        except Exception as e:
            st.error(f"❌ Error displaying chapter table: {str(e)}")
            # Fallback to simple table
            st.table(chapters_df)
    
    # Export functionality
    st.markdown("## 📤 Export Data")
    
    col1, col2, col3 = st.columns(3)
    
    try:
        with col1:
            if st.button("📊 Export Analytics CSV"):
                csv_data = chapters_df.to_csv(index=False)
                st.download_button(
                    label="💾 Download CSV",
                    data=csv_data,
                    file_name=f"{novel_title.replace(' ', '_')}_analytics.csv",
                    mime="text/csv"
                )
        
        with col2:
            if st.button("📈 Export Reading Report"):
                report = f"""# Reading Analytics Report
## {novel_title}

**Author:** {novel_author}
**Total Chapters:** {total_chapters}
**Processed Chapters:** {processed_chapters}
**Total Word Count:** {total_words:,}
**Average Chapter Length:** {avg_chapter_length:.0f} words
**Estimated Reading Time:** {estimated_reading_time:.1f} minutes

### Chapter Breakdown:
{chapters_df.to_string(index=False)}

---
Generated by Novel Companion AI on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
                st.download_button(
                    label="📄 Download Report",
                    data=report,
                    file_name=f"{novel_title.replace(' ', '_')}_report.txt",
                    mime="text/plain"
                )
        
        with col3:
            if st.button("🔄 Refresh Analytics"):
                st.cache_data.clear()
                st.rerun()
                
    except Exception as e:
        st.warning(f"⚠️ Error with export functionality: {str(e)}")

def manage_chat_history():
    """Manage chat history length and cleanup"""
    if len(st.session_state.chat_history) > MAX_CHAT_MESSAGES:
        # Keep only the most recent messages
        st.session_state.chat_history = st.session_state.chat_history[-MAX_CHAT_MESSAGES:]
    
    # Remove very old messages (older than 24 hours in a real scenario)
    # For now, just limit by count
    current_time = datetime.now()
    filtered_history = []
    
    for message in st.session_state.chat_history:
        # Keep message if it doesn't have a timestamp or is recent
        if 'timestamp' not in message:
            filtered_history.append(message)
        else:
            message_time = message['timestamp']
            if isinstance(message_time, str):
                try:
                    message_time = datetime.fromisoformat(message_time)
                except:
                    filtered_history.append(message)
                    continue
            
            # Keep messages from the last session (for demo purposes)
            filtered_history.append(message)
    
    st.session_state.chat_history = filtered_history

def main():
    """Main application function."""
    # Load custom CSS
    apply_css()
    
    # Initialize session state
    initialize_session_state()
    
    # Create sidebar
    create_sidebar()
    
    # Main content area
    create_header()
    
    # Navigation tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📖 Chapter Analysis", 
        "👥 Character Mapping", 
        "💬 AI Companion", 
        "📊 Analytics"
    ])
    
    with tab1:
        chapter_summarization_tab()
    
    with tab2:
        character_mapping_tab()
    
    with tab3:
        story_companion_tab()
    
    with tab4:
        analytics_dashboard()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem; color: #666;">
        <h4>🚀 Novel Companion AI</h4>
        <p>Powered by Advanced NLP & Large Language Models | 
        <a href="https://github.com/chogerlate/NovelVizAI-Frontend" target="_blank">View on GitHub</a></p>
        <p><em>Enhancing reading comprehension through intelligent AI assistance</em></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 

