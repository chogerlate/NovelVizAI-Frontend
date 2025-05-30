#!/usr/bin/env python3
"""
Novel Companion AI - Streamlit Application
A comprehensive AI-driven reading assistant with intelligent chapter summarization,
dynamic character mapping, and interactive story companion features.
"""

import streamlit as st
import json
import time
from datetime import datetime
from typing import Dict, List, Optional
import pandas as pd

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

# Custom CSS for beautiful styling
def load_css():
    st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    
    .stApp {
        background: white;
    }
    
    .content-container {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        margin: 1rem 0;
    }
    
    .feature-card {
        background: linear-gradient(145deg, #f0f2f6, #ffffff);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    
    .character-card {
        background: linear-gradient(145deg, #e8f4fd, #ffffff);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 3px solid #4a90e2;
    }
    
    .summary-box {
        background: linear-gradient(145deg, #f8f9fa, #ffffff);
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e9ecef;
        margin: 1rem 0;
    }
    
    .chat-message {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
    }
    
    .user-message {
        background: linear-gradient(145deg, #667eea, #764ba2);
        color: white;
        margin-left: 2rem;
    }
    
    .ai-message {
        background: linear-gradient(145deg, #f8f9fa, #e9ecef);
        color: #333;
        margin-right: 2rem;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    .title-gradient {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Sample data for demonstration
SAMPLE_CHARACTERS = {
    "Elizabeth Bennet": {
        "description": "Spirited and intelligent protagonist of Pride and Prejudice",
        "role": "Main Character",
        "first_appearance": "Chapter 1",
        "relationships": ["Mr. Darcy (love interest)", "Jane Bennet (sister)", "Mr. Bennet (father)"],
        "key_traits": ["Witty", "Independent", "Prejudiced initially", "Strong-willed"]
    },
    "Mr. Darcy": {
        "description": "Wealthy and seemingly arrogant gentleman",
        "role": "Male Lead",
        "first_appearance": "Chapter 3",
        "relationships": ["Elizabeth Bennet (love interest)", "Mr. Bingley (friend)", "Georgiana Darcy (sister)"],
        "key_traits": ["Proud", "Honorable", "Misunderstood", "Generous"]
    },
    "Jane Bennet": {
        "description": "Elizabeth's gentle and kind elder sister",
        "role": "Supporting Character",
        "first_appearance": "Chapter 1",
        "relationships": ["Mr. Bingley (love interest)", "Elizabeth Bennet (sister)"],
        "key_traits": ["Gentle", "Optimistic", "Beautiful", "Reserved"]
    }
}

SAMPLE_CHAPTERS = {
    "Chapter 1": {
        "title": "The Arrival of Mr. Bingley",
        "summary": "The story opens with the famous line about wealthy single men. Mr. and Mrs. Bennet discuss the arrival of the wealthy Mr. Bingley to Netherfield Park. Mrs. Bennet is excited about the prospect of one of her daughters marrying him, while Mr. Bennet remains characteristically dry and witty.",
        "key_events": ["Mr. Bingley moves to Netherfield", "Mrs. Bennet's marriage schemes begin"],
        "characters_introduced": ["Mr. Bennet", "Mrs. Bennet", "Elizabeth Bennet (mentioned)"],
        "themes": ["Marriage and social status", "Family dynamics"]
    },
    "Chapter 2": {
        "title": "Mr. Bennet's Visit",
        "summary": "Mr. Bennet surprises his family by revealing he has already visited Mr. Bingley, despite his earlier apparent indifference. This sets up the social connection needed for his daughters to meet the eligible bachelor.",
        "key_events": ["Mr. Bennet's secret visit revealed", "Family preparation for social meeting"],
        "characters_introduced": ["Continuation of Bennet family introduction"],
        "themes": ["Paternal care disguised as indifference", "Social conventions"]
    }
}

def initialize_session_state():
    """Initialize session state variables."""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'current_novel' not in st.session_state:
        st.session_state.current_novel = "Pride and Prejudice"
    if 'uploaded_text' not in st.session_state:
        st.session_state.uploaded_text = ""
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False

def create_header():
    """Create the main header section."""
    st.markdown('<h1 class="title-gradient">📚 Novel Companion AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Your intelligent reading assistant powered by advanced NLP and Large Language Models</p>', unsafe_allow_html=True)
    
    # Feature overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🔍 Chapter Summarization</h3>
            <p>Get intelligent summaries of complex chapters with key events, themes, and character developments highlighted.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>👥 Character Mapping</h3>
            <p>Dynamic character relationship maps with personality traits, story arcs, and interconnections visualized.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>💬 Story Companion</h3>
            <p>Interactive AI assistant to discuss plot points, analyze themes, and answer questions about the narrative.</p>
        </div>
        """, unsafe_allow_html=True)

def create_sidebar():
    """Create the sidebar with navigation and controls."""
    with st.sidebar:
        st.markdown("## 🎛️ Control Panel")
        
        # Novel selection
        selected_novel = st.selectbox(
            "📖 Select Novel",
            ["Pride and Prejudice", "To Kill a Mockingbird", "1984", "Upload Custom Text"],
            index=0
        )
        
        if selected_novel == "Upload Custom Text":
            uploaded_file = st.file_uploader(
                "Upload your text file",
                type=['txt', 'pdf', 'docx'],
                help="Supported formats: TXT, PDF, DOCX"
            )
            
            if uploaded_file is not None:
                st.success(f"✅ Uploaded: {uploaded_file.name}")
        
        st.session_state.current_novel = selected_novel
        
        st.markdown("---")
        
        # Analysis options
        st.markdown("## 🔧 Analysis Options")
        
        analysis_depth = st.select_slider(
            "Analysis Depth",
            options=["Basic", "Standard", "Deep", "Comprehensive"],
            value="Standard"
        )
        
        include_themes = st.checkbox("Include Theme Analysis", value=True)
        include_sentiment = st.checkbox("Include Sentiment Analysis", value=True)
        include_relationships = st.checkbox("Character Relationship Analysis", value=True)
        
        st.markdown("---")
        
        # Quick stats
        st.markdown("## 📊 Quick Stats")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Characters", "12", "+3")
        with col2:
            st.metric("Chapters", "8", "+1")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Themes", "5", "+1")
        with col2:
            st.metric("Summaries", "8", "+1")

def chapter_summarization_tab():
    """Create the chapter summarization interface."""
    st.markdown("## 📖 Intelligent Chapter Summarization")
    
    # Chapter selection
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_chapter = st.selectbox(
            "Select Chapter to Analyze",
            list(SAMPLE_CHAPTERS.keys()),
            help="Choose a chapter to generate an intelligent summary"
        )
    
    with col2:
        if st.button("🔄 Generate Summary", type="primary"):
            with st.spinner("Analyzing chapter content..."):
                time.sleep(2)  # Simulate AI processing
                st.success("Summary generated successfully!")
    
    if selected_chapter in SAMPLE_CHAPTERS:
        chapter_data = SAMPLE_CHAPTERS[selected_chapter]
        
        # Display summary
        st.markdown(f"""
        <div class="summary-box">
            <h3>📝 {chapter_data['title']}</h3>
            <p><strong>Summary:</strong> {chapter_data['summary']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Key information in columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎯 Key Events")
            for event in chapter_data['key_events']:
                st.markdown(f"• {event}")
            
            st.markdown("### 🎭 Characters Introduced")
            for character in chapter_data['characters_introduced']:
                st.markdown(f"• {character}")
        
        with col2:
            st.markdown("### 🎨 Major Themes")
            for theme in chapter_data['themes']:
                st.markdown(f"• {theme}")
            
            # Sentiment analysis visualization
            st.markdown("### 📊 Chapter Sentiment")
            sentiment_data = pd.DataFrame({
                'Emotion': ['Joy', 'Tension', 'Romance', 'Humor', 'Melancholy'],
                'Intensity': [0.7, 0.3, 0.8, 0.9, 0.2]
            })
            st.bar_chart(sentiment_data.set_index('Emotion'))

def character_mapping_tab():
    """Create the character mapping interface."""
    st.markdown("## 👥 Dynamic Character Mapping")
    
    # Character selection and overview
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 📋 Character List")
        selected_character = st.radio(
            "Select Character",
            list(SAMPLE_CHARACTERS.keys()),
            help="Choose a character to view detailed information"
        )
        
        # Quick stats
        st.markdown("### 📈 Network Stats")
        st.metric("Total Characters", len(SAMPLE_CHARACTERS))
        st.metric("Relationships", "8")
        st.metric("Character Arcs", "3")
    
    with col2:
        if selected_character in SAMPLE_CHARACTERS:
            char_data = SAMPLE_CHARACTERS[selected_character]
            
            st.markdown(f"""
            <div class="character-card">
                <h3>🎭 {selected_character}</h3>
                <p><strong>Role:</strong> {char_data['role']}</p>
                <p><strong>Description:</strong> {char_data['description']}</p>
                <p><strong>First Appearance:</strong> {char_data['first_appearance']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Character traits
            st.markdown("#### 🌟 Key Traits")
            trait_cols = st.columns(2)
            for i, trait in enumerate(char_data['key_traits']):
                with trait_cols[i % 2]:
                    st.markdown(f"🔹 {trait}")
            
            # Relationships
            st.markdown("#### 💞 Relationships")
            for relationship in char_data['relationships']:
                st.markdown(f"• {relationship}")
    
    # Character relationship network visualization
    st.markdown("### 🕸️ Character Relationship Network")
    
    # Simulate a network graph with tabs
    tab1, tab2, tab3 = st.tabs(["📊 Network View", "📈 Timeline", "🎯 Interactions"])
    
    with tab1:
        st.info("🔄 Interactive character relationship network would be displayed here using libraries like NetworkX or Plotly")
        
        # Sample relationship matrix
        characters = list(SAMPLE_CHARACTERS.keys())
        relationship_matrix = pd.DataFrame(
            [[0, 0.9, 0.7], [0.9, 0, 0.4], [0.7, 0.4, 0]],
            index=characters,
            columns=characters
        )
        st.dataframe(relationship_matrix, use_container_width=True)
    
    with tab2:
        st.markdown("#### 📅 Character Development Timeline")
        timeline_data = pd.DataFrame({
            'Chapter': [1, 2, 3, 4, 5, 6, 7, 8],
            'Elizabeth Development': [0.1, 0.2, 0.4, 0.6, 0.7, 0.8, 0.9, 1.0],
            'Darcy Development': [0.0, 0.1, 0.2, 0.4, 0.6, 0.8, 0.9, 1.0],
            'Jane Development': [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        })
        st.line_chart(timeline_data.set_index('Chapter'))
    
    with tab3:
        st.markdown("#### 🗣️ Character Interactions")
        interaction_data = pd.DataFrame({
            'Characters': ['Elizabeth-Darcy', 'Elizabeth-Jane', 'Jane-Bingley', 'Darcy-Bingley'],
            'Frequency': [45, 32, 28, 15],
            'Sentiment': [0.6, 0.9, 0.8, 0.7]
        })
        st.dataframe(interaction_data, use_container_width=True)

def story_companion_tab():
    """Create the interactive story companion interface."""
    st.markdown("## 💬 Interactive Story Companion")
    
    # Chat interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🤖 AI Reading Assistant")
        
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
        user_input = st.chat_input("Ask me anything about the novel...")
        
        if user_input:
            # Add user message
            st.session_state.chat_history.append({
                'role': 'user',
                'content': user_input,
                'timestamp': datetime.now()
            })
            
            # Generate AI response (simulated)
            with st.spinner("🤔 Thinking..."):
                time.sleep(1)
                
                # Sample responses based on common questions
                if "character" in user_input.lower():
                    ai_response = "The characters in this novel are beautifully developed. Elizabeth Bennet, for instance, represents the independent spirit of women challenging social norms of the era. Her wit and intelligence make her a compelling protagonist who grows throughout the story."
                elif "theme" in user_input.lower():
                    ai_response = "The major themes include the dangers of first impressions, the importance of looking beyond surface appearances, social class and its influence on relationships, and the evolution of love from initial prejudice to deep understanding."
                elif "summary" in user_input.lower():
                    ai_response = "This novel explores the complex dance of courtship in 19th-century England, focusing on Elizabeth Bennet's journey from prejudice to love, while examining how pride and social expectations can both hinder and ultimately strengthen genuine relationships."
                else:
                    ai_response = f"That's an interesting question about '{user_input}'. Based on my analysis of the text, I can help you explore the narrative elements, character motivations, and thematic significance. What specific aspect would you like to dive deeper into?"
            
            # Add AI response
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': ai_response,
                'timestamp': datetime.now()
            })
            
            st.rerun()
    
    with col2:
        st.markdown("### 🎯 Quick Actions")
        
        # Predefined questions
        st.markdown("#### 💡 Suggested Questions")
        
        quick_questions = [
            "Analyze Elizabeth's character development",
            "What are the main themes?",
            "Explain the relationship dynamics",
            "Summarize the central conflict",
            "Discuss the historical context"
        ]
        
        for question in quick_questions:
            if st.button(question, key=f"quick_{question}"):
                # Simulate clicking the question
                st.session_state.chat_history.append({
                    'role': 'user',
                    'content': question,
                    'timestamp': datetime.now()
                })
                st.rerun()
        
        st.markdown("---")
        
        # Analysis tools
        st.markdown("#### 🔧 Analysis Tools")
        
        if st.button("📊 Generate Theme Report"):
            st.info("Comprehensive theme analysis report generated!")
        
        if st.button("🎭 Character Analysis"):
            st.info("Detailed character analysis complete!")
        
        if st.button("📝 Plot Summary"):
            st.info("Intelligent plot summary created!")
        
        # Clear chat
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()

def analytics_dashboard():
    """Create an analytics dashboard for reading insights."""
    st.markdown("## 📊 Reading Analytics Dashboard")
    
    # Metrics overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📚 Reading Progress",
            value="65%",
            delta="12% this week"
        )
    
    with col2:
        st.metric(
            label="⏱️ Reading Time",
            value="4.2 hrs",
            delta="30 min today"
        )
    
    with col3:
        st.metric(
            label="🎯 Comprehension Score",
            value="87%",
            delta="5% improvement"
        )
    
    with col4:
        st.metric(
            label="💡 Insights Generated",
            value="23",
            delta="8 new"
        )
    
    # Charts and visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Reading Progress Over Time")
        progress_data = pd.DataFrame({
            'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            'Pages Read': [15, 23, 18, 31, 27, 42, 35],
            'Comprehension': [85, 87, 83, 91, 89, 93, 90]
        })
        st.line_chart(progress_data.set_index('Day'))
    
    with col2:
        st.markdown("### 🎨 Theme Distribution")
        theme_data = pd.DataFrame({
            'Theme': ['Romance', 'Social Class', 'Pride', 'Prejudice', 'Family'],
            'Occurrence': [35, 28, 22, 20, 18]
        })
        st.bar_chart(theme_data.set_index('Theme'))

def main():
    """Main application function."""
    # Load custom CSS
    load_css()
    
    # Initialize session state
    initialize_session_state()
    
    # Create sidebar
    create_sidebar()
    
    # Main content area
    create_header()
    
    # Navigation tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📖 Chapter Summaries", 
        "👥 Character Mapping", 
        "💬 Story Companion", 
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