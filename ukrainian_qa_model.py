import os
import json
import logging
from typing import Dict, List, Optional
import openai
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import pickle
from pathlib import Path

logger = logging.getLogger(__name__)

class UkrainianQAModel:
    """ML model for answering questions about Ukrainian topics"""
    
    def __init__(self):
        self.model_ready = False
        self.embedding_model = None
        self.knowledge_base = []
        self.faiss_index = None
        self.openai_client = None
        
        # Ukrainian knowledge base
        self.ukrainian_knowledge = {
            "history": [
                "Ukraine gained independence from the Soviet Union in 1991",
                "The capital of Ukraine is Kyiv (Kiev)",
                "Ukraine is the largest country entirely in Europe",
                "The Ukrainian language belongs to the East Slavic group",
                "Ukraine has a rich cultural heritage with Cossack traditions"
            ],
            "culture": [
                "Ukrainian embroidery (vyshyvanka) is a traditional craft",
                "Borscht is a famous Ukrainian beet soup",
                "The bandura is a traditional Ukrainian musical instrument",
                "Ukrainian Easter eggs (pysanky) are decorated with wax",
                "The sunflower is Ukraine's national flower"
            ],
            "geography": [
                "Ukraine borders Russia, Belarus, Poland, Slovakia, Hungary, Romania, and Moldova",
                "The Carpathian Mountains are in western Ukraine",
                "The Black Sea borders Ukraine to the south",
                "The Dnieper River is Ukraine's longest river",
                "Ukraine has fertile soil known as 'chernozem'"
            ],
            "politics": [
                "Ukraine is a democratic republic with a president and parliament",
                "The current president is Volodymyr Zelenskyy",
                "Ukraine has been working towards EU and NATO membership",
                "The country has faced challenges with Russian aggression since 2014",
                "Ukraine has made significant progress in democratic reforms"
            ]
        }
        
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the ML model and knowledge base"""
        try:
            # Initialize OpenAI client if API key is available
            openai_api_key = os.getenv('OPENAI_API_KEY')
            if openai_api_key:
                self.openai_client = openai.OpenAI(api_key=openai_api_key)
                logger.info("OpenAI client initialized")
            
            # Initialize sentence transformer for embeddings
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Sentence transformer model loaded")
            
            # Build knowledge base
            self._build_knowledge_base()
            
            # Build FAISS index for similarity search
            self._build_faiss_index()
            
            self.model_ready = True
            logger.info("Ukrainian QA model initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing model: {str(e)}")
            self.model_ready = False
    
    def _build_knowledge_base(self):
        """Build the knowledge base from Ukrainian topics"""
        self.knowledge_base = []
        
        for category, facts in self.ukrainian_knowledge.items():
            for fact in facts:
                self.knowledge_base.append({
                    'text': fact,
                    'category': category,
                    'source': 'ukrainian_knowledge_base'
                })
        
        # Add some common Ukrainian phrases and their meanings
        ukrainian_phrases = [
            "Доброго ранку - Good morning",
            "Дякую - Thank you",
            "Будь ласка - Please/You're welcome",
            "Привіт - Hello",
            "До побачення - Goodbye",
            "Слава Україні - Glory to Ukraine",
            "Героям слава - Glory to the Heroes"
        ]
        
        for phrase in ukrainian_phrases:
            self.knowledge_base.append({
                'text': phrase,
                'category': 'language',
                'source': 'ukrainian_phrases'
            })
        
        logger.info(f"Built knowledge base with {len(self.knowledge_base)} entries")
    
    def _build_faiss_index(self):
        """Build FAISS index for similarity search"""
        if not self.knowledge_base or not self.embedding_model:
            return
        
        # Create embeddings for all knowledge base entries
        texts = [entry['text'] for entry in self.knowledge_base]
        embeddings = self.embedding_model.encode(texts)
        
        # Normalize embeddings
        embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
        
        # Create FAISS index
        dimension = embeddings.shape[1]
        self.faiss_index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
        self.faiss_index.add(embeddings.astype('float32'))
        
        logger.info(f"Built FAISS index with {len(embeddings)} vectors")
    
    def _find_relevant_context(self, question: str, top_k: int = 3) -> List[str]:
        """Find relevant context from knowledge base using similarity search"""
        if not self.faiss_index or not self.embedding_model:
            return []
        
        # Encode the question
        question_embedding = self.embedding_model.encode([question])
        question_embedding = question_embedding / np.linalg.norm(question_embedding, axis=1, keepdims=True)
        
        # Search for similar entries
        scores, indices = self.faiss_index.search(question_embedding.astype('float32'), top_k)
        
        relevant_contexts = []
        for idx in indices[0]:
            if idx < len(self.knowledge_base):
                relevant_contexts.append(self.knowledge_base[idx]['text'])
        
        return relevant_contexts
    
    def _get_openai_answer(self, question: str, context: List[str]) -> str:
        """Get answer using OpenAI API"""
        if not self.openai_client:
            return "I'm sorry, but I don't have access to advanced AI capabilities at the moment."
        
        try:
            context_text = "\n".join(context) if context else "No specific context available."
            
            prompt = f"""You are a helpful assistant specializing in Ukrainian culture, history, geography, and language. 
            Answer the following question about Ukraine based on the provided context and your knowledge.
            
            Context:
            {context_text}
            
            Question: {question}
            
            Please provide a comprehensive and accurate answer about Ukrainian topics. If the question is not related to Ukraine, politely redirect the conversation to Ukrainian topics."""
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant specializing in Ukrainian culture, history, geography, and language."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error getting OpenAI answer: {str(e)}")
            return "I'm sorry, but I encountered an error while processing your question."
    
    def _get_local_answer(self, question: str, context: List[str]) -> str:
        """Get answer using local knowledge base"""
        if not context:
            return "I don't have specific information about that topic in my Ukrainian knowledge base. Could you ask about Ukrainian history, culture, geography, or language?"
        
        # Simple template-based response
        context_text = " ".join(context)
        
        if "language" in question.lower() or "ukrainian" in question.lower():
            return f"Based on my knowledge: {context_text}"
        elif "history" in question.lower():
            return f"From Ukrainian history: {context_text}"
        elif "culture" in question.lower():
            return f"In Ukrainian culture: {context_text}"
        elif "geography" in question.lower():
            return f"Regarding Ukrainian geography: {context_text}"
        else:
            return f"Here's what I know about Ukraine: {context_text}"
    
    def get_answer(self, question: str) -> str:
        """Get answer for a question about Ukrainian topics"""
        if not self.model_ready:
            return "I'm sorry, but the model is not ready yet. Please try again in a moment."
        
        # Find relevant context
        context = self._find_relevant_context(question)
        
        # Try OpenAI first, fallback to local model
        if self.openai_client:
            return self._get_openai_answer(question, context)
        else:
            return self._get_local_answer(question, context)
    
    def is_ready(self) -> bool:
        """Check if the model is ready to use"""
        return self.model_ready
    
    def get_knowledge_stats(self) -> Dict:
        """Get statistics about the knowledge base"""
        if not self.knowledge_base:
            return {"total_entries": 0, "categories": {}}
        
        categories = {}
        for entry in self.knowledge_base:
            cat = entry['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        return {
            "total_entries": len(self.knowledge_base),
            "categories": categories
        }
