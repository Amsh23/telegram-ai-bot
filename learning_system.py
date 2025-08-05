#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 Advanced Learning System for Telegram AI Bot
Machine Learning system that learns from conversations
"""

import json
import os
import numpy as np
import tensorflow as tf
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import logging
from collections import defaultdict
import re
from hazm import Normalizer, word_tokenize

class ConversationLearner:
    """🧠 Advanced conversation learning system"""
    
    def __init__(self, data_dir="conversation_data"):
        # Setup logging first
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        self.data_dir = data_dir
        self.conversation_file = os.path.join(data_dir, "conversations.json")
        self.patterns_file = os.path.join(data_dir, "learned_patterns.json")
        self.model_file = os.path.join(data_dir, "response_model.pkl")
        self.vectorizer_file = os.path.join(data_dir, "vectorizer.pkl")
        
        # Initialize components
        self.normalizer = Normalizer()
        self.vectorizer = None
        self.response_patterns = {}
        self.conversations = []
        self.user_style = {}
        self.response_history = defaultdict(list)
        
        # Create data directory
        os.makedirs(data_dir, exist_ok=True)
        
        # Load existing data
        self.load_data()
        
        print("🧠 Learning System initialized successfully!")
    
    def load_data(self):
        """📂 Load existing conversation data and patterns"""
        try:
            # Load conversations
            if os.path.exists(self.conversation_file):
                with open(self.conversation_file, 'r', encoding='utf-8') as f:
                    self.conversations = json.load(f)
                self.logger.info(f"📚 Loaded {len(self.conversations)} conversations")
            
            # Load learned patterns
            if os.path.exists(self.patterns_file):
                with open(self.patterns_file, 'r', encoding='utf-8') as f:
                    self.response_patterns = json.load(f)
                self.logger.info(f"🎯 Loaded {len(self.response_patterns)} response patterns")
            
            # Load vectorizer
            if os.path.exists(self.vectorizer_file):
                with open(self.vectorizer_file, 'rb') as f:
                    self.vectorizer = pickle.load(f)
                self.logger.info("📊 Vectorizer loaded successfully")
            
        except Exception as e:
            self.logger.error(f"❌ Error loading data: {e}")
    
    def save_data(self):
        """💾 Save conversation data and learned patterns"""
        try:
            # Save conversations
            with open(self.conversation_file, 'w', encoding='utf-8') as f:
                json.dump(self.conversations, f, ensure_ascii=False, indent=2)
            
            # Save patterns
            with open(self.patterns_file, 'w', encoding='utf-8') as f:
                json.dump(self.response_patterns, f, ensure_ascii=False, indent=2)
            
            # Save vectorizer
            if self.vectorizer:
                with open(self.vectorizer_file, 'wb') as f:
                    pickle.dump(self.vectorizer, f)
            
            self.logger.info("💾 Data saved successfully")
            
        except Exception as e:
            self.logger.error(f"❌ Error saving data: {e}")
    
    def preprocess_text(self, text):
        """🔄 Preprocess and normalize text"""
        if not text:
            return ""
        
        # Normalize Persian text
        text = self.normalizer.normalize(text)
        
        # Clean text
        text = re.sub(r'[^\w\s\u0600-\u06FF\u200C\u200D]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        text = text.strip().lower()
        
        return text
    
    def extract_features(self, text):
        """🔍 Extract linguistic features from text"""
        features = {
            'length': len(text),
            'word_count': len(text.split()),
            'has_question': '?' in text or any(q in text for q in ['چی', 'کی', 'کجا', 'چرا', 'چطور']),
            'has_greeting': any(g in text for g in ['سلام', 'درود', 'hello', 'hi']),
            'has_thanks': any(t in text for t in ['ممنون', 'مرسی', 'متشکر', 'thank']),
            'has_goodbye': any(b in text for b in ['خداحافظ', 'فعلا', 'bye', 'goodbye']),
            'language': 'persian' if re.search(r'[\u0600-\u06FF]', text) else 'english',
            'sentiment': self.detect_sentiment(text)
        }
        
        return features
    
    def detect_sentiment(self, text):
        """😊 Simple sentiment detection"""
        positive_words = ['خوب', 'عالی', 'ممنون', 'مرسی', 'good', 'great', 'thanks', 'nice']
        negative_words = ['بد', 'غمگین', 'ناراحت', 'bad', 'sad', 'angry', 'upset']
        
        text_lower = text.lower()
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        if pos_count > neg_count:
            return 'positive'
        elif neg_count > pos_count:
            return 'negative'
        else:
            return 'neutral'
    
    def learn_from_conversation(self, user_message, bot_response, context=None):
        """🎓 Learn from a conversation exchange"""
        try:
            # Preprocess messages
            clean_user = self.preprocess_text(user_message)
            clean_response = self.preprocess_text(bot_response)
            
            if not clean_user or not clean_response:
                return
            
            # Extract features
            user_features = self.extract_features(clean_user)
            
            # Create conversation entry
            conversation = {
                'timestamp': datetime.now().isoformat(),
                'user_message': clean_user,
                'bot_response': clean_response,
                'user_features': user_features,
                'context': context or {}
            }
            
            # Add to conversations
            self.conversations.append(conversation)
            
            # Learn response patterns
            self.learn_response_pattern(clean_user, clean_response, user_features)
            
            # Update user style analysis
            self.analyze_user_style(clean_user, user_features)
            
            # Retrain model periodically
            if len(self.conversations) % 10 == 0:
                self.retrain_model()
            
            # Save data
            self.save_data()
            
            self.logger.info(f"🎓 Learned from conversation: '{clean_user[:30]}...'")
            
        except Exception as e:
            self.logger.error(f"❌ Error learning from conversation: {e}")
    
    def learn_response_pattern(self, user_message, bot_response, features):
        """🎯 Learn response patterns based on message features"""
        # Create pattern key based on features
        pattern_key = f"{features['language']}_{features['sentiment']}"
        
        if features['has_question']:
            pattern_key += "_question"
        elif features['has_greeting']:
            pattern_key += "_greeting"
        elif features['has_thanks']:
            pattern_key += "_thanks"
        elif features['has_goodbye']:
            pattern_key += "_goodbye"
        else:
            pattern_key += "_statement"
        
        # Store response pattern
        if pattern_key not in self.response_patterns:
            self.response_patterns[pattern_key] = []
        
        self.response_patterns[pattern_key].append({
            'input': user_message,
            'response': bot_response,
            'frequency': 1
        })
        
        # Limit pattern storage
        if len(self.response_patterns[pattern_key]) > 20:
            self.response_patterns[pattern_key] = self.response_patterns[pattern_key][-20:]
    
    def analyze_user_style(self, message, features):
        """👤 Analyze user communication style"""
        style_key = f"{features['language']}_{features['sentiment']}"
        
        if style_key not in self.user_style:
            self.user_style[style_key] = {
                'avg_length': 0,
                'common_words': defaultdict(int),
                'preferred_expressions': [],
                'count': 0
            }
        
        style = self.user_style[style_key]
        style['count'] += 1
        
        # Update average length
        style['avg_length'] = (style['avg_length'] * (style['count'] - 1) + features['length']) / style['count']
        
        # Count words
        words = message.split()
        for word in words:
            if len(word) > 2:  # Only meaningful words
                style['common_words'][word] += 1
    
    def retrain_model(self):
        """🔄 Retrain the response model with new data"""
        try:
            if len(self.conversations) < 5:
                return
            
            # Prepare training data
            texts = []
            responses = []
            
            for conv in self.conversations:
                texts.append(conv['user_message'])
                responses.append(conv['bot_response'])
            
            # Create or update vectorizer
            if not self.vectorizer:
                self.vectorizer = TfidfVectorizer(
                    max_features=1000,
                    ngram_range=(1, 2),
                    min_df=1
                )
                text_vectors = self.vectorizer.fit_transform(texts)
            else:
                text_vectors = self.vectorizer.transform(texts)
            
            self.logger.info(f"🔄 Model retrained with {len(texts)} conversations")
            
        except Exception as e:
            self.logger.error(f"❌ Error retraining model: {e}")
    
    def generate_learned_response(self, user_message):
        """🤖 Generate response based on learned patterns"""
        try:
            clean_message = self.preprocess_text(user_message)
            features = self.extract_features(clean_message)
            
            # Try pattern-based response first
            pattern_response = self.get_pattern_response(clean_message, features)
            if pattern_response:
                return pattern_response
            
            # Try similarity-based response
            similarity_response = self.get_similarity_response(clean_message)
            if similarity_response:
                return similarity_response
            
            # Generate style-aware response
            style_response = self.generate_style_aware_response(features)
            return style_response
            
        except Exception as e:
            self.logger.error(f"❌ Error generating learned response: {e}")
            return None
    
    def get_pattern_response(self, message, features):
        """🎯 Get response based on learned patterns"""
        pattern_key = f"{features['language']}_{features['sentiment']}"
        
        if features['has_question']:
            pattern_key += "_question"
        elif features['has_greeting']:
            pattern_key += "_greeting"
        elif features['has_thanks']:
            pattern_key += "_thanks"
        elif features['has_goodbye']:
            pattern_key += "_goodbye"
        else:
            pattern_key += "_statement"
        
        if pattern_key in self.response_patterns:
            patterns = self.response_patterns[pattern_key]
            if patterns:
                # Return most frequent response or random
                import random
                return random.choice(patterns)['response']
        
        return None
    
    def get_similarity_response(self, message):
        """🔍 Get response based on message similarity"""
        if not self.vectorizer or len(self.conversations) < 3:
            return None
        
        try:
            # Vectorize input message
            message_vector = self.vectorizer.transform([message])
            
            # Get all conversation texts
            conv_texts = [conv['user_message'] for conv in self.conversations]
            conv_vectors = self.vectorizer.transform(conv_texts)
            
            # Calculate similarities
            similarities = cosine_similarity(message_vector, conv_vectors)[0]
            
            # Find best match
            best_idx = np.argmax(similarities)
            if similarities[best_idx] > 0.3:  # Threshold for similarity
                return self.conversations[best_idx]['bot_response']
        
        except Exception as e:
            self.logger.error(f"❌ Error in similarity matching: {e}")
        
        return None
    
    def generate_style_aware_response(self, features):
        """🎨 Generate response that matches user communication style"""
        language = features['language']
        sentiment = features['sentiment']
        
        # Style-aware responses
        if language == 'persian':
            if sentiment == 'positive':
                responses = [
                    "آره دقیقاً! منم همینو فکر می‌کردم! 😊",
                    "وای عالیه! خیلی جالبه این موضوع! ✨",
                    "حق با توعه! کاملاً موافقم! 👍"
                ]
            elif sentiment == 'negative':
                responses = [
                    "آخ متأسفم 😔 امیدوارم حالت بهتر بشه",
                    "نه بابا! چه بدی! امیدوارم درست بشه 🙁",
                    "وای چقدر ناراحت‌کننده! صبر کن ببینم چیکار می‌تونم بکنم"
                ]
            else:
                responses = [
                    "آها، فهمیدم! جالب بود که گفتی 🤔",
                    "اوکی، گرفتم! یه سوال دیگه هم داری؟",
                    "باشه عزیزم! هر چی بخوای بگو!"
                ]
        else:
            if sentiment == 'positive':
                responses = [
                    "That's awesome! I totally agree! 😊",
                    "Great point! Really interesting! ✨",
                    "Exactly! You're absolutely right! 👍"
                ]
            elif sentiment == 'negative':
                responses = [
                    "Oh no, I'm sorry to hear that 😔",
                    "That's really unfortunate! Hope it gets better 🙁",
                    "Aw, that's tough! Let me see how I can help"
                ]
            else:
                responses = [
                    "I see! That's interesting to know 🤔",
                    "Got it! Anything else you'd like to discuss?",
                    "Okay! Feel free to ask me anything!"
                ]
        
        import random
        return random.choice(responses)
    
    def get_learning_stats(self):
        """📊 Get learning system statistics"""
        return {
            'total_conversations': len(self.conversations),
            'learned_patterns': len(self.response_patterns),
            'user_styles': len(self.user_style),
            'last_update': datetime.now().isoformat(),
            'data_quality': self.calculate_data_quality()
        }
    
    def calculate_data_quality(self):
        """📈 Calculate quality of learned data"""
        if not self.conversations:
            return 0
        
        # Simple quality metrics
        avg_length = np.mean([len(conv['user_message']) for conv in self.conversations])
        language_diversity = len(set([conv['user_features']['language'] for conv in self.conversations]))
        pattern_coverage = len(self.response_patterns) / max(len(self.conversations), 1)
        
        quality_score = min(100, (avg_length/10 + language_diversity*20 + pattern_coverage*30))
        return round(quality_score, 1)

# Global learning system instance
learning_system = ConversationLearner()

def learn_from_interaction(user_message, bot_response, context=None):
    """🎓 Easy function to learn from interactions"""
    learning_system.learn_from_conversation(user_message, bot_response, context)

def get_learned_response(user_message):
    """🤖 Easy function to get learned response"""
    return learning_system.generate_learned_response(user_message)

def get_stats():
    """📊 Easy function to get learning stats"""
    return learning_system.get_learning_stats()

if __name__ == "__main__":
    # Test the learning system
    learner = ConversationLearner()
    
    # Example learning
    learner.learn_from_conversation("سلام چطوری؟", "سلام عزیزم! خوبم ممنون! تو چطوری؟")
    learner.learn_from_conversation("خوبم مرسی", "خوشحالم که خوبی! چه خبر؟")
    
    # Test response generation
    response = learner.generate_learned_response("سلام")
    print(f"Generated response: {response}")
    
    # Show stats
    stats = learner.get_learning_stats()
    print(f"Learning stats: {stats}")
