# Ukrainian Q&A - ML-Powered Ukrainian Knowledge Assistant

A machine learning-powered web application that answers questions about Ukrainian culture, history, geography, and language. Built with Flask, sentence transformers, and modern web technologies.

## 🇺🇦 Features

- **Intelligent Q&A**: Ask questions about Ukrainian topics and get accurate, contextual answers
- **Multiple Knowledge Domains**: History, culture, geography, politics, and language
- **Dual AI Approach**: Uses both local ML models and OpenAI API (when available)
- **Beautiful UI**: Modern, responsive interface with Ukrainian-themed design
- **Real-time Chat**: Interactive chat interface with suggestion chips
- **Semantic Search**: Advanced similarity search using FAISS and sentence transformers

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd WebAI
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** (optional)
   ```bash
   cp config.env.example .env
   # Edit .env and add your OpenAI API key if desired
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## 🏗️ Architecture

### Core Components

- **`app.py`**: Flask web server with REST API endpoints
- **`ukrainian_qa_model.py`**: ML model class with knowledge base and similarity search
- **`templates/index.html`**: Modern web interface with chat functionality

### ML Pipeline

1. **Knowledge Base**: Curated Ukrainian facts and information
2. **Embedding Model**: Sentence transformers for semantic understanding
3. **Similarity Search**: FAISS index for fast context retrieval
4. **Answer Generation**: OpenAI API or local template-based responses

### Knowledge Domains

- **History**: Independence, historical events, cultural heritage
- **Culture**: Traditional crafts, food, music, customs
- **Geography**: Borders, mountains, rivers, climate
- **Politics**: Government, current events, international relations
- **Language**: Common phrases, translations, linguistic features

## 🎯 Usage Examples

### Sample Questions

- "What is the capital of Ukraine?"
- "Tell me about Ukrainian borscht"
- "What does Слава Україні mean?"
- "Ukrainian independence history"
- "Geography of Ukraine"
- "Traditional Ukrainian music"

### API Endpoints

- `GET /`: Main web interface
- `POST /api/ask`: Submit a question
- `GET /api/health`: Health check and model status

## 🔧 Configuration

### Environment Variables

- `OPENAI_API_KEY`: OpenAI API key for enhanced responses (optional)
- `FLASK_DEBUG`: Enable debug mode (default: False)
- `PORT`: Server port (default: 5000)

### Model Configuration

The application uses:
- **Sentence Transformer**: `all-MiniLM-L6-v2` for embeddings
- **FAISS Index**: For fast similarity search
- **Knowledge Base**: Curated Ukrainian facts and information

## 🛠️ Development

### Project Structure

```
WebAI/
├── app.py                 # Main Flask application
├── ukrainian_qa_model.py  # ML model implementation
├── requirements.txt       # Python dependencies
├── config.env.example     # Environment configuration example
├── README.md             # This file
└── templates/
    └── index.html        # Web interface
```

### Adding New Knowledge

To expand the knowledge base, edit the `ukrainian_knowledge` dictionary in `ukrainian_qa_model.py`:

```python
self.ukrainian_knowledge = {
    "new_category": [
        "New fact about Ukraine",
        "Another interesting fact"
    ]
}
```

### Customizing the Model

- **Embedding Model**: Change the sentence transformer model in `_initialize_model()`
- **Similarity Search**: Modify FAISS index parameters in `_build_faiss_index()`
- **Response Generation**: Customize answer templates in `_get_local_answer()`

## 🌟 Features in Detail

### Smart Context Retrieval

The system uses semantic similarity to find the most relevant information for each question, ensuring accurate and contextual responses.

### Fallback System

- **Primary**: OpenAI API for comprehensive answers
- **Fallback**: Local knowledge base with template-based responses
- **Graceful Degradation**: Always provides some response, even without external APIs

### Modern Web Interface

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Real-time Chat**: Interactive conversation interface
- **Suggestion Chips**: Quick access to common questions
- **Loading States**: Visual feedback during processing
- **Error Handling**: Graceful error messages and recovery

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Ukrainian cultural knowledge and traditions
- Open source ML libraries (sentence-transformers, FAISS)
- Flask web framework
- Modern web technologies (HTML5, CSS3, JavaScript)

---

**Слава Україні! 🇺🇦**

*Built with ❤️ for Ukrainian culture and knowledge sharing*
