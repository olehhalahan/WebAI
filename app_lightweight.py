from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
import logging
import re

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class LightweightUkrainianQA:
    """Lightweight Ukrainian Q&A system without heavy ML dependencies"""
    
    def __init__(self):
        self.knowledge_base = {
            "capital": {
                "keywords": ["capital", "kyiv", "kiev", "main city"],
                "answer": "The capital of Ukraine is Kyiv (also spelled Kiev). It's the largest city in Ukraine and serves as the political, economic, and cultural center of the country."
            },
            "borscht": {
                "keywords": ["borscht", "borsch", "soup", "traditional food"],
                "answer": "Borscht is a famous Ukrainian beet soup that's considered a national dish. It's made with beets, cabbage, potatoes, and often includes meat. The soup has a distinctive red color and is served with sour cream and fresh dill."
            },
            "slava_ukraini": {
                "keywords": ["слава україні", "slava ukraini", "glory", "slogan"],
                "answer": "'Слава Україні' (Slava Ukraini) means 'Glory to Ukraine' in Ukrainian. It's a patriotic slogan that has become a symbol of Ukrainian national identity and resistance. The traditional response is 'Героям слава' (Heroiam slava) which means 'Glory to the Heroes.'"
            },
            "independence": {
                "keywords": ["independence", "1991", "soviet union", "freedom"],
                "answer": "Ukraine gained independence from the Soviet Union on August 24, 1991, when the Ukrainian parliament declared independence. This followed the failed coup attempt in Moscow and the collapse of the Soviet Union. Ukraine became a sovereign nation after centuries of foreign rule."
            },
            "geography": {
                "keywords": ["geography", "borders", "mountains", "rivers", "black sea"],
                "answer": "Ukraine is the largest country entirely in Europe. It borders Russia, Belarus, Poland, Slovakia, Hungary, Romania, and Moldova. The Carpathian Mountains are in western Ukraine, the Black Sea borders the south, and the Dnieper River is the longest river. Ukraine has fertile soil known as 'chernozem.'"
            },
            "culture": {
                "keywords": ["culture", "traditional", "embroidery", "vyshyvanka", "bandura"],
                "answer": "Ukrainian culture is rich and diverse. Traditional crafts include embroidery (vyshyvanka), Easter egg decorating (pysanky), and pottery. The bandura is a traditional musical instrument. Ukrainian folk music and dance are important cultural expressions."
            },
            "language": {
                "keywords": ["language", "ukrainian", "phrases", "words"],
                "answer": "Ukrainian is the official language of Ukraine, belonging to the East Slavic group. Common phrases include: 'Привіт' (Hello), 'Дякую' (Thank you), 'Будь ласка' (Please/You're welcome), 'До побачення' (Goodbye)."
            },
            "politics": {
                "keywords": ["politics", "president", "zelensky", "government", "democracy"],
                "answer": "Ukraine is a democratic republic with a president and parliament. The current president is Volodymyr Zelenskyy. Ukraine has been working towards EU and NATO membership and has made significant progress in democratic reforms."
            },
            "food": {
                "keywords": ["food", "cuisine", "dishes", "vareniki", "holubtsi"],
                "answer": "Ukrainian cuisine features hearty, flavorful dishes. Popular foods include vareniki (dumplings), holubtsi (cabbage rolls), kasha (porridge), and various types of bread. Ukrainian food often uses ingredients like potatoes, cabbage, beets, and sour cream."
            },
            "history": {
                "keywords": ["history", "historical", "past", "ancient", "medieval"],
                "answer": "Ukraine has a rich history dating back to ancient times. It was part of Kyivan Rus' in the medieval period, then came under various foreign rulers including the Polish-Lithuanian Commonwealth, Russian Empire, and Soviet Union. Ukraine has a strong cultural heritage with Cossack traditions."
            }
        }
    
    def find_best_match(self, question):
        """Find the best matching knowledge base entry"""
        question_lower = question.lower()
        best_match = None
        best_score = 0
        
        for topic, data in self.knowledge_base.items():
            score = 0
            for keyword in data["keywords"]:
                if keyword in question_lower:
                    score += 1
            
            if score > best_score:
                best_score = score
                best_match = topic
        
        return best_match if best_score > 0 else None
    
    def get_answer(self, question):
        """Get answer for a question about Ukrainian topics"""
        if not question.strip():
            return "Please ask a question about Ukrainian topics."
        
        # Check for specific patterns
        question_lower = question.lower()
        
        # Handle greetings
        if any(word in question_lower for word in ["hello", "hi", "привіт", "greetings"]):
            return "Привіт! Hello! I'm your Ukrainian Q&A assistant. Ask me anything about Ukrainian culture, history, geography, or language! 🇺🇦"
        
        # Handle thanks
        if any(word in question_lower for word in ["thank", "дякую", "thanks"]):
            return "Будь ласка! You're welcome! I'm happy to help you learn about Ukraine! 🇺🇦"
        
        # Find best matching topic
        best_match = self.find_best_match(question)
        
        if best_match:
            return self.knowledge_base[best_match]["answer"]
        
        # Default response for unmatched questions
        return ("I don't have specific information about that topic in my knowledge base. "
                "Try asking about Ukrainian history, culture, geography, language, food, or politics. "
                "For example: 'What is the capital of Ukraine?' or 'Tell me about Ukrainian borscht'")

# Initialize the lightweight QA system
qa_system = LightweightUkrainianQA()

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
        
        # Get answer from the lightweight system
        answer = qa_system.get_answer(question)
        
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
    return jsonify({
        'status': 'healthy', 
        'model_loaded': True,
        'version': 'lightweight'
    })

@app.route('/api/topics')
def get_topics():
    """Get available topics"""
    topics = list(qa_system.knowledge_base.keys())
    return jsonify({
        'topics': topics,
        'count': len(topics)
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting Lightweight Ukrainian Q&A application on port {port}")
    print("🇺🇦 Lightweight Ukrainian Q&A Application")
    print("=" * 50)
    print("✅ No heavy ML dependencies required")
    print("🌐 Open your browser and go to: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=port, debug=debug)
