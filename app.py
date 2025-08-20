from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from ukrainian_qa_model import UkrainianQAModel
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Initialize the Ukrainian QA model
qa_model = UkrainianQAModel()

@app.route('/')
def index():
    """Main page with the Ukrainian Q&A interface"""
    return render_template('index.html')

@app.route('/api/ask', methods=['POST'])
def ask_question():
    """API endpoint to handle questions about Ukrainian topics"""
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({'error': 'Question is required'}), 400
        
        logger.info(f"Received question: {question}")
        
        # Get answer from the model
        answer = qa_model.get_answer(question)
        
        return jsonify({
            'question': question,
            'answer': answer,
            'success': True
        })
        
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        return jsonify({
            'error': 'An error occurred while processing your question',
            'success': False
        }), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'model_loaded': qa_model.is_ready()})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting Ukrainian Q&A application on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
