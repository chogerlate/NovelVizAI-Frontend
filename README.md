# 📚 Novel Companion AI

An intelligent reading assistant powered by advanced NLP techniques and Large Language Models that enhances reading comprehension through three core features: intelligent chapter summarization, dynamic character mapping, and an interactive story companion.

![Novel Companion AI](https://img.shields.io/badge/Novel%20Companion-AI%20Powered-blue)
![Python](https://img.shields.io/badge/Python-3.10+-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.45+-red)

## 🌟 Features

### 🔍 Intelligent Chapter Summarization
- **Advanced Text Processing**: Uses sophisticated NLP techniques to analyze chapter content
- **Key Event Extraction**: Automatically identifies and highlights crucial plot points
- **Theme Analysis**: Discovers major themes and their development throughout chapters
- **Sentiment Visualization**: Provides emotional tone analysis with interactive charts
- **Character Development Tracking**: Monitors how characters evolve chapter by chapter

### 👥 Dynamic Character Mapping
- **Named Entity Recognition**: Automatically identifies and tracks characters
- **Relationship Network**: Visualizes character connections and interactions
- **Character Profiles**: Detailed information including traits, roles, and story arcs
- **Development Timeline**: Shows character growth across the narrative
- **Interaction Analysis**: Measures relationship strength and sentiment

### 💬 Interactive Story Companion
- **Conversational AI**: Chat with an AI assistant about the novel
- **Context-Aware Responses**: Understands plot, characters, and themes
- **Question Answering**: Get instant answers about any aspect of the story
- **Discussion Facilitation**: Engages in deep literary analysis
- **Reading Support**: Provides clarification and additional insights

### 📊 Reading Analytics Dashboard
- **Progress Tracking**: Monitor reading speed and comprehension
- **Insight Generation**: Automated analysis reports
- **Performance Metrics**: Track your reading improvement over time
- **Theme Distribution**: Visual breakdown of narrative themes

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- pip or uv package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/chogerlate/NovelVizAI-Frontend.git
   cd NovelVizAI-Frontend
   ```

2. **Install dependencies**
   
   Using uv (recommended):
   ```bash
   uv sync
   ```
   
   Using pip:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```
   
   Or directly with Streamlit:
   ```bash
   streamlit run app/client.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:8501` to access the application.

## 📖 Usage Guide

### Getting Started with Novel Analysis

1. **Select a Novel**: Choose from pre-loaded classics or upload your own text
2. **Configure Analysis**: Set analysis depth and enable desired features
3. **Explore Features**: Navigate through the tabbed interface to access different tools

### Chapter Summarization

1. Navigate to the "📖 Chapter Summaries" tab
2. Select a chapter from the dropdown menu
3. Click "🔄 Generate Summary" to analyze the content
4. Review the intelligent summary, key events, and thematic analysis
5. Explore sentiment visualization charts

### Character Mapping

1. Go to the "👥 Character Mapping" tab
2. Select a character from the list to view detailed information
3. Explore character traits, relationships, and development
4. Use the network tabs to visualize character interactions and timelines

### Story Companion Chat

1. Visit the "💬 Story Companion" tab
2. Type questions about the novel in the chat input
3. Use suggested questions for quick analysis
4. Engage in discussions about themes, characters, and plot points

### Analytics Dashboard

1. Check the "📊 Analytics" tab for reading insights
2. Monitor your reading progress and comprehension scores
3. View theme distribution and reading time analytics

## 🛠️ Technical Architecture

### Core Technologies

- **Frontend**: Streamlit for interactive web application
- **NLP Processing**: Custom text analysis pipeline with extensible architecture
- **Data Visualization**: Pandas and Plotly for interactive charts
- **Text Processing**: Regular expressions and statistical analysis
- **State Management**: Streamlit session state for user data persistence

### Application Structure

```
app/
├── client.py                 # Main Streamlit application
├── components/
│   ├── __init__.py
│   └── nlp_utils.py         # NLP utilities and analysis functions
├── __init__.py
main.py                      # Application entry point
pyproject.toml              # Project dependencies and metadata
README.md                   # Documentation
```

### Key Components

- **NovelAnalyzer Class**: Manages novel analysis with state tracking
- **NLP Utilities**: Text processing, sentiment analysis, and theme extraction
- **Interactive UI Components**: Modular Streamlit components for each feature
- **Visualization Pipeline**: Charts and graphs for data presentation

## 🔧 Configuration

### Analysis Options

The application provides several configurable analysis options:

- **Analysis Depth**: Basic, Standard, Deep, or Comprehensive
- **Theme Analysis**: Enable/disable thematic analysis
- **Sentiment Analysis**: Toggle emotional tone analysis
- **Character Relationships**: Control relationship mapping

### Supported File Formats

- **TXT**: Plain text files
- **PDF**: Portable Document Format (planned)
- **DOCX**: Microsoft Word documents (planned)

## 🎨 Customization

### Adding Custom Novels

1. Select "Upload Custom Text" from the novel selector
2. Upload your text file (TXT format recommended)
3. The application will automatically analyze the content

### Extending NLP Features

The application is designed for extensibility. To add new NLP features:

1. Extend the `nlp_utils.py` module with new analysis functions
2. Update the `NovelAnalyzer` class to incorporate new features
3. Add corresponding UI components in `client.py`

## 📊 Performance Considerations

- **Text Processing**: Optimized for novels up to 500,000 words
- **Real-time Analysis**: Chapter summaries generated in 2-3 seconds
- **Memory Usage**: Efficient state management for large texts
- **Responsive UI**: Streamlit's reactive architecture ensures smooth interactions

## 🚧 Future Enhancements

### Planned Features

- **Advanced LLM Integration**: OpenAI GPT, Anthropic Claude, or local models
- **Multi-language Support**: Analysis for novels in various languages
- **Export Functionality**: Save analysis reports as PDF or Word documents
- **Collaborative Features**: Share insights with reading groups
- **Mobile Optimization**: Responsive design for mobile devices

### Technical Improvements

- **Enhanced NER**: Deep learning models for better character recognition
- **Transformer Summarization**: State-of-the-art summarization models
- **Network Analysis**: Advanced graph algorithms for character relationships
- **Performance Optimization**: Caching and parallel processing

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

1. Clone the repo and install dependencies
2. Create a virtual environment
3. Install development dependencies
4. Run tests before submitting PRs

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Streamlit Team**: For the amazing web app framework
- **Open Source Community**: For the libraries and tools that make this possible
- **Literary Analysis Research**: For inspiration and methodological guidance

## 📞 Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/chogerlate/NovelVizAI-Frontend/issues)
- **Documentation**: This README and inline code documentation
- **Community**: Join discussions in our GitHub Discussions

---

**Novel Companion AI** - *Enhancing reading comprehension through intelligent AI assistance* 📚✨
