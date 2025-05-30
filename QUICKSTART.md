# 🚀 Quick Start Guide - Novel Companion AI

Get up and running with Novel Companion AI in under 5 minutes!

## ⚡ Instant Launch

### Option 1: Using the Launcher (Recommended)
```bash
uv run launch.py
```

### Option 2: Direct Streamlit Launch
```bash
uv run streamlit run app/client.py
```

### Option 3: Using the Main Entry Point
```bash
uv run main.py
```

## 🔧 Installation

### Prerequisites
- Python 3.10 or higher
- Internet connection for package installation

### Quick Install
```bash
# Clone the repository
git clone https://github.com/chogerlate/NovelVizAI-Frontend.git
cd NovelVizAI-Frontend

# Install dependencies
uv sync  # OR pip install -r requirements.txt

# Launch the application
uv run launch.py
```

## 🎯 First Steps

1. **📖 Open your browser** to `http://localhost:8501`
2. **🔍 Select a novel** from the dropdown (try "Pride and Prejudice")
3. **⚙️ Configure analysis** in the sidebar (Standard depth is good to start)
4. **🚀 Explore features** using the tabs at the top

## 🌟 Feature Tour

### 📖 Chapter Summaries
- Select any chapter from the dropdown
- Click "🔄 Generate Summary" 
- Explore key events, themes, and sentiment analysis

### 👥 Character Mapping  
- Browse character list on the left
- Click characters to see detailed profiles
- Explore relationship networks and development timelines

### 💬 Story Companion
- Chat with AI about the novel
- Ask questions like "What are the main themes?"
- Use suggested questions for quick insights

### 📊 Analytics Dashboard
- View reading progress and comprehension metrics
- Explore theme distributions and character interactions
- Track your reading journey over time

## 🎨 Customization

### Upload Your Own Novel
1. Select "Upload Custom Text" from the novel dropdown
2. Upload a .txt file of your novel
3. Wait for automatic analysis to complete
4. Explore all features with your custom content

### Adjust Analysis Depth
- **Basic**: Quick overview and basic insights
- **Standard**: Balanced analysis (recommended)
- **Deep**: Detailed character and theme analysis
- **Comprehensive**: Full analytical suite

## 🔧 Troubleshooting

### Application Won't Start
```bash
# Check if all dependencies are installed
pip install streamlit pandas plotly networkx nltk scikit-learn

# Or using uv
uv sync
```

### Port Already in Use
```bash
# Use a different port
uv run streamlit run app/client.py --server.port 8502
```

### Import Errors
```bash
# Ensure you're in the correct directory
cd /path/to/NovelVizAI-Frontend

# Reinstall dependencies
uv add -r requirements.txt
```

## 💡 Tips for Best Experience

### 🎯 Getting Better Results
- **Upload clean text files**: Remove headers, footers, and page numbers
- **Use proper chapter breaks**: Clear chapter divisions improve analysis
- **Try different analysis depths**: Experiment to find your preferred level of detail

### 🚀 Performance Tips
- **Smaller files first**: Start with shorter texts to test features
- **Use Standard analysis**: Deep analysis takes longer for large texts
- **Be patient**: Initial analysis may take a few moments

### 🎨 UI Tips
- **Use the sidebar**: All main controls are in the left panel
- **Explore all tabs**: Each tab offers unique insights
- **Try the chat**: The AI companion is great for discussions

## 📚 Sample Questions to Ask the AI

- "What are the main themes in this novel?"
- "How does Elizabeth's character develop?"
- "Explain the relationship between Darcy and Elizabeth"
- "What is the significance of pride in the story?"
- "Summarize the central conflict"

## 🆘 Need Help?

- **📖 Full Documentation**: See `README.md`
- **🐛 Issues**: [GitHub Issues](https://github.com/chogerlate/NovelVizAI-Frontend/issues)
- **💬 Questions**: Use the Story Companion chat feature
- **🔍 Examples**: Try the pre-loaded "Pride and Prejudice" sample

## 🎉 What's Next?

Once you're comfortable with the basics:

1. **📊 Dive into Analytics**: Explore the dashboard for reading insights
2. **🎭 Character Analysis**: Use the network view to visualize relationships
3. **📝 Export Results**: Save your analysis (coming soon!)
4. **🤝 Share Insights**: Discuss findings with reading groups
5. **🔧 Customize**: Explore the code to add your own features

---

**Happy Reading with Novel Companion AI!** 📚✨

*Got everything working? Dive into the full documentation in `README.md` for advanced features and customization options.* 