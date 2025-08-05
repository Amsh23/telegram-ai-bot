#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Telegram Advanced AI Auto-Reply Bot v3.0
⚡ Powered by TensorFlow, Transformers & Advanced Computer Vision
🧠 Smart Message Analysis with Machine Learning
🎯 Persian/English Dual Language Support
"""

import os
import time
import re
import random
import logging
import json
import numpy as np
import cv2
import easyocr
import pyautogui
import pyperclip
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
from datetime import datetime
from typing import Optional, List, Dict, Tuple, Any
import threading
from collections import deque
import hashlib

# TensorFlow & AI Libraries
import tensorflow as tf
from transformers import pipeline, AutoTokenizer, AutoModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from hazm import Normalizer, word_tokenize

# Import configurations
try:
    from config_advanced import *
    print("✅ Advanced configuration loaded")
except ImportError:
    from config import *
    print("⚠️ Using basic configuration")

# Import learning system
try:
    from learning_system import learning_system, learn_from_interaction, get_learned_response, get_stats
    print("🧠 Learning system loaded successfully")
    LEARNING_ENABLED = True
except ImportError:
    print("⚠️ Learning system not available")
    LEARNING_ENABLED = False

# Configure TensorFlow
tf.config.set_visible_devices([], 'GPU')  # Use CPU for stability
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

class AdvancedLogger:
    """🔍 Advanced logging system with analytics"""
    
    def __init__(self):
        self.setup_logging()
        self.stats = {
            'messages_processed': 0,
            'responses_sent': 0,
            'ocr_accuracy': [],
            'response_time': [],
            'ai_confidence': []
        }
    
    def setup_logging(self):
        """Setup advanced logging"""
        self.logger = logging.getLogger('TelegramAI')
        self.logger.setLevel(getattr(logging, LOG_LEVEL))
        
        # File handler with rotation
        handler = logging.FileHandler(LOG_FILENAME, encoding='utf-8')
        formatter = logging.Formatter(LOG_FORMAT)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
        # Console handler for real-time monitoring
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        self.logger.addHandler(console)
    
    def log_stats(self):
        """Log performance statistics"""
        if self.stats['messages_processed'] > 0:
            avg_response_time = np.mean(self.stats['response_time']) if self.stats['response_time'] else 0
            avg_confidence = np.mean(self.stats['ai_confidence']) if self.stats['ai_confidence'] else 0
            
            self.logger.info(f"📊 PERFORMANCE STATS:")
            self.logger.info(f"   Messages: {self.stats['messages_processed']}")
            self.logger.info(f"   Responses: {self.stats['responses_sent']}")
            self.logger.info(f"   Avg Response Time: {avg_response_time:.2f}s")
            self.logger.info(f"   AI Confidence: {avg_confidence:.2f}")

class AdvancedOCR:
    """🔍 Multi-engine OCR with AI enhancement"""
    
    def __init__(self):
        self.tesseract_config = OCR_CONFIG
        self.languages = OCR_LANGUAGES
        self.easyocr_reader = None
        self.init_easyocr()
        self.ocr_cache = {}
        
    def init_easyocr(self):
        """Initialize EasyOCR with optimized settings"""
        try:
            self.easyocr_reader = easyocr.Reader(['fa', 'en'], gpu=False)
            print("✅ EasyOCR initialized successfully")
        except Exception as e:
            print(f"⚠️ EasyOCR initialization failed: {e}")
    
    def preprocess_image(self, image: Image.Image) -> Image.Image:
        """🎨 Advanced image preprocessing for better OCR"""
        # Convert to OpenCV format
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Noise reduction
        cv_image = cv2.bilateralFilter(cv_image, 9, 75, 75)
        
        # Adaptive thresholding for better text contrast
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        adaptive_thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        
        # Morphological operations to clean up text
        kernel = np.ones((1, 1), np.uint8)
        adaptive_thresh = cv2.morphologyEx(adaptive_thresh, cv2.MORPH_CLOSE, kernel)
        
        # Convert back to PIL
        return Image.fromarray(adaptive_thresh)
    
    def extract_text_multi_engine(self, image: Image.Image) -> Dict[str, Any]:
        """🚀 Multi-engine OCR with confidence scoring"""
        results = {
            'tesseract': {'text': '', 'confidence': 0},
            'easyocr': {'text': '', 'confidence': 0},
            'best': {'text': '', 'confidence': 0, 'engine': ''}
        }
        
        # Create image hash for caching
        img_hash = hashlib.md5(image.tobytes()).hexdigest()
        if img_hash in self.ocr_cache:
            return self.ocr_cache[img_hash]
        
        # Preprocess image
        processed_image = self.preprocess_image(image)
        
        # Tesseract OCR
        try:
            tesseract_data = pytesseract.image_to_data(
                processed_image, lang=self.languages, config=self.tesseract_config, output_type=pytesseract.Output.DICT
            )
            
            # Extract text and calculate confidence
            words = []
            confidences = []
            for i, conf in enumerate(tesseract_data['conf']):
                if int(conf) > 30:  # Filter low confidence words
                    text = tesseract_data['text'][i].strip()
                    if text:
                        words.append(text)
                        confidences.append(int(conf))
            
            if words:
                results['tesseract']['text'] = ' '.join(words)
                results['tesseract']['confidence'] = np.mean(confidences)
        
        except Exception as e:
            print(f"Tesseract error: {e}")
        
        # EasyOCR
        if self.easyocr_reader:
            try:
                easyocr_results = self.easyocr_reader.readtext(np.array(processed_image))
                
                texts = []
                confidences = []
                for (bbox, text, conf) in easyocr_results:
                    if conf > 0.3:  # Filter low confidence
                        texts.append(text)
                        confidences.append(conf * 100)  # Convert to percentage
                
                if texts:
                    results['easyocr']['text'] = ' '.join(texts)
                    results['easyocr']['confidence'] = np.mean(confidences)
            
            except Exception as e:
                print(f"EasyOCR error: {e}")
        
        # Choose best result
        best_engine = 'tesseract'
        if results['easyocr']['confidence'] > results['tesseract']['confidence']:
            best_engine = 'easyocr'
        
        results['best'] = {
            'text': results[best_engine]['text'],
            'confidence': results[best_engine]['confidence'],
            'engine': best_engine
        }
        
        # Cache result
        self.ocr_cache[img_hash] = results
        
        return results

class AIMessageAnalyzer:
    """🧠 Advanced AI-powered message analysis"""
    
    def __init__(self):
        self.normalizer = Normalizer()
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.persian_patterns = self.load_persian_patterns()
        self.conversation_history = deque(maxlen=50)
        self.init_ai_models()
    
    def init_ai_models(self):
        """Initialize AI models"""
        try:
            # Sentiment analysis pipeline
            self.sentiment_analyzer = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                device=-1  # CPU
            )
            print("✅ Sentiment analyzer loaded")
        except Exception as e:
            print(f"⚠️ Sentiment analyzer failed: {e}")
            self.sentiment_analyzer = None
    
    def load_persian_patterns(self) -> List[str]:
        """Load Persian language patterns"""
        return [
            r'[آ-ی]{2,}',  # Persian characters
            r'(چطور|چی|کجا|کی|چرا|چه)',  # Question words
            r'(سلام|درود|احوال)',  # Greetings
            r'(ممنون|مرسی|تشکر)',  # Thanks
            r'(باشه|اوکی|حله)',  # Agreement
            r'(میخوام|میگم|میدونم)',  # Verbs
        ]
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """🎭 Analyze message sentiment"""
        if not self.sentiment_analyzer or not text:
            return {'label': 'NEUTRAL', 'score': 0.5}
        
        try:
            result = self.sentiment_analyzer(text[:512])  # Limit text length
            return result[0] if result else {'label': 'NEUTRAL', 'score': 0.5}
        except:
            return {'label': 'NEUTRAL', 'score': 0.5}
    
    def detect_language(self, text: str) -> Dict[str, float]:
        """🌍 Detect text language with confidence"""
        if not text:
            return {'persian': 0, 'english': 0, 'mixed': 0}
        
        persian_chars = len(re.findall(r'[آ-ی]', text))
        english_chars = len(re.findall(r'[a-zA-Z]', text))
        total_chars = persian_chars + english_chars
        
        if total_chars == 0:
            return {'persian': 0, 'english': 0, 'mixed': 0}
        
        persian_ratio = persian_chars / total_chars
        english_ratio = english_chars / total_chars
        
        if persian_ratio > 0.7:
            return {'persian': persian_ratio, 'english': english_ratio, 'mixed': 0}
        elif english_ratio > 0.7:
            return {'persian': persian_ratio, 'english': english_ratio, 'mixed': 0}
        else:
            return {'persian': persian_ratio, 'english': english_ratio, 'mixed': 1.0}
    
    def extract_intent(self, text: str) -> Dict[str, Any]:
        """🎯 Extract user intent from message"""
        intent_patterns = {
            'greeting': [r'(سلام|hi|hello|hey|درود)', r'(احوال|چطور|how.*are)'],
            'question': [r'(چی|what|چطور|how|کجا|where|چرا|why)', r'[؟?]'],
            'thanks': [r'(ممنون|مرسی|thank|تشکر)', r'(خواهش|welcome)'],
            'goodbye': [r'(خداحافظ|bye|goodbye|فعلا)', r'(برم|رفتم|leaving)'],
            'request': [r'(میخوام|want|need|لطفا|please)', r'(کمک|help)'],
            'complaint': [r'(مشکل|problem|خراب|broken)', r'(نمیتونم|can.*not)'],
            'compliment': [r'(عالی|great|خوب|good|perfect)', r'(دوست.*دارم|love)'],
        }
        
        text_lower = text.lower()
        detected_intents = {}
        
        for intent, patterns in intent_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, text_lower))
                score += matches * 0.3
            
            if score > 0:
                detected_intents[intent] = min(score, 1.0)
        
        # Return most likely intent
        if detected_intents:
            best_intent = max(detected_intents.items(), key=lambda x: x[1])
            return {'intent': best_intent[0], 'confidence': best_intent[1], 'all_intents': detected_intents}
        
        return {'intent': 'unknown', 'confidence': 0, 'all_intents': {}}
    
    def analyze_message_comprehensive(self, text: str) -> Dict[str, Any]:
        """📊 Comprehensive message analysis"""
        if not text:
            return {}
        
        # Normalize Persian text
        normalized_text = self.normalizer.normalize(text)
        
        analysis = {
            'original_text': text,
            'normalized_text': normalized_text,
            'timestamp': time.time(),
            'length': len(text),
            'word_count': len(normalized_text.split()),
            'language': self.detect_language(normalized_text),
            'sentiment': self.analyze_sentiment(normalized_text),
            'intent': self.extract_intent(normalized_text),
            'is_real_message': self.is_real_user_message(normalized_text),
            'toxicity_score': self.calculate_toxicity(normalized_text),
            'complexity_score': self.calculate_complexity(normalized_text)
        }
        
        # Add to conversation history
        self.conversation_history.append(analysis)
        
        return analysis
    
    def is_real_user_message(self, text: str) -> Dict[str, Any]:
        """🔍 Advanced real message detection"""
        if not text or len(text.strip()) < 2:
            return {'is_real': False, 'confidence': 0, 'reasons': ['too_short']}
        
        reasons = []
        score = 0
        
        # Check for real message indicators
        for pattern in REAL_MESSAGE_INDICATORS:
            if re.search(pattern, text, re.IGNORECASE):
                score += 0.2
                reasons.append(f'real_pattern: {pattern[:20]}')
        
        # Check language characteristics
        lang_info = self.detect_language(text)
        if lang_info['persian'] > 0.3 or lang_info['english'] > 0.3:
            score += 0.3
            reasons.append('language_detected')
        
        # Check for interface patterns (negative score)
        interface_count = 0
        for pattern in INTERFACE_PATTERNS:
            if re.search(pattern, text):
                interface_count += 1
                score -= 0.2
        
        if interface_count > 0:
            reasons.append(f'interface_patterns: {interface_count}')
        
        # Check for meaningful words
        words = text.split()
        meaningful_words = 0
        for word in words:
            if (len(word) > 1 and 
                not word.isdigit() and 
                re.search(r'[a-zA-Zآ-ی]', word)):
                meaningful_words += 1
        
        if meaningful_words >= MIN_MEANINGFUL_WORDS:
            score += 0.3
            reasons.append(f'meaningful_words: {meaningful_words}')
        
        # Intent detection adds confidence
        intent_info = self.extract_intent(text)
        if intent_info['confidence'] > 0.5:
            score += 0.2
            reasons.append(f'intent: {intent_info["intent"]}')
        
        is_real = score > 0.5
        return {
            'is_real': is_real,
            'confidence': min(max(score, 0), 1),
            'reasons': reasons,
            'score': score
        }
    
    def calculate_toxicity(self, text: str) -> float:
        """🛡️ Calculate message toxicity score"""
        toxic_patterns = [
            r'(احمق|stupid|idiot)', r'(کثیف|dirty|nasty)',
            r'(لعنت|damn|hell)', r'(برو|go.*away|get.*lost)'
        ]
        
        score = 0
        for pattern in toxic_patterns:
            matches = len(re.findall(pattern, text.lower()))
            score += matches * 0.2
        
        return min(score, 1.0)
    
    def calculate_complexity(self, text: str) -> float:
        """🧮 Calculate message complexity"""
        if not text:
            return 0
        
        words = text.split()
        if not words:
            return 0
        
        # Average word length
        avg_word_length = np.mean([len(word) for word in words])
        
        # Sentence count
        sentences = len(re.split(r'[.!?؟]', text))
        
        # Complexity score
        complexity = (avg_word_length / 10) + (len(words) / 20) + (sentences / 5)
        return min(complexity, 1.0)

class SmartResponseGenerator:
    """🎨 AI-powered response generation"""
    
    def __init__(self):
        self.load_response_templates()
        self.conversation_context = deque(maxlen=10)
        
    def load_response_templates(self):
        """Load advanced response templates"""
        self.templates = {
            'greeting': {
                'formal': [
                    "سلام و احترام! چطور می‌تونم کمکتون کنم؟ 😊",
                    "درود بر شما! در خدمتم 🙏",
                    "سلام عزیز! چه خبر؟ 👋"
                ],
                'casual': [
                    "سلاام! چطوری؟ 😄",
                    "های! چه خبرا؟ 🤗",
                    "سلام داداش! حالت چطوره؟ 😊"
                ]
            },
            'question': {
                'helpful': [
                    "خوب سوال پرسیدی! بذار ببینم... 🤔",
                    "جالب! این موضوع رو بررسی می‌کنم 🔍",
                    "سوال جالبیه! کمی صبر کن تا چک کنم 📝"
                ],
                'clarifying': [
                    "میشه یکم بیشتر توضیح بدی؟ 🤗",
                    "کاملاً متوجه نشدم، دوباره بگو؟ 😅",
                    "یکم گیج شدم! ساده‌تر بگو لطفاً 🙃"
                ]
            },
            'thanks': [
                "خواهش می‌کنم عزیزم! 😊💕",
                "قابلی نداشت! 🤗",
                "همیشه در خدمتم! 😄👍"
            ],
            'goodbye': [
                "فعلاً! مواظب خودت باش! 👋😊",
                "خداحافظ عزیز! موفق باشی! 🌟",
                "بای بای! منتظر برگشتتم! 💕"
            ],
            'confusion': [
                "ببخشید نفهمیدم چی گفتی! 😅",
                "یکم گیج شدم... دوباره بگو؟ 🤔",
                "اوووپس! نگرفتم! توضیح بیشتر لطفاً 😊"
            ],
            'compliment': [
                "وای ممنون! خوشحالم که راضی هستی! 😍",
                "اییی چقدر مهربونی! ممنونم! 🥰",
                "دمت گرم! خیلی لطف داری! 😊💕"
            ]
        }
    
    def generate_contextual_response(self, analysis: Dict[str, Any]) -> str:
        """🎯 Generate contextual response based on analysis"""
        if not analysis.get('is_real_message', {}).get('is_real', False):
            return ""
        
        intent = analysis.get('intent', {}).get('intent', 'unknown')
        sentiment = analysis.get('sentiment', {}).get('label', 'NEUTRAL')
        language = analysis.get('language', {})
        original_text = analysis.get('original_text', '')
        
        # 🧠 Try learning system first if available
        if LEARNING_ENABLED and original_text:
            learned_response = get_learned_response(original_text)
            if learned_response:
                # Log that we used learned response
                logging.info(f"🧠 Using learned response for: '{original_text[:30]}...'")
                return learned_response
        
        # Choose response category based on intent
        if intent == 'greeting':
            category = 'greeting'
            style = 'casual' if sentiment == 'POSITIVE' else 'formal'
            responses = self.templates[category].get(style, self.templates[category]['formal'])
        
        elif intent == 'question':
            category = 'question'
            style = 'helpful' if analysis.get('complexity_score', 0) > 0.5 else 'clarifying'
            responses = self.templates[category].get(style, self.templates[category]['helpful'])
        
        elif intent == 'thanks':
            responses = self.templates['thanks']
        
        elif intent == 'goodbye':
            responses = self.templates['goodbye']
        
        elif intent == 'compliment':
            responses = self.templates['compliment']
        
        else:
            # Check traditional response rules
            traditional_response = self.check_traditional_rules(analysis['normalized_text'])
            if traditional_response:
                return traditional_response
            
            responses = self.templates['confusion']
        
        # Add context awareness
        selected_response = random.choice(responses)
        
        # Add emoji based on sentiment
        if sentiment == 'POSITIVE' and not any(emoji in selected_response for emoji in ['😊', '😄', '🤗', '😍']):
            selected_response += " 😊"
        elif sentiment == 'NEGATIVE':
            selected_response = selected_response.replace('😊', '😔').replace('😄', '🤔')
        
        return selected_response
    
    def check_traditional_rules(self, text: str) -> str:
        """Check traditional response rules from config"""
        text_lower = text.lower()
        
        for rule_name, rule_data in RESPONSE_RULES.items():
            keywords = rule_data['keywords']
            
            matched_keywords = [keyword for keyword in keywords if keyword.lower() in text_lower]
            
            if matched_keywords:
                if 'responses' in rule_data:
                    return random.choice(rule_data['responses'])
                elif 'response' in rule_data:
                    response = rule_data['response']
                    if response == 'current_time':
                        return f"الان ساعت {datetime.now().strftime('%H:%M')} هست! ⏰"
                    return response
        
        return ""

class TelegramAdvancedBot:
    """🚀 Advanced Telegram Auto-Reply Bot with AI"""
    
    def __init__(self):
        print("\n" + "="*60)
        print("🚀 Telegram Advanced AI Bot v3.0 Initializing...")
        print("="*60)
        
        # Initialize components
        self.logger = AdvancedLogger()
        self.ocr = AdvancedOCR()
        self.analyzer = AIMessageAnalyzer()
        self.response_generator = SmartResponseGenerator()
        
        # Bot settings
        self.chat_region = (CHAT_REGION['x'], CHAT_REGION['y'], CHAT_REGION['width'], CHAT_REGION['height'])
        self.input_position = (INPUT_CLICK_POSITION['x'], INPUT_CLICK_POSITION['y'])
        self.check_interval = CHECK_INTERVAL
        self.debug_mode = DEBUG_MODE
        
        # State management
        self.is_running = False
        self.message_cache = {}
        self.performance_monitor = {
            'start_time': time.time(),
            'messages_processed': 0,
            'successful_responses': 0,
            'ocr_calls': 0,
            'ai_analysis_time': []
        }
        
        self.logger.logger.info("🚀 Advanced AI Bot initialized successfully")
        print("✅ All AI components loaded successfully!")
        
    def capture_and_analyze(self) -> Optional[Dict[str, Any]]:
        """📸 Capture screenshot and perform advanced analysis"""
        try:
            # Capture screenshot
            screenshot = pyautogui.screenshot(region=self.chat_region)
            
            if self.debug_mode:
                screenshot.save('debug_screenshot.png')
            
            # Multi-engine OCR
            start_time = time.time()
            ocr_results = self.ocr.extract_text_multi_engine(screenshot)
            ocr_time = time.time() - start_time
            
            self.performance_monitor['ocr_calls'] += 1
            
            # Get best OCR result
            text = ocr_results['best']['text']
            ocr_confidence = ocr_results['best']['confidence']
            ocr_engine = ocr_results['best']['engine']
            
            if not text or len(text.strip()) < 2:
                return None
            
            # AI Analysis
            analysis_start = time.time()
            analysis = self.analyzer.analyze_message_comprehensive(text)
            analysis_time = time.time() - analysis_start
            
            self.performance_monitor['ai_analysis_time'].append(analysis_time)
            
            # Add OCR metadata
            analysis['ocr_info'] = {
                'confidence': ocr_confidence,
                'engine': ocr_engine,
                'processing_time': ocr_time,
                'all_results': ocr_results
            }
            
            if self.debug_mode:
                self.logger.logger.debug(f"📝 OCR [{ocr_engine}]: '{text[:50]}...' (conf: {ocr_confidence:.1f}%)")
                self.logger.logger.debug(f"🧠 AI Analysis: {analysis['intent']['intent']} (conf: {analysis['intent']['confidence']:.2f})")
                self.logger.logger.debug(f"🌍 Language: {max(analysis['language'], key=analysis['language'].get)}")
                self.logger.logger.debug(f"⏱️ Analysis time: {analysis_time:.3f}s")
            
            return analysis
            
        except Exception as e:
            self.logger.logger.error(f"❌ Capture/Analysis error: {e}")
            return None
    
    def should_respond(self, analysis: Dict[str, Any]) -> bool:
        """🤔 Intelligent response decision"""
        if not analysis:
            return False
        
        # Check if it's a real message
        real_message_info = analysis.get('is_real_message', {})
        if not real_message_info.get('is_real', False):
            if self.debug_mode:
                self.logger.logger.debug(f"❌ Not a real message: {real_message_info.get('reasons', [])}")
            return False
        
        # Check OCR confidence
        ocr_confidence = analysis.get('ocr_info', {}).get('confidence', 0)
        if ocr_confidence < 30:  # Very low confidence
            if self.debug_mode:
                self.logger.logger.debug(f"❌ OCR confidence too low: {ocr_confidence}")
            return False
        
        # Check message cache for duplicates
        text_hash = hashlib.md5(analysis['normalized_text'].encode()).hexdigest()
        current_time = time.time()
        
        if text_hash in self.message_cache:
            last_time = self.message_cache[text_hash]
            if current_time - last_time < NEW_MESSAGE_THRESHOLD:
                if self.debug_mode:
                    self.logger.logger.debug("❌ Duplicate message detected")
                return False
        
        self.message_cache[text_hash] = current_time
        
        # Clean old cache entries
        old_entries = [k for k, v in self.message_cache.items() if current_time - v > NEW_MESSAGE_THRESHOLD * 2]
        for k in old_entries:
            del self.message_cache[k]
        
        # Check toxicity
        if analysis.get('toxicity_score', 0) > 0.7:
            if self.debug_mode:
                self.logger.logger.debug("❌ Message too toxic")
            return False
        
        return True
    
    def send_response(self, response: str) -> bool:
        """📤 Send response with advanced error handling"""
        if not response:
            return False
        
        try:
            start_time = time.time()
            
            # Click input field
            pyautogui.click(self.input_position[0], self.input_position[1])
            time.sleep(0.3)
            
            # Clear field
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.1)
            
            # Use clipboard for Persian text
            pyperclip.copy(response)
            time.sleep(0.1)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.3)
            
            # Send message
            pyautogui.press('enter')
            
            send_time = time.time() - start_time
            
            self.performance_monitor['successful_responses'] += 1
            self.logger.stats['responses_sent'] += 1
            self.logger.stats['response_time'].append(send_time)
            
            self.logger.logger.info(f"📤 Response sent: '{response[:30]}...' ({send_time:.2f}s)")
            
            return True
            
        except Exception as e:
            self.logger.logger.error(f"❌ Send error: {e}")
            return False
    
    def run_monitoring_loop(self):
        """🔄 Main monitoring loop with AI processing"""
        self.is_running = True
        self.logger.logger.info("🚀 Advanced AI monitoring started")
        
        print("\n" + "="*60)
        print("🤖 Advanced AI Bot Running")
        print("="*60)
        print(f"📊 Region: {self.chat_region}")
        print(f"⏱️ Interval: {self.check_interval}s")
        print(f"🔍 Debug: {'ON' if self.debug_mode else 'OFF'}")
        print(f"🧠 AI Analysis: ACTIVE")
        print(f"⚡ Multi-Engine OCR: ACTIVE")
        print("="*60)
        print("⚠️ Press Ctrl+C to stop")
        print("🚨 Emergency: Move mouse to corner")
        print("="*60)
        
        try:
            while self.is_running:
                loop_start = time.time()
                
                # Check emergency stop
                mouse_x, mouse_y = pyautogui.position()
                screen_width, screen_height = pyautogui.size()
                if mouse_x < 5 or mouse_y < 5 or mouse_x > screen_width - 5 or mouse_y > screen_height - 5:
                    print("\n🚨 Emergency stop activated!")
                    break
                
                # Capture and analyze
                analysis = self.capture_and_analyze()
                
                if analysis:
                    self.performance_monitor['messages_processed'] += 1
                    self.logger.stats['messages_processed'] += 1
                    
                    # Log detection
                    intent = analysis.get('intent', {}).get('intent', 'unknown')
                    confidence = analysis.get('is_real_message', {}).get('confidence', 0)
                    engine = analysis.get('ocr_info', {}).get('engine', 'unknown')
                    
                    self.logger.logger.info(f"📨 Message detected [{engine}]: '{analysis['original_text'][:50]}...'")
                    self.logger.logger.info(f"🎯 Intent: {intent} | Confidence: {confidence:.2f}")
                    
                    # Decide if we should respond
                    if self.should_respond(analysis):
                        # Generate response
                        response = self.response_generator.generate_contextual_response(analysis)
                        
                        if response:
                            self.logger.logger.info(f"🧠 AI Response: '{response[:50]}...'")
                            
                            # Send response
                            if self.send_response(response):
                                self.logger.logger.info("✅ Response sent successfully")
                                
                                # 🧠 Learn from this interaction
                                if LEARNING_ENABLED:
                                    try:
                                        original_message = analysis.get('original_text', '')
                                        context = {
                                            'intent': analysis.get('intent', {}).get('intent', 'unknown'),
                                            'sentiment': analysis.get('sentiment', {}).get('label', 'NEUTRAL'),
                                            'language': max(analysis.get('language', {}), key=analysis.get('language', {}).get) if analysis.get('language') else 'unknown',
                                            'confidence': analysis.get('is_real_message', {}).get('confidence', 0)
                                        }
                                        learn_from_interaction(original_message, response, context)
                                        self.logger.logger.info(f"🎓 Interaction learned and saved")
                                    except Exception as learn_error:
                                        self.logger.logger.warning(f"⚠️ Learning failed: {learn_error}")
                                
                            else:
                                self.logger.logger.warning("⚠️ Failed to send response")
                        else:
                            if self.debug_mode:
                                self.logger.logger.debug("🤐 No response generated")
                    else:
                        if self.debug_mode:
                            self.logger.logger.debug("🚫 Response not triggered")
                
                # Performance monitoring
                loop_time = time.time() - loop_start
                if loop_time < self.check_interval:
                    time.sleep(self.check_interval - loop_time)
                
                # Log stats every 10 cycles
                if self.performance_monitor['messages_processed'] % 10 == 0 and self.performance_monitor['messages_processed'] > 0:
                    self.log_performance_stats()
                    
        except KeyboardInterrupt:
            print("\n⛔ Bot stopped by user (Ctrl+C)")
        except Exception as e:
            self.logger.logger.error(f"❌ Critical error: {e}")
        finally:
            self.is_running = False
            self.logger.logger.info("🛑 Bot stopped")
            self.log_final_stats()
    
    def log_performance_stats(self):
        """📊 Log performance statistics"""
        uptime = time.time() - self.performance_monitor['start_time']
        avg_ai_time = np.mean(self.performance_monitor['ai_analysis_time']) if self.performance_monitor['ai_analysis_time'] else 0
        
        self.logger.logger.info(f"📊 PERFORMANCE UPDATE:")
        self.logger.logger.info(f"   ⏱️ Uptime: {uptime/60:.1f}m")
        self.logger.logger.info(f"   📨 Messages: {self.performance_monitor['messages_processed']}")
        self.logger.logger.info(f"   📤 Responses: {self.performance_monitor['successful_responses']}")
        self.logger.logger.info(f"   🔍 OCR Calls: {self.performance_monitor['ocr_calls']}")
        self.logger.logger.info(f"   🧠 Avg AI Time: {avg_ai_time:.3f}s")
        
        if self.performance_monitor['messages_processed'] > 0:
            response_rate = (self.performance_monitor['successful_responses'] / self.performance_monitor['messages_processed']) * 100
            self.logger.logger.info(f"   📈 Response Rate: {response_rate:.1f}%")
    
    def log_final_stats(self):
        """📈 Log final statistics"""
        total_time = time.time() - self.performance_monitor['start_time']
        
        print("\n" + "="*60)
        print("📊 FINAL PERFORMANCE REPORT")
        print("="*60)
        print(f"⏱️ Total Runtime: {total_time/60:.1f} minutes")
        print(f"📨 Messages Processed: {self.performance_monitor['messages_processed']}")
        print(f"📤 Responses Sent: {self.performance_monitor['successful_responses']}")
        print(f"🔍 OCR Operations: {self.performance_monitor['ocr_calls']}")
        
        if self.performance_monitor['ai_analysis_time']:
            avg_ai_time = np.mean(self.performance_monitor['ai_analysis_time'])
            print(f"🧠 Average AI Analysis: {avg_ai_time:.3f}s")
        
        if self.performance_monitor['messages_processed'] > 0:
            response_rate = (self.performance_monitor['successful_responses'] / self.performance_monitor['messages_processed']) * 100
            print(f"📈 Response Rate: {response_rate:.1f}%")
        
        # 🧠 Learning system statistics
        if LEARNING_ENABLED:
            try:
                learning_stats = get_stats()
                print(f"🎓 LEARNING SYSTEM STATS:")
                print(f"   📚 Total Conversations Learned: {learning_stats['total_conversations']}")
                print(f"   🎯 Response Patterns: {learning_stats['learned_patterns']}")
                print(f"   👤 User Styles Analyzed: {learning_stats['user_styles']}")
                print(f"   📊 Data Quality Score: {learning_stats['data_quality']}%")
            except Exception as e:
                print(f"   ⚠️ Learning stats unavailable: {e}")
        
        print("="*60)
        
        self.logger.log_stats()

def main():
    """🚀 Main application entry point"""
    print("\n🤖 Starting Telegram Advanced AI Bot v3.0...")
    
    try:
        bot = TelegramAdvancedBot()
        bot.run_monitoring_loop()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
    finally:
        print("\n👋 Bot shutdown complete!")

if __name__ == "__main__":
    main()
