import streamlit as st

# Custom CSS for beautiful styling
def apply_css():
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
    
    .theme-badge {
        background: linear-gradient(145deg, #667eea, #764ba2);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        margin: 0.2rem;
        display: inline-block;
    }
    
    .emotion-tag {
        background: linear-gradient(145deg, #ff6b6b, #ee5a24);
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 10px;
        font-size: 0.7rem;
        margin: 0.1rem;
        display: inline-block;
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
    
    .quote-box {
        background: linear-gradient(145deg, #fff5f5, #ffffff);
        border-left: 4px solid #667eea;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 5px;
        font-style: italic;
    }
    </style>
    """, unsafe_allow_html=True)
