#!/usr/bin/env python3
"""
Simple standalone Ukrainian Q&A application
No external dependencies required - uses only Python standard library
"""

import http.server
import socketserver
import json
import urllib.parse
import os
import sys

class UkrainianQA:
    """Simple Ukrainian Q&A system using only standard library"""
    
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

# Initialize the QA system
qa_system = UkrainianQA()

class UkrainianQAHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP request handler for Ukrainian Q&A"""
    
    def do_GET(self):
        """Handle GET requests"""
        # Handle both '/' and '/?' paths
        if self.path in ['/', '/?', '/index.html']:
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
            self.end_headers()
            self.wfile.write(self.get_html_page().encode('utf-8'))
        elif self.path == '/api/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'status': 'healthy', 'model_loaded': True, 'version': 'simple'}
            self.wfile.write(json.dumps(response).encode())
        elif self.path == '/api/topics':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            topics = list(qa_system.knowledge_base.keys())
            response = {'topics': topics, 'count': len(topics)}
            self.wfile.write(json.dumps(response).encode())
        else:
            # For any other path, redirect to main page
            self.send_response(302)
            self.send_header('Location', '/')
            self.end_headers()
    
    def do_POST(self):
        """Handle POST requests"""
        print(f"Received POST request to: {self.path}")
        
        if self.path == '/api/ask':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                print(f"Received data: {post_data.decode('utf-8')}")
                
                data = json.loads(post_data.decode('utf-8'))
                question = data.get('question', '').strip()
                
                if not question:
                    response = {'error': 'Question is required', 'success': False}
                else:
                    answer = qa_system.get_answer(question)
                    response = {
                        'question': question,
                        'answer': answer,
                        'success': True
                    }
                
                print(f"Sending response: {response}")
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                print(f"Error processing request: {e}")
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {'error': f'An error occurred: {str(e)}', 'success': False}
                self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def get_html_page(self):
        """Return the HTML page for the Ukrainian Q&A interface"""
        return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ukrainian Q&A - AI Assistant</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: #000000;
            color: #ffffff;
            line-height: 1.6;
            overflow-x: hidden;
        }
        
        /* Cursor-style gradient background */
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
                        radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
                        radial-gradient(circle at 40% 40%, rgba(120, 219, 255, 0.2) 0%, transparent 50%);
            z-index: -1;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
            min-height: 100vh;
        }
        
        /* Header Section - Cursor Style */
        .header {
            text-align: center;
            margin-bottom: 60px;
            padding: 60px 0;
        }
        
        .header h1 {
            font-size: 4rem;
            font-weight: 800;
            background: linear-gradient(135deg, #ffffff 0%, #a8a8a8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 20px;
            letter-spacing: -0.02em;
        }
        
        .header .subtitle {
            font-size: 1.5rem;
            color: #a8a8a8;
            margin-bottom: 40px;
            font-weight: 400;
        }
        
        .header .description {
            font-size: 1.1rem;
            color: #666666;
            max-width: 600px;
            margin: 0 auto;
            line-height: 1.7;
        }
        
        /* Main Chat Interface */
        .chat-interface {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 24px;
            padding: 40px;
            backdrop-filter: blur(20px);
            margin-bottom: 40px;
        }
        
        .input-group {
            display: flex;
            gap: 16px;
            margin-bottom: 30px;
            align-items: center;
        }
        
        input[type="text"] {
            flex: 1;
            padding: 20px 24px;
            font-size: 16px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            color: #ffffff;
            outline: none;
            transition: all 0.3s ease;
            font-weight: 400;
        }
        
        input[type="text"]::placeholder {
            color: #666666;
        }
        
        input[type="text"]:focus {
            border-color: #ffffff;
            background: rgba(255, 255, 255, 0.08);
            box-shadow: 0 0 0 4px rgba(255, 255, 255, 0.1);
        }
        
        button {
            padding: 20px 32px;
            font-size: 16px;
            font-weight: 600;
            background: linear-gradient(135deg, #ffffff 0%, #e0e0e0 100%);
            color: #000000;
            border: none;
            border-radius: 16px;
            cursor: pointer;
            transition: all 0.3s ease;
            white-space: nowrap;
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(255, 255, 255, 0.2);
        }
        
        button:active {
            transform: translateY(0);
        }
        
        /* Chat Area */
        .chat {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 20px;
            padding: 30px;
            height: 500px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        
        .chat::-webkit-scrollbar {
            width: 6px;
        }
        
        .chat::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
        }
        
        .chat::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.2);
            border-radius: 10px;
        }
        
        .message {
            padding: 20px 24px;
            border-radius: 16px;
            max-width: 80%;
            word-wrap: break-word;
            position: relative;
            animation: fadeInUp 0.4s ease;
            font-size: 15px;
            line-height: 1.6;
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .user-message {
            background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%);
            color: #000000;
            align-self: flex-end;
            margin-left: auto;
            border-bottom-right-radius: 8px;
            font-weight: 500;
        }
        
        .bot-message {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            align-self: flex-start;
            margin-right: auto;
            border-bottom-left-radius: 8px;
            color: #ffffff;
        }
        
        /* Suggestions Section */
        .suggestions {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
        }
        
        .suggestions h3 {
            color: #ffffff;
            margin-bottom: 20px;
            font-size: 1.3rem;
            font-weight: 600;
        }
        
        .suggestion {
            display: inline-block;
            margin: 8px;
            padding: 12px 20px;
            background: rgba(255, 255, 255, 0.05);
            color: #ffffff;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.3s ease;
            font-weight: 400;
        }
        
        .suggestion:hover {
            background: rgba(255, 255, 255, 0.1);
            transform: translateY(-2px);
            border-color: rgba(255, 255, 255, 0.2);
        }
        
        /* Status */
        .status {
            text-align: center;
            padding: 20px;
            background: rgba(76, 175, 80, 0.1);
            border: 1px solid rgba(76, 175, 80, 0.2);
            border-radius: 16px;
            color: #4caf50;
            font-weight: 500;
        }
        
        .typing-indicator {
            display: none;
            align-self: flex-start;
            margin-right: auto;
            padding: 20px 24px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            border-bottom-left-radius: 8px;
            color: #666666;
            font-style: italic;
            animation: pulse 1.5s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 0.6; }
            50% { opacity: 1; }
        }
        
        /* Features Section - Cursor Style */
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin: 60px 0;
        }
        
        .feature {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 20px;
            padding: 30px;
            text-align: center;
        }
        
        .feature h3 {
            color: #ffffff;
            font-size: 1.4rem;
            margin-bottom: 15px;
            font-weight: 600;
        }
        
        .feature p {
            color: #666666;
            line-height: 1.6;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .container {
                padding: 20px 15px;
            }
            
            .header h1 {
                font-size: 2.5rem;
            }
            
            .header .subtitle {
                font-size: 1.2rem;
            }
            
            .chat-interface {
                padding: 20px;
            }
            
            .input-group {
                flex-direction: column;
            }
            
            .message {
                max-width: 95%;
            }
            
            .features {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Header Section -->
        <div class="header">
            <h1>The Ukrainian Q&A</h1>
            <div class="subtitle">AI Assistant</div>
            <div class="description">
                Built to help you learn about Ukrainian culture, history, geography, and language. 
                Ask me anything and get instant, accurate answers powered by AI.
            </div>
        </div>
        
        <!-- Main Chat Interface -->
        <div class="chat-interface">
            <div class="input-group">
                <input type="text" id="questionInput" placeholder="Ask me about Ukrainian culture, history, or language..." onkeypress="handleKeyPress(event)">
                <button onclick="askQuestion()">Ask Question</button>
            </div>
            
            <div class="chat" id="chatContainer">
                <div class="message bot-message">
                    Привіт! Hello! I'm your Ukrainian Q&A assistant. Ask me anything about Ukrainian culture, history, geography, or language!
                </div>
                <div class="typing-indicator" id="typingIndicator">AI is thinking...</div>
            </div>
        </div>
        
        <!-- Suggestions -->
        <div class="suggestions">
            <h3>💡 Try these questions:</h3>
            <div class="suggestion" onclick="askQuestion('What is the capital of Ukraine?')">Capital of Ukraine</div>
            <div class="suggestion" onclick="askQuestion('Tell me about Ukrainian borscht')">Ukrainian Borscht</div>
            <div class="suggestion" onclick="askQuestion('What does Слава Україні mean?')">Слава Україні</div>
            <div class="suggestion" onclick="askQuestion('Ukrainian independence history')">Independence History</div>
            <div class="suggestion" onclick="askQuestion('Geography of Ukraine')">Ukrainian Geography</div>
            <div class="suggestion" onclick="askQuestion('Hello')">Say Hello</div>
        </div>
        
        <!-- Features Section -->
        <div class="features">
            <div class="feature">
                <h3>🇺🇦 Cultural Knowledge</h3>
                <p>Learn about Ukrainian traditions, food, music, and cultural heritage with detailed explanations.</p>
            </div>
            <div class="feature">
                <h3>📚 Historical Insights</h3>
                <p>Discover Ukraine's rich history from ancient times to modern independence and current events.</p>
            </div>
            <div class="feature">
                <h3>🗺️ Geographic Facts</h3>
                <p>Explore Ukraine's geography, borders, natural resources, and beautiful landscapes.</p>
            </div>
        </div>
        
        <!-- Status -->
        <div class="status">
            ✅ Server is running - AI is ready to help!
        </div>
    </div>

    <script>
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                askQuestion();
            }
        }
        
        function askQuestion(predefinedQuestion) {
            var question = predefinedQuestion || document.getElementById('questionInput').value.trim();
            
            if (!question) {
                alert('Please enter a question!');
                return;
            }
            
            // Add user message
            addMessage('user', question);
            
            // Clear input if it was typed
            if (!predefinedQuestion) {
                document.getElementById('questionInput').value = '';
            }
            
            // Show typing indicator
            var typingIndicator = document.getElementById('typingIndicator');
            typingIndicator.style.display = 'block';
            
            // Make API request
            var xhr = new XMLHttpRequest();
            xhr.open('POST', '/api/ask', true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            
            xhr.onreadystatechange = function() {
                if (xhr.readyState === 4) {
                    // Hide typing indicator
                    typingIndicator.style.display = 'none';
                    
                    if (xhr.status === 200) {
                        try {
                            var response = JSON.parse(xhr.responseText);
                            if (response.success) {
                                addMessage('bot', response.answer);
                            } else {
                                addMessage('bot', 'Error: ' + (response.error || 'Unknown error'));
                            }
                        } catch (e) {
                            addMessage('bot', 'Error parsing response: ' + e.message);
                        }
                    } else {
                        addMessage('bot', 'Error: HTTP ' + xhr.status);
                    }
                }
            };
            
            xhr.send(JSON.stringify({question: question}));
        }
        
        function addMessage(sender, content) {
            var chatContainer = document.getElementById('chatContainer');
            var messageDiv = document.createElement('div');
            messageDiv.className = 'message ' + sender + '-message';
            
            // Just add the content without sender labels for cleaner look
            messageDiv.textContent = content;
            
            chatContainer.appendChild(messageDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
    </script>
</body>
</html>
        '''

def main():
    """Main function to start the server"""
    PORT = 9999
    
    print("🇺🇦 Simple Ukrainian Q&A Application")
    print("=" * 50)
    print("✅ No external dependencies required!")
    print("🌐 Starting server on port 9999...")
    print("📱 Open your browser and go to: http://localhost:9999")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        with socketserver.TCPServer(("", PORT), UkrainianQAHandler) as httpd:
            print(f"Server started at http://localhost:{PORT}")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    main()
