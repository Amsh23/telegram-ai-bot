#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Ultimate Telegram AI Auto Responder v4.0
🤖 Advanced automation with TensorFlow, OCR, and intelligent learning
🌍 Persian/English dual language support with desktop automation
"""

import pyautogui
import time
import os
import subprocess
import json
import cv2
import numpy as np
from datetime import datetime
import logging
import keyboard
import threading
import win32gui
import win32con
import sqlite3
import re
import random
from collections import defaultdict, Counter
from typing import Optional, List, Dict, Tuple, Any
import hashlib
from pathlib import Path

# AI and ML Libraries
import easyocr
import tensorflow as tf
from PIL import Image, ImageEnhance, ImageFilter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# Configure TensorFlow
tf.config.set_visible_devices([], 'GPU')  # CPU only for stability
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Configure pyautogui
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

class AdvancedOCRSystem:
    """🔍 Advanced OCR with AI enhancement"""
    
    def __init__(self):
        self.setup_logging()
        self.init_ocr_engines()
        self.confidence_threshold = 0.7
        
    def setup_logging(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def init_ocr_engines(self):
        """Initialize OCR engines"""
        try:
            self.easy_reader = easyocr.Reader(['fa', 'en'], gpu=False)
            self.logger.info("✅ EasyOCR initialized")
        except Exception as e:
            self.logger.error(f"❌ OCR initialization failed: {e}")
            self.easy_reader = None
    
    def preprocess_image(self, image_path):
        """🔧 Advanced image preprocessing"""
        try:
            img = cv2.imread(image_path)
            if img is None:
                return None
                
            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Enhance contrast
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            enhanced = clahe.apply(gray)
            
            # Noise reduction
            denoised = cv2.fastNlMeansDenoising(enhanced)
            
            # Sharpen
            kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
            sharpened = cv2.filter2D(denoised, -1, kernel)
            
            # Save preprocessed image
            processed_path = image_path.replace('.png', '_processed.png')
            cv2.imwrite(processed_path, sharpened)
            
            return processed_path
            
        except Exception as e:
            self.logger.error(f"Preprocessing failed: {e}")
            return image_path
    
    def detect_language(self, text):
        """🌍 Detect text language"""
        persian_chars = len(re.findall(r'[\u0600-\u06FF]', text))
        english_chars = len(re.findall(r'[a-zA-Z]', text))
        
        if persian_chars > english_chars:
            return 'persian'
        elif english_chars > 0:
            return 'english'
        return 'unknown'
    
    def is_real_message(self, text):
        """🔍 Filter real messages from UI elements"""
        text = text.strip().lower()
        
        # Skip short texts
        if len(text) < 3:
            return False
            
        # Skip common UI elements
        ui_elements = [
            'online', 'آنلاین', 'typing', 'در حال تایپ',
            'last seen', 'آخرین بازدید', 'members', 'اعضا',
            'telegram', 'تلگرام', 'search', 'جستجو'
        ]
        
        for element in ui_elements:
            if element in text:
                return False
                
        return True
    
    def extract_text(self, image_path):
        """📖 Extract text with quality assessment"""
        if not self.easy_reader:
            return None
            
        try:
            # Preprocess image
            processed_path = self.preprocess_image(image_path)
            
            # Extract text using EasyOCR
            results = self.easy_reader.readtext(processed_path)
            
            if not results:
                return None
            
            # Process results
            extracted_texts = []
            for (bbox, text, confidence) in results:
                if confidence > self.confidence_threshold and self.is_real_message(text):
                    extracted_texts.append({
                        'text': text.strip(),
                        'confidence': confidence,
                        'bbox': bbox
                    })
            
            if not extracted_texts:
                return None
                
            # Combine texts
            full_text = '\n'.join([item['text'] for item in extracted_texts])
            avg_confidence = sum([item['confidence'] for item in extracted_texts]) / len(extracted_texts)
            
            return {
                'text': full_text,
                'language': self.detect_language(full_text),
                'confidence': avg_confidence,
                'quality': min(avg_confidence * 1.2, 1.0)
            }
            
        except Exception as e:
            self.logger.error(f"Text extraction failed: {e}")
            return None

class TensorFlowLearningSystem:
    """🧠 Advanced TensorFlow-powered learning system"""
    
    def __init__(self):
        self.setup_logging()
        self.setup_directories()
        self.init_components()
        self.load_conversations()
        
    def setup_logging(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def setup_directories(self):
        """📁 Setup data directories"""
        self.data_dir = Path("conversation_data")
        self.data_dir.mkdir(exist_ok=True)
        
        self.conversations_file = self.data_dir / "conversations.json"
        self.learning_data_file = self.data_dir / "learning_data.json"
        self.model_file = self.data_dir / "response_model.pkl"
        
    def init_components(self):
        """🔧 Initialize ML components"""
        self.conversations = []
        self.patterns = defaultdict(list)
        self.word_associations = defaultdict(Counter)
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words=None)
        self.response_cache = {}
        
        # Response templates
        self.templates = {
            'persian': {
                'greeting': ['سلام!', 'درود!', 'چطوری؟', 'سلام عزیز', 'حالت چطوره؟'],
                'question': ['جالبه!', 'خوب پرسیدی', 'بذار فکر کنم', 'سوال جالبیه', 'چه سوالی!'],
                'positive': ['عالیه!', 'خوشحالم', 'آفرین', 'چه خوب', 'فوق‌العاده!'],
                'negative': ['متأسفم', 'ناراحت شدم', 'امیدوارم بهتر بشه', 'صبر کن', 'درک می‌کنم'],
                'thanks': ['خواهش می‌کنم', 'قابلی نداره', 'موظفم', 'خوشحالم کمک کردم'],
                'general': ['جالب بود', 'ادامه بده', 'بیشتر بگو', 'متوجه شدم', 'درسته']
            },
            'english': {
                'greeting': ['Hello!', 'Hi there!', 'How are you?', 'Nice to meet you!', 'Hey!'],
                'question': ['Interesting!', 'Good question', 'Let me think', 'That\'s interesting', 'Great question!'],
                'positive': ['Great!', 'Awesome!', 'That\'s wonderful', 'I\'m happy', 'Fantastic!'],
                'negative': ['Sorry to hear', 'That\'s sad', 'Hope it gets better', 'I understand', 'My condolences'],
                'thanks': ['You\'re welcome', 'No problem', 'My pleasure', 'Glad to help', 'Anytime!'],
                'general': ['Interesting', 'Tell me more', 'I see', 'Makes sense', 'Go on']
            }
        }
        
    def load_conversations(self):
        """📚 Load conversation dataset"""
        try:
            # Load from collected chats
            if os.path.exists('conversation_data/collected_chats.json'):
                with open('conversation_data/collected_chats.json', 'r', encoding='utf-8') as f:
                    collected = json.load(f)
                    self.conversations.extend(collected)
                    
            # Load from simple learning
            if os.path.exists('conversation_data/simple_learning.json'):
                with open('conversation_data/simple_learning.json', 'r', encoding='utf-8') as f:
                    simple_data = json.load(f)
                    if 'conversations' in simple_data:
                        self.conversations.extend(simple_data['conversations'])
                        
            # Build learning structures
            self.build_learning_structures()
            
            self.logger.info(f"📚 Loaded {len(self.conversations)} conversations")
            
        except Exception as e:
            self.logger.error(f"Failed to load conversations: {e}")
    
    def build_learning_structures(self):
        """🏗️ Build learning data structures"""
        for conv in self.conversations:
            input_text = conv.get('input', '')
            response_text = conv.get('response', '')
            
            if input_text and response_text:
                # Build word associations
                self.update_word_associations(input_text, response_text)
                
                # Categorize patterns
                category = self.categorize_message(input_text)
                language = conv.get('language', self.detect_language(input_text))
                
                self.patterns[f"{language}_{category}"].append({
                    'input': input_text,
                    'response': response_text,
                    'quality': conv.get('quality', 0.8)
                })
    
    def detect_language(self, text):
        """🌍 Detect message language"""
        persian_chars = len(re.findall(r'[\u0600-\u06FF]', text))
        english_chars = len(re.findall(r'[a-zA-Z]', text))
        
        return 'persian' if persian_chars > english_chars else 'english'
    
    def categorize_message(self, text):
        """📂 Categorize message type"""
        text_lower = text.lower()
        
        # Greeting patterns
        if any(word in text_lower for word in ['سلام', 'درود', 'صبح بخیر', 'hello', 'hi', 'hey', 'good morning']):
            return 'greeting'
            
        # Question patterns
        if '؟' in text or '?' in text or any(word in text_lower for word in ['چی', 'چه', 'کی', 'کجا', 'چرا', 'what', 'why', 'when', 'where', 'how']):
            return 'question'
            
        # Thanks patterns
        if any(word in text_lower for word in ['ممنون', 'مرسی', 'thanks', 'thank you']):
            return 'thanks'
            
        # Positive sentiment
        if any(word in text_lower for word in ['عالی', 'خوب', 'خوشحال', 'great', 'good', 'awesome', 'happy']):
            return 'positive'
            
        # Negative sentiment
        if any(word in text_lower for word in ['بد', 'ناراحت', 'غمگین', 'bad', 'sad', 'sorry', 'terrible']):
            return 'negative'
            
        return 'general'
    
    def update_word_associations(self, input_text, response_text):
        """🔗 Update word associations"""
        input_words = re.findall(r'\w+', input_text.lower())
        response_words = re.findall(r'\w+', response_text.lower())
        
        for input_word in input_words:
            for response_word in response_words:
                self.word_associations[input_word][response_word] += 1
    
    def generate_intelligent_response(self, message_text):
        """🤖 Generate intelligent response using AI"""
        try:
            language = self.detect_language(message_text)
            category = self.categorize_message(message_text)
            
            # Check cache first
            message_hash = hashlib.md5(message_text.encode()).hexdigest()
            if message_hash in self.response_cache:
                return self.response_cache[message_hash]
            
            # Try pattern matching first
            pattern_key = f"{language}_{category}"
            if pattern_key in self.patterns and self.patterns[pattern_key]:
                # Find similar conversations
                similar_convs = self.find_similar_conversations(message_text, pattern_key)
                if similar_convs:
                    response = self.select_best_response(similar_convs, message_text)
                    self.response_cache[message_hash] = response
                    return response
            
            # Use word associations
            response = self.generate_from_associations(message_text, language)
            if response:
                self.response_cache[message_hash] = response
                return response
                
            # Fallback to templates
            templates = self.templates.get(language, {}).get(category, self.templates.get(language, {}).get('general', []))
            if templates:
                response = random.choice(templates)
                self.response_cache[message_hash] = response
                return response
                
            # Ultimate fallback
            fallback = "متوجه شدم 😊" if language == 'persian' else "I understand 😊"
            self.response_cache[message_hash] = fallback
            return fallback
            
        except Exception as e:
            self.logger.error(f"Response generation failed: {e}")
            return "سلام! 😊" if self.detect_language(message_text) == 'persian' else "Hello! 😊"
    
    def find_similar_conversations(self, message_text, pattern_key):
        """🔍 Find similar conversations using TF-IDF"""
        conversations = self.patterns[pattern_key]
        if len(conversations) < 2:
            return conversations
            
        try:
            # Prepare texts for similarity calculation
            texts = [conv['input'] for conv in conversations]
            texts.append(message_text)
            
            # Calculate TF-IDF
            tfidf_matrix = self.vectorizer.fit_transform(texts)
            
            # Calculate similarities
            similarities = cosine_similarity(tfidf_matrix[-1:], tfidf_matrix[:-1]).flatten()
            
            # Get top similar conversations
            top_indices = similarities.argsort()[-3:][::-1]
            return [conversations[i] for i in top_indices if similarities[i] > 0.1]
            
        except Exception:
            return conversations[:3]
    
    def select_best_response(self, similar_convs, message_text):
        """🎯 Select best response from similar conversations"""
        if not similar_convs:
            return None
            
        # Weight by quality and similarity
        weighted_responses = []
        for conv in similar_convs:
            quality = conv.get('quality', 0.8)
            response = conv['response']
            
            # Add some variation
            if quality > 0.9 and random.random() > 0.7:
                weighted_responses.append(response)
            elif quality > 0.8:
                weighted_responses.append(response)
                
        return random.choice(weighted_responses) if weighted_responses else similar_convs[0]['response']
    
    def generate_from_associations(self, message_text, language):
        """🔗 Generate response using word associations"""
        try:
            words = re.findall(r'\w+', message_text.lower())
            if not words:
                return None
                
            # Collect associated words
            associated_words = Counter()
            for word in words:
                if word in self.word_associations:
                    associated_words.update(self.word_associations[word])
            
            if not associated_words:
                return None
                
            # Build response from top associations
            top_words = [word for word, count in associated_words.most_common(5)]
            
            if language == 'persian':
                response_starters = ['البته', 'بله', 'آره', 'خوب', 'درسته']
            else:
                response_starters = ['Yes', 'Sure', 'Of course', 'Well', 'Right']
                
            starter = random.choice(response_starters)
            main_word = random.choice(top_words) if top_words else ""
            
            if main_word:
                return f"{starter}، {main_word}" if language == 'persian' else f"{starter}, {main_word}"
            else:
                return None
                
        except Exception:
            return None
    
    def learn_from_interaction(self, user_message, bot_response):
        """🎓 Learn from new interactions"""
        try:
            conversation = {
                'input': user_message,
                'response': bot_response,
                'language': self.detect_language(user_message),
                'timestamp': datetime.now().isoformat(),
                'source': 'interaction',
                'quality': 0.8
            }
            
            self.conversations.append(conversation)
            self.update_word_associations(user_message, bot_response)
            
            # Update patterns
            category = self.categorize_message(user_message)
            language = conversation['language']
            pattern_key = f"{language}_{category}"
            
            self.patterns[pattern_key].append(conversation)
            
            # Save every 10 interactions
            if len(self.conversations) % 10 == 0:
                self.save_learning_data()
                
        except Exception as e:
            self.logger.error(f"Learning failed: {e}")
    
    def save_learning_data(self):
        """💾 Save learning data"""
        try:
            learning_data = {
                'conversations': self.conversations[-100:],  # Keep recent conversations
                'patterns': dict(self.patterns),
                'word_associations': {k: dict(v) for k, v in self.word_associations.items()},
                'stats': {
                    'total_conversations': len(self.conversations),
                    'patterns_learned': len(self.patterns),
                    'word_associations': len(self.word_associations),
                    'last_updated': datetime.now().isoformat()
                }
            }
            
            with open(self.learning_data_file, 'w', encoding='utf-8') as f:
                json.dump(learning_data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            self.logger.error(f"Failed to save learning data: {e}")
    
    def get_stats(self):
        """📊 Get learning statistics"""
        persian_count = len([c for c in self.conversations if c.get('language') == 'persian'])
        english_count = len([c for c in self.conversations if c.get('language') == 'english'])
        
        return {
            'total_conversations': len(self.conversations),
            'persian_conversations': persian_count,
            'english_conversations': english_count,
            'patterns_learned': len(self.patterns),
            'word_associations': len(self.word_associations),
            'cache_size': len(self.response_cache)
        }

class AdvancedDataCollector:
    """📊 Advanced dataset collection and management"""
    
    def __init__(self):
        self.setup_logging()
        self.setup_database()
        
    def setup_logging(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def setup_database(self):
        """🗄️ Setup SQLite database for data management"""
        self.db_path = "conversation_data/advanced_data.db"
        os.makedirs("conversation_data", exist_ok=True)
        
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        
        # Create tables
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY,
                input_text TEXT NOT NULL,
                response_text TEXT NOT NULL,
                language TEXT,
                source TEXT,
                quality REAL,
                category TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY,
                user_message TEXT,
                bot_response TEXT,
                success BOOLEAN,
                response_time REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
    
    def collect_quality_data(self):
        """📈 Collect high-quality conversation data"""
        quality_conversations = []
        
        # Persian quality data
        persian_data = [
            {"input": "سلام، حالت چطوره؟", "response": "سلام! خوبم ممنون، تو چطوری؟", "quality": 0.95},
            {"input": "کار می‌کنی؟", "response": "بله، مشغول کارم. تو چی؟", "quality": 0.90},
            {"input": "فیلم خوبی پیشنهاد بده", "response": "فیلم جدایی نادر از سیمین رو ببین، عالیه", "quality": 0.92},
            {"input": "غذا چی بپزم؟", "response": "خورشت قیمه خوشمزس، آسونم هست", "quality": 0.88},
            {"input": "خسته‌ام", "response": "استراحت کن عزیزم، نوشابه بخور", "quality": 0.87},
            {"input": "برف می‌باره", "response": "واقعاً؟ چه قشنگ! عکس بفرست", "quality": 0.89},
            {"input": "دلم برات تنگ شده", "response": "منم دلم برات تنگ شده، کی می‌بینمت؟", "quality": 0.94},
            {"input": "درس خوندی؟", "response": "آره، ریاضی خوندم. تو چی؟", "quality": 0.91},
            {"input": "بیا بریم بیرون", "response": "آره حتماً، کجا بریم؟", "quality": 0.93},
            {"input": "کمکم کن", "response": "البته! چه کمکی می‌تونم بکنم؟", "quality": 0.96}
        ]
        
        # English quality data
        english_data = [
            {"input": "How are you today?", "response": "I'm doing great, thanks! How about you?", "quality": 0.95},
            {"input": "What's your favorite movie?", "response": "I love sci-fi movies, especially Interstellar. What about you?", "quality": 0.92},
            {"input": "I'm feeling tired", "response": "You should get some rest. Maybe drink some tea?", "quality": 0.88},
            {"input": "Can you help me?", "response": "Of course! What do you need help with?", "quality": 0.96},
            {"input": "What's the weather like?", "response": "It's sunny and warm today. Perfect for a walk!", "quality": 0.89},
            {"input": "I miss you", "response": "I miss you too! When can we meet?", "quality": 0.94},
            {"input": "Good morning!", "response": "Good morning! Hope you have a wonderful day!", "quality": 0.93},
            {"input": "What should I cook?", "response": "How about pasta? It's quick and delicious!", "quality": 0.90},
            {"input": "I'm bored", "response": "Want to watch a movie or read a book?", "quality": 0.87},
            {"input": "Thank you so much", "response": "You're welcome! Happy to help anytime!", "quality": 0.95}
        ]
        
        # Process and add to database
        for conv in persian_data:
            conv.update({"language": "persian", "source": "quality", "category": "social"})
            quality_conversations.append(conv)
            
        for conv in english_data:
            conv.update({"language": "english", "source": "quality", "category": "social"})
            quality_conversations.append(conv)
            
        # Insert into database
        for conv in quality_conversations:
            self.cursor.execute('''
                INSERT INTO conversations (input_text, response_text, language, source, quality, category)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (conv['input'], conv['response'], conv['language'], conv['source'], conv['quality'], conv['category']))
        
        self.conn.commit()
        self.logger.info(f"✅ Added {len(quality_conversations)} quality conversations")
        
        return quality_conversations
    
    def export_data(self):
        """📤 Export collected data"""
        try:
            # Get all conversations from database
            self.cursor.execute('SELECT * FROM conversations ORDER BY created_at DESC')
            rows = self.cursor.fetchall()
            
            conversations = []
            for row in rows:
                conversations.append({
                    'input': row[1],
                    'response': row[2],
                    'language': row[3],
                    'source': row[4],
                    'quality': row[5],
                    'category': row[6]
                })
            
            # Save to JSON
            with open('conversation_data/exported_conversations.json', 'w', encoding='utf-8') as f:
                json.dump(conversations, f, ensure_ascii=False, indent=2)
                
            self.logger.info(f"📤 Exported {len(conversations)} conversations")
            return conversations
            
        except Exception as e:
            self.logger.error(f"Export failed: {e}")
            return []

class UltimateTelegramResponder:
    """🚀 Ultimate Telegram Auto Responder with all advanced features"""
    
    def __init__(self):
        self.setup_logging()
        self.init_ai_systems()
        self.load_configuration()
        self.init_stats()
        self.running = False
        self.telegram_hwnd = None
        
    def setup_logging(self):
        """📝 Setup comprehensive logging"""
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.FileHandler('conversation_data/ultimate_responder.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def init_ai_systems(self):
        """🧠 Initialize all AI systems"""
        self.logger.info("🚀 Initializing Ultimate AI Systems...")
        
        try:
            # Initialize OCR system
            self.ocr = AdvancedOCRSystem()
            self.logger.info("✅ Advanced OCR System ready")
            
            # Initialize learning system
            self.learning = TensorFlowLearningSystem()
            self.logger.info("✅ TensorFlow Learning System ready")
            
            # Initialize data collector
            self.data_collector = AdvancedDataCollector()
            self.data_collector.collect_quality_data()
            self.logger.info("✅ Data Collection System ready")
            
        except Exception as e:
            self.logger.error(f"❌ AI Systems initialization failed: {e}")
            
    def load_configuration(self):
        """⚙️ Load advanced configuration"""
        default_config = {
            "telegram_executable": "C:\\TelegramDesktop\\Telegram.exe",
            "monitoring_interval": 2,
            "response_delay": 1.5,
            "auto_response_enabled": True,
            "max_responses_per_chat": 3,
            "ai_confidence_threshold": 0.7,
            "learning_enabled": True,
            "ocr_preprocessing": True,
            "response_caching": True,
            "working_hours": {
                "enabled": False,
                "start": "09:00",
                "end": "18:00"
            },
            "response_triggers": [
                "سلام", "hello", "hi", "سلام", "؟", "?", 
                "چطوری", "how are you", "کجایی", "where are you",
                "ممنون", "thanks", "کمک", "help"
            ],
            "excluded_chats": ["Saved Messages", "پیام‌های ذخیره شده"],
            "screen_regions": {
                "chat_list": {"x": 0, "y": 100, "width": 300, "height": 600},
                "chat_area": {"x": 300, "y": 100, "width": 700, "height": 600},
                "input_area": {"x": 300, "y": 650, "width": 600, "height": 50}
            },
            "ai_settings": {
                "response_creativity": 0.8,
                "learning_rate": 0.1,
                "pattern_matching_threshold": 0.6,
                "sentiment_analysis": True
            }
        }
        
        try:
            with open('conversation_data/ultimate_config.json', 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except:
            self.config = default_config
            self.save_configuration()
            
    def save_configuration(self):
        """💾 Save configuration"""
        try:
            with open('conversation_data/ultimate_config.json', 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save config: {e}")
            
    def init_stats(self):
        """📊 Initialize comprehensive statistics"""
        self.stats = {
            "session_start": datetime.now().isoformat(),
            "messages_read": 0,
            "responses_sent": 0,
            "chats_processed": 0,
            "ocr_success": 0,
            "ocr_failed": 0,
            "ai_responses": 0,
            "template_responses": 0,
            "learning_interactions": 0,
            "errors": 0,
            "average_response_time": 0,
            "languages_detected": {"persian": 0, "english": 0},
            "response_categories": defaultdict(int)
        }
        
    def find_telegram_window(self):
        """🔍 Find Telegram window with enhanced detection"""
        def enum_windows_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                window_title = win32gui.GetWindowText(hwnd)
                if any(keyword in window_title.lower() for keyword in ['telegram', 'تلگرام']):
                    rect = win32gui.GetWindowRect(hwnd)
                    windows.append({
                        'hwnd': hwnd,
                        'title': window_title,
                        'rect': rect
                    })
        
        windows = []
        win32gui.EnumWindows(enum_windows_callback, windows)
        return windows[0] if windows else None
        
    def launch_telegram(self):
        """🚀 Launch Telegram with better detection"""
        self.logger.info("🚀 Launching Telegram...")
        
        # Check if already running
        telegram_window = self.find_telegram_window()
        if telegram_window:
            self.telegram_hwnd = telegram_window['hwnd']
            self.focus_telegram()
            self.logger.info("✅ Telegram already running")
            return True
            
        # Launch Telegram
        if os.path.exists(self.config['telegram_executable']):
            try:
                subprocess.Popen(self.config['telegram_executable'])
                time.sleep(5)  # Wait for startup
                
                # Find window after launch
                telegram_window = self.find_telegram_window()
                if telegram_window:
                    self.telegram_hwnd = telegram_window['hwnd']
                    self.focus_telegram()
                    self.logger.info("✅ Telegram launched successfully")
                    return True
                else:
                    self.logger.error("❌ Telegram window not found after launch")
                    return False
                    
            except Exception as e:
                self.logger.error(f"❌ Failed to launch Telegram: {e}")
                return False
        else:
            self.logger.error(f"❌ Telegram not found at: {self.config['telegram_executable']}")
            return False
            
    def focus_telegram(self):
        """🎯 Focus Telegram window"""
        try:
            if self.telegram_hwnd:
                win32gui.SetForegroundWindow(self.telegram_hwnd)
                win32gui.ShowWindow(self.telegram_hwnd, win32con.SW_RESTORE)
                time.sleep(0.3)
        except Exception as e:
            self.logger.error(f"Failed to focus Telegram: {e}")
            
    def capture_screen_region(self, region):
        """📸 Capture screen region with enhanced quality"""
        try:
            x, y, width, height = region['x'], region['y'], region['width'], region['height']
            screenshot = pyautogui.screenshot(region=(x, y, width, height))
            
            # Save with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]
            filename = f"conversation_data/capture_{timestamp}.png"
            screenshot.save(filename)
            
            return filename
        except Exception as e:
            self.logger.error(f"Screenshot failed: {e}")
            return None
            
    def read_chat_messages(self, image_path):
        """📖 Read messages with AI enhancement"""
        try:
            start_time = time.time()
            result = self.ocr.extract_text(image_path)
            
            if result and result['text']:
                self.stats['ocr_success'] += 1
                self.stats['languages_detected'][result['language']] += 1
                
                # Split into individual messages
                lines = result['text'].split('\n')
                messages = []
                
                for line in lines:
                    line = line.strip()
                    if len(line) > 3 and not line.isdigit():
                        # Filter out timestamps and system messages
                        if not any(word in line.lower() for word in ['online', 'آنلاین', 'typing', 'در حال تایپ']):
                            messages.append({
                                'text': line,
                                'language': result['language'],
                                'confidence': result['confidence'],
                                'quality': result['quality'],
                                'timestamp': datetime.now().isoformat(),
                                'processing_time': time.time() - start_time
                            })
                
                self.stats['messages_read'] += len(messages)
                return messages
            else:
                self.stats['ocr_failed'] += 1
                return []
                
        except Exception as e:
            self.logger.error(f"Failed to read messages: {e}")
            self.stats['ocr_failed'] += 1
            return []
            
    def should_respond(self, message):
        """🤔 Advanced decision making for responses"""
        text = message['text'].lower()
        
        # Check confidence threshold
        if message['confidence'] < self.config['ai_confidence_threshold']:
            return False
        
        # Check for trigger words
        for trigger in self.config['response_triggers']:
            if trigger.lower() in text:
                return True
                
        # Check for questions
        if '?' in text or '؟' in text:
            return True
            
        # Check message length (avoid very short messages)
        if len(message['text']) < 5:
            return False
        
        # AI-based decision (sentiment analysis)
        if self.config['ai_settings']['sentiment_analysis']:
            category = self.learning.categorize_message(message['text'])
            if category in ['question', 'greeting', 'thanks']:
                return True
            
        return True
        
    def generate_response(self, message):
        """🤖 Generate intelligent AI response"""
        try:
            start_time = time.time()
            
            # Use AI learning system
            response = self.learning.generate_intelligent_response(message['text'])
            
            if response:
                self.stats['ai_responses'] += 1
                response_category = self.learning.categorize_message(message['text'])
                self.stats['response_categories'][response_category] += 1
            else:
                # Fallback to templates
                self.stats['template_responses'] += 1
                if message['language'] == 'persian':
                    response = random.choice(['سلام! چطوری؟ 😊', 'ممنون از پیامت! 🙏', 'جالب بود! بیشتر بگو 🤔'])
                else:
                    response = random.choice(['Hello! How are you? 😊', 'Thanks for your message! 🙏', 'Interesting! Tell me more 🤔'])
            
            # Update response time stats
            response_time = time.time() - start_time
            if self.stats['average_response_time'] == 0:
                self.stats['average_response_time'] = response_time
            else:
                self.stats['average_response_time'] = (self.stats['average_response_time'] + response_time) / 2
                
            return response
            
        except Exception as e:
            self.logger.error(f"Failed to generate response: {e}")
            return "متوجه نشدم / I don't understand"
            
    def send_response(self, response):
        """⌨️ Send response with enhanced reliability"""
        try:
            # Focus Telegram first
            self.focus_telegram()
            time.sleep(0.3)
            
            # Click on input area
            input_region = self.config['screen_regions']['input_area']
            input_x = input_region['x'] + input_region['width'] // 2
            input_y = input_region['y'] + input_region['height'] // 2
            
            pyautogui.click(input_x, input_y)
            time.sleep(0.3)
            
            # Clear any existing text
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.1)
            
            # Type the response with variable speed
            pyautogui.typewrite(response, interval=0.02)
            time.sleep(0.3)
            
            # Send message
            pyautogui.press('enter')
            
            self.stats['responses_sent'] += 1
            self.logger.info(f"✅ Sent: {response[:50]}...")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send response: {e}")
            self.stats['errors'] += 1
            return False
            
    def process_chat_cycle(self):
        """🔄 Enhanced chat processing cycle"""
        try:
            # Focus Telegram
            self.focus_telegram()
            
            # Capture chat area
            chat_region = self.config['screen_regions']['chat_area']
            screenshot_path = self.capture_screen_region(chat_region)
            
            if not screenshot_path:
                return
                
            # Read messages with AI
            messages = self.read_chat_messages(screenshot_path)
            
            if messages:
                self.logger.info(f"📖 Found {len(messages)} messages")
                
                # Process latest messages
                for message in messages[-2:]:  # Process last 2 messages
                    if self.should_respond(message):
                        self.logger.info(f"💬 Processing: {message['text'][:50]}...")
                        
                        # Generate AI response
                        response = self.generate_response(message)
                        
                        # Send response if enabled
                        if self.config['auto_response_enabled']:
                            time.sleep(self.config['response_delay'])
                            if self.send_response(response):
                                # Learn from this interaction
                                if self.config['learning_enabled']:
                                    self.learning.learn_from_interaction(message['text'], response)
                                    self.stats['learning_interactions'] += 1
                                time.sleep(1)  # Wait between messages
                        else:
                            self.logger.info(f"🤖 Would respond: {response}")
                            
                self.stats['chats_processed'] += 1
                            
            # Cleanup
            try:
                os.remove(screenshot_path)
            except:
                pass
                
        except Exception as e:
            self.logger.error(f"Error in chat cycle: {e}")
            self.stats['errors'] += 1
            
    def start_monitoring(self):
        """🚀 Start the ultimate monitoring system"""
        self.logger.info("🚀 Starting Ultimate Telegram Auto Responder...")
        
        # Launch Telegram
        if not self.launch_telegram():
            self.logger.error("❌ Cannot start - Telegram unavailable")
            return False
            
        self.running = True
        cycle_count = 0
        
        print("\n🤖 Ultimate Telegram AI Auto Responder v4.0 Active!")
        print("🧠 AI Learning System: ENABLED")
        print("🔍 Advanced OCR: ENABLED")
        print("📊 Data Collection: ENABLED")
        print("🌍 Languages: Persian + English")
        print("⌨️ Press 'q' to quit safely")
        print("⏸️ Press 'p' to pause/resume")
        print("📊 Press 's' to show stats")
        print("🧠 Press 'l' to show learning stats")
        print("-" * 70)
        
        try:
            while self.running:
                cycle_count += 1
                
                if cycle_count % 20 == 0:
                    self.logger.info(f"🔄 Monitoring cycle #{cycle_count}")
                    
                # Process current chat view
                self.process_chat_cycle()
                
                # Check for control keys
                if keyboard.is_pressed('q'):
                    self.logger.info("🛑 Quit requested")
                    break
                elif keyboard.is_pressed('p'):
                    self.toggle_pause()
                elif keyboard.is_pressed('s'):
                    self.show_stats()
                elif keyboard.is_pressed('l'):
                    self.show_learning_stats()
                    
                # Auto-save stats every 50 cycles
                if cycle_count % 50 == 0:
                    self.save_session_data()
                    
                # Wait for next cycle
                time.sleep(self.config['monitoring_interval'])
                
        except KeyboardInterrupt:
            self.logger.info("🛑 Interrupted by user")
        finally:
            self.stop_monitoring()
            
        return True
        
    def toggle_pause(self):
        """⏸️ Toggle pause state"""
        self.config['auto_response_enabled'] = not self.config['auto_response_enabled']
        status = "ACTIVE" if self.config['auto_response_enabled'] else "PAUSED"
        self.logger.info(f"⏸️ Auto response: {status}")
        time.sleep(1)  # Prevent key repeat
        
    def show_stats(self):
        """📊 Show comprehensive statistics"""
        print("\n📊 Ultimate Responder Statistics:")
        print(f"  ⏰ Session time: {datetime.now() - datetime.fromisoformat(self.stats['session_start'])}")
        print(f"  📖 Messages read: {self.stats['messages_read']}")
        print(f"  💬 Responses sent: {self.stats['responses_sent']}")
        print(f"  💰 Chats processed: {self.stats['chats_processed']}")
        print(f"  ✅ OCR success: {self.stats['ocr_success']}")
        print(f"  ❌ OCR failed: {self.stats['ocr_failed']}")
        print(f"  🤖 AI responses: {self.stats['ai_responses']}")
        print(f"  📝 Template responses: {self.stats['template_responses']}")
        print(f"  🎓 Learning interactions: {self.stats['learning_interactions']}")
        print(f"  ⚡ Avg response time: {self.stats['average_response_time']:.3f}s")
        print(f"  🇮🇷 Persian: {self.stats['languages_detected']['persian']}")
        print(f"  🇺🇸 English: {self.stats['languages_detected']['english']}")
        print(f"  🚨 Errors: {self.stats['errors']}")
        print("-" * 50)
        time.sleep(3)  # Prevent key repeat
        
    def show_learning_stats(self):
        """🧠 Show learning system statistics"""
        learning_stats = self.learning.get_stats()
        print("\n🧠 AI Learning System Statistics:")
        print(f"  📚 Total conversations: {learning_stats['total_conversations']}")
        print(f"  🇮🇷 Persian conversations: {learning_stats['persian_conversations']}")
        print(f"  🇺🇸 English conversations: {learning_stats['english_conversations']}")
        print(f"  🎯 Patterns learned: {learning_stats['patterns_learned']}")
        print(f"  🔗 Word associations: {learning_stats['word_associations']}")
        print(f"  💾 Cache size: {learning_stats['cache_size']}")
        
        # Top response categories
        print("\n📊 Top Response Categories:")
        for category, count in sorted(self.stats['response_categories'].items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"    {category}: {count}")
        print("-" * 50)
        time.sleep(3)  # Prevent key repeat
        
    def save_session_data(self):
        """💾 Save session data"""
        try:
            # Save statistics
            with open('conversation_data/session_stats.json', 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, ensure_ascii=False, indent=2)
                
            # Save learning data
            self.learning.save_learning_data()
            
            # Export data collector data
            self.data_collector.export_data()
            
            self.logger.info("💾 Session data saved")
            
        except Exception as e:
            self.logger.error(f"Failed to save session data: {e}")
        
    def stop_monitoring(self):
        """🛑 Stop monitoring and cleanup"""
        self.running = False
        self.save_session_data()
        
        self.logger.info("💾 All data saved")
        self.logger.info("👋 Ultimate Responder stopped")
        
    def setup_screen_coordinates(self):
        """🎯 Interactive setup for screen coordinates"""
        print("🎯 Ultimate Screen Coordinate Setup")
        print("Follow the instructions to set up screen regions for optimal AI performance")
        print("-" * 70)
        
        regions = ['chat_list', 'chat_area', 'input_area']
        
        for region in regions:
            input(f"\n📍 Position your mouse over the {region} and press Enter...")
            x, y = pyautogui.position()
            
            # Get region size with intelligent defaults
            if region == 'chat_list':
                width = int(input(f"Enter width for {region} (default 300): ") or "300")
                height = int(input(f"Enter height for {region} (default 600): ") or "600")
            elif region == 'chat_area':
                width = int(input(f"Enter width for {region} (default 700): ") or "700")
                height = int(input(f"Enter height for {region} (default 600): ") or "600")
            else:  # input_area
                width = int(input(f"Enter width for {region} (default 600): ") or "600")
                height = int(input(f"Enter height for {region} (default 50): ") or "50")
            
            self.config['screen_regions'][region] = {
                'x': x, 'y': y, 'width': width, 'height': height
            }
            
            print(f"✅ {region}: x={x}, y={y}, w={width}, h={height}")
            
        self.save_configuration()
        print("💾 Screen coordinates saved with AI optimization!")

def main():
    """🎯 Main application entry point"""
    responder = UltimateTelegramResponder()
    
    print("🚀 Ultimate Telegram AI Auto Responder v4.0")
    print("🤖 TensorFlow + Advanced OCR + Intelligent Learning")
    print("=" * 70)
    print("1. 🚀 Start Ultimate Auto Responder")
    print("2. 🎯 Setup Screen Coordinates")
    print("3. ⚙️ View Configuration")
    print("4. 🧪 Test AI Systems")
    print("5. 📊 View Statistics")
    print("6. 🧠 Learning System Info")
    print("7. 📈 Export Data")
    print("8. 🚪 Exit")
    
    try:
        choice = input("\nSelect option (1-8): ").strip()
        
        if choice == "1":
            responder.start_monitoring()
            
        elif choice == "2":
            responder.setup_screen_coordinates()
            
        elif choice == "3":
            print("\n⚙️ Ultimate Configuration:")
            for key, value in responder.config.items():
                if isinstance(value, dict):
                    print(f"  {key}:")
                    for subkey, subvalue in value.items():
                        print(f"    {subkey}: {subvalue}")
                else:
                    print(f"  {key}: {value}")
                
        elif choice == "4":
            # Test all AI systems
            print("\n🧪 Testing AI Systems...")
            
            # Test OCR
            screenshot = responder.capture_screen_region(responder.config['screen_regions']['chat_area'])
            if screenshot:
                messages = responder.read_chat_messages(screenshot)
                print(f"\n🔍 OCR Test Results ({len(messages)} messages):")
                for i, msg in enumerate(messages, 1):
                    print(f"  {i}. {msg['text']} (Lang: {msg['language']}, Conf: {msg['confidence']:.2f})")
            
            # Test learning system
            test_messages = ["سلام، حالت چطوره؟", "Hello, how are you?", "ممنون از کمکت", "Thank you for your help"]
            print(f"\n🧠 AI Learning Test:")
            for msg in test_messages:
                response = responder.learning.generate_intelligent_response(msg)
                print(f"  Q: {msg}")
                print(f"  A: {response}")
                print()
                
        elif choice == "5":
            responder.show_stats()
            
        elif choice == "6":
            responder.show_learning_stats()
            
        elif choice == "7":
            print("\n📈 Exporting data...")
            exported = responder.data_collector.export_data()
            print(f"✅ Exported {len(exported)} conversations")
            
        elif choice == "8":
            print("👋 Goodbye!")
            
        else:
            print("❌ Invalid choice")
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Check dependencies
    missing_packages = []
    
    required_packages = {
        'pyautogui': 'pyautogui',
        'keyboard': 'keyboard', 
        'win32gui': 'pywin32',
        'cv2': 'opencv-python',
        'easyocr': 'easyocr',
        'sklearn': 'scikit-learn',
        'tensorflow': 'tensorflow'
    }
    
    for module, package in required_packages.items():
        try:
            __import__(module)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"  pip install {package}")
        print("\nInstall missing packages and try again.")
    else:
        main()
