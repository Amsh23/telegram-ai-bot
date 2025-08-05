#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Advanced Telegram Auto Responder
Ultimate system with all features combined
Persian/English auto-response with learning capabilities
"""

import os
import json
import time
import random
import hashlib
import logging
import re
from datetime import datetime
from collections import defaultdict, Counter
from pathlib import Path

# Core dependencies
try:
    import pyautogui
    import keyboard
    AUTOMATION_AVAILABLE = True
except ImportError:
    AUTOMATION_AVAILABLE = False
    print("⚠️ Install automation: pip install pyautogui keyboard")

try:
    import win32gui
    import win32con
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False
    print("⚠️ Install win32: pip install pywin32")

try:
    import cv2
    import numpy as np
    from PIL import Image, ImageEnhance
    VISION_AVAILABLE = True
except ImportError:
    VISION_AVAILABLE = False
    print("⚠️ Install vision: pip install opencv-python pillow")

try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False
    print("⚠️ Install OCR: pip install pytesseract")

class LightweightOCR:
    """🔍 Lightweight OCR using Tesseract"""
    
    def __init__(self):
        self.setup_logging()
        self.confidence_threshold = 0.6
        
    def setup_logging(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def preprocess_image(self, image_path):
        """🔧 Simple image preprocessing"""
        try:
            if not VISION_AVAILABLE:
                return image_path
                
            img = cv2.imread(image_path)
            if img is None:
                return image_path
                
            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Threshold for better text recognition
            _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            
            # Save processed image
            processed_path = image_path.replace('.png', '_processed.png')
            cv2.imwrite(processed_path, thresh)
            
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
        """🔍 Filter real messages"""
        text = text.strip().lower()
        
        if len(text) < 3:
            return False
            
        # Skip UI elements
        ui_elements = [
            'online', 'آنلاین', 'typing', 'در حال تایپ',
            'last seen', 'آخرین بازدید', 'telegram', 'تلگرام'
        ]
        
        for element in ui_elements:
            if element in text:
                return False
                
        return True
    
    def extract_text(self, image_path):
        """📖 Extract text using Tesseract"""
        try:
            if not TESSERACT_AVAILABLE:
                return {
                    'text': 'سلام! چطوری؟',  # Sample text for testing
                    'language': 'persian',
                    'confidence': 0.8
                }
            
            # Preprocess image
            processed_path = self.preprocess_image(image_path)
            
            # Extract text using Tesseract
            text = pytesseract.image_to_string(processed_path, lang='fas+eng')
            
            if not text or not self.is_real_message(text):
                return None
            
            text = text.strip()
            language = self.detect_language(text)
            
            return {
                'text': text,
                'language': language,
                'confidence': 0.8
            }
            
        except Exception as e:
            self.logger.error(f"Text extraction failed: {e}")
            return None

class AdvancedLearningSystem:
    """🧠 Advanced learning system"""
    
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
        
    def init_components(self):
        """🔧 Initialize learning components"""
        self.conversations = []
        self.patterns = defaultdict(list)
        self.word_associations = defaultdict(Counter)
        self.response_cache = {}
        
        # Enhanced response templates
        self.templates = {
            'persian': {
                'greeting': [
                    'سلام!', 'درود!', 'چطوری؟', 'سلام عزیز', 'حالت چطوره؟', 
                    'سلام و علیکم', 'خوش آمدید', 'صبح بخیر', 'عصر بخیر'
                ],
                'question': [
                    'جالبه!', 'خوب پرسیدی', 'بذار فکر کنم', 'سوال جالبیه', 
                    'چه سوالی!', 'باید بررسی کنم', 'فکر می‌کنم که...', 'به نظرم'
                ],
                'positive': [
                    'عالیه!', 'خوشحالم', 'آفرین', 'چه خوب', 'فوق‌العاده!', 
                    'واقعاً که!', 'بسیار خوب', 'محشره', 'دمت گرم'
                ],
                'negative': [
                    'متأسفم', 'ناراحت شدم', 'امیدوارم بهتر بشه', 'صبر کن', 
                    'درک می‌کنم', 'دلم برات می‌سوزه', 'غمگین شدم', 'ببخشید'
                ],
                'thanks': [
                    'خواهش می‌کنم', 'قابلی نداره', 'موظفم', 'خوشحالم کمک کردم', 
                    'همیشه در خدمتم', 'نظر لطفته', 'چه حرفیه', 'فدات شم'
                ],
                'general': [
                    'جالب بود', 'ادامه بده', 'بیشتر بگو', 'متوجه شدم', 'درسته', 
                    'همینطوره', 'آره دقیقا', 'واقعا؟', 'چی؟', 'باشه'
                ]
            },
            'english': {
                'greeting': [
                    'Hello!', 'Hi there!', 'How are you?', 'Nice to meet you!', 
                    'Hey!', 'Good to see you!', 'Welcome!', 'Good morning', 'Good evening'
                ],
                'question': [
                    'Interesting!', 'Good question', 'Let me think', 'That\'s interesting', 
                    'Great question!', 'I need to consider this', 'Hmm...', 'Well...'
                ],
                'positive': [
                    'Great!', 'Awesome!', 'That\'s wonderful', 'I\'m happy', 
                    'Fantastic!', 'Amazing!', 'Excellent!', 'Perfect!', 'Love it!'
                ],
                'negative': [
                    'Sorry to hear', 'That\'s sad', 'Hope it gets better', 'I understand', 
                    'My condolences', 'I feel for you', 'That\'s tough', 'Oh no'
                ],
                'thanks': [
                    'You\'re welcome', 'No problem', 'My pleasure', 'Glad to help', 
                    'Anytime!', 'Happy to help', 'Don\'t mention it', 'Sure thing'
                ],
                'general': [
                    'Interesting', 'Tell me more', 'I see', 'Makes sense', 
                    'Go on', 'That\'s right', 'Really?', 'What?', 'OK', 'Cool'
                ]
            }
        }
        
    def load_conversations(self):
        """📚 Load conversation dataset"""
        try:
            # Load from multiple sources
            conversation_files = [
                'conversation_data/collected_chats.json',
                'conversation_data/simple_learning.json',
                'conversation_data/conversations.json',
                'conversation_data/collected_persian.json',
                'conversation_data/collected_english.json'
            ]
            
            for file_path in conversation_files:
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        
                        if isinstance(data, list):
                            self.conversations.extend(data)
                        elif isinstance(data, dict):
                            if 'conversations' in data:
                                self.conversations.extend(data['conversations'])
                            elif 'chats' in data:
                                self.conversations.extend(data['chats'])
                                
            # Build learning structures
            self.build_learning_structures()
            
            self.logger.info(f"📚 Loaded {len(self.conversations)} conversations")
            
        except Exception as e:
            self.logger.error(f"Failed to load conversations: {e}")
    
    def build_learning_structures(self):
        """🏗️ Build learning data structures"""
        for conv in self.conversations:
            input_text = conv.get('input', conv.get('message', ''))
            response_text = conv.get('response', conv.get('reply', ''))
            
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
        greeting_words = ['سلام', 'درود', 'صبح بخیر', 'عصر بخیر', 'hello', 'hi', 'hey', 'good morning', 'good evening']
        if any(word in text_lower for word in greeting_words):
            return 'greeting'
            
        # Question patterns
        if '؟' in text or '?' in text or any(word in text_lower for word in ['چی', 'چه', 'کی', 'کجا', 'چرا', 'چطور', 'what', 'why', 'when', 'where', 'how', 'who']):
            return 'question'
            
        # Thanks patterns
        thanks_words = ['ممنون', 'مرسی', 'تشکر', 'متشکرم', 'thanks', 'thank you', 'thx']
        if any(word in text_lower for word in thanks_words):
            return 'thanks'
            
        # Positive sentiment
        positive_words = ['عالی', 'خوب', 'خوشحال', 'فوق‌العاده', 'آفرین', 'great', 'good', 'awesome', 'happy', 'excellent']
        if any(word in text_lower for word in positive_words):
            return 'positive'
            
        # Negative sentiment
        negative_words = ['بد', 'ناراحت', 'غمگین', 'متأسف', 'bad', 'sad', 'sorry', 'terrible', 'awful']
        if any(word in text_lower for word in negative_words):
            return 'negative'
            
        return 'general'
    
    def update_word_associations(self, input_text, response_text):
        """🔗 Update word associations"""
        input_words = re.findall(r'\w+', input_text.lower())
        response_words = re.findall(r'\w+', response_text.lower())
        
        for input_word in input_words:
            for response_word in response_words:
                self.word_associations[input_word][response_word] += 1
    
    def find_similar_responses(self, message_text, pattern_key):
        """🔍 Find similar responses"""
        conversations = self.patterns[pattern_key]
        if not conversations:
            return []
            
        # Word matching similarity
        message_words = set(re.findall(r'\w+', message_text.lower()))
        similar_convs = []
        
        for conv in conversations:
            input_words = set(re.findall(r'\w+', conv['input'].lower()))
            similarity = len(message_words & input_words) / max(len(message_words | input_words), 1)
            
            if similarity > 0.1:  # At least 10% word overlap
                similar_convs.append((conv, similarity))
        
        # Sort by similarity and quality
        similar_convs.sort(key=lambda x: x[1] * x[0].get('quality', 0.8), reverse=True)
        
        return [conv for conv, sim in similar_convs[:5]]
    
    def generate_response(self, message_text):
        """🤖 Generate intelligent response"""
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
                similar_convs = self.find_similar_responses(message_text, pattern_key)
                if similar_convs:
                    # Select best response with randomization
                    weights = [conv.get('quality', 0.8) for conv in similar_convs]
                    selected_conv = random.choices(similar_convs, weights=weights)[0]
                    response = selected_conv['response']
                    
                    # Add variation
                    if random.random() > 0.6:
                        response = self.add_variation(response, language)
                    
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
                
                # Add emoji occasionally
                if random.random() > 0.7:
                    response += ' ' + random.choice(['😊', '😄', '🙂', '👍', '❤️', '😉'])
                
                self.response_cache[message_hash] = response
                return response
                
            # Ultimate fallback
            fallback = "متوجه شدم 😊" if language == 'persian' else "I understand 😊"
            self.response_cache[message_hash] = fallback
            return fallback
            
        except Exception as e:
            self.logger.error(f"Response generation failed: {e}")
            return "سلام! 😊" if self.detect_language(message_text) == 'persian' else "Hello! 😊"
    
    def add_variation(self, response, language):
        """🎨 Add natural variation to responses"""
        variations = {}
        
        if language == 'persian':
            variations = {
                'سلام': ['سلام', 'درود', 'سلام علیکم', 'هی'],
                'خوب': ['خوب', 'عالی', 'فوق‌العاده', 'بهترین'],
                'ممنون': ['ممنون', 'مرسی', 'متشکرم', 'دستت درد نکنه'],
                'آره': ['آره', 'بله', 'اوهوم', 'درسته'],
                '😊': ['😊', '😄', '🙂', '😉', '👍']
            }
        else:
            variations = {
                'hello': ['hello', 'hi', 'hey', 'howdy'],
                'good': ['good', 'great', 'excellent', 'awesome'],
                'thanks': ['thanks', 'thank you', 'much appreciated', 'cheers'],
                'yes': ['yes', 'yeah', 'yep', 'sure'],
                '😊': ['😊', '😄', '🙂', '😉', '👍']
            }
        
        for original, opts in variations.items():
            if original in response.lower():
                response = response.replace(original, random.choice(opts))
                
        return response
    
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
            top_words = [word for word, count in associated_words.most_common(2)]
            
            if language == 'persian':
                starters = ['البته', 'بله', 'آره', 'خوب', 'درسته', 'همینطوره', 'اوکی']
                connectors = ['و', 'که', 'اما', 'یعنی', 'پس']
            else:
                starters = ['Yes', 'Sure', 'Of course', 'Well', 'Right', 'Indeed', 'OK']
                connectors = ['and', 'but', 'so', 'that', 'then']
                
            if top_words:
                starter = random.choice(starters)
                main_word = random.choice(top_words)
                
                if language == 'persian':
                    responses = [
                        f"{starter}، {main_word}",
                        f"{main_word} جالبه",
                        f"درباره {main_word} چی؟"
                    ]
                else:
                    responses = [
                        f"{starter}, {main_word}",
                        f"{main_word} is interesting",
                        f"What about {main_word}?"
                    ]
                
                return random.choice(responses)
            else:
                return None
                
        except Exception:
            return None
    
    def add_conversation(self, user_message, bot_response, language):
        """🎓 Learn from new interactions"""
        try:
            conversation = {
                'input': user_message,
                'response': bot_response,
                'language': language,
                'timestamp': datetime.now().isoformat(),
                'source': 'interaction',
                'quality': 0.8
            }
            
            self.conversations.append(conversation)
            self.update_word_associations(user_message, bot_response)
            
            # Update patterns
            category = self.categorize_message(user_message)
            pattern_key = f"{language}_{category}"
            
            self.patterns[pattern_key].append(conversation)
            
            # Save periodically
            if len(self.conversations) % 5 == 0:
                self.save_learning_data()
                
        except Exception as e:
            self.logger.error(f"Learning failed: {e}")
    
    def save_learning_data(self):
        """💾 Save learning data"""
        try:
            learning_data = {
                'conversations': self.conversations[-100:],  # Keep recent conversations
                'patterns': {k: v[-10:] for k, v in self.patterns.items()},  # Keep recent patterns
                'stats': {
                    'total_conversations': len(self.conversations),
                    'patterns_learned': len(self.patterns),
                    'word_associations': len(self.word_associations),
                    'cache_size': len(self.response_cache),
                    'last_updated': datetime.now().isoformat()
                }
            }
            
            filename = 'conversation_data/advanced_learning.json'
            with open(filename, 'w', encoding='utf-8') as f:
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

class AdvancedTelegramResponder:
    """🚀 Advanced Telegram Auto Responder"""
    
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
        os.makedirs('conversation_data', exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.FileHandler('conversation_data/advanced_responder.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def init_ai_systems(self):
        """🧠 Initialize AI systems"""
        self.logger.info("🚀 Initializing Advanced AI Systems...")
        
        try:
            # Initialize OCR system
            self.ocr = LightweightOCR()
            self.logger.info("✅ Lightweight OCR System ready")
            
            # Initialize learning system
            self.learning = AdvancedLearningSystem()
            self.logger.info("✅ Advanced Learning System ready")
            
        except Exception as e:
            self.logger.error(f"❌ AI Systems initialization failed: {e}")
            
    def load_configuration(self):
        """⚙️ Load system configuration"""
        self.config = {
            'check_interval': 2.0,
            'response_delay': (1.5, 3.5),
            'screenshot_delay': 0.5,
            'max_response_length': 250,
            'auto_response_enabled': True,
            'language_detection': True,
            'learning_enabled': True,
            'ocr_confidence_threshold': 0.6,
            'response_probability': 0.8,  # 80% chance to respond
            'max_responses_per_minute': 10
        }
        
        # Load config from file if exists
        try:
            if os.path.exists('advanced_config.json'):
                with open('advanced_config.json', 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    self.config.update(user_config)
                    self.logger.info("📋 Configuration loaded from file")
            else:
                # Save default config
                with open('advanced_config.json', 'w', encoding='utf-8') as f:
                    json.dump(self.config, f, ensure_ascii=False, indent=2)
                    self.logger.info("📋 Default configuration saved")
        except Exception as e:
            self.logger.warning(f"⚠️ Config load warning: {e}")
    
    def init_stats(self):
        """📊 Initialize comprehensive statistics"""
        self.stats = {
            'total_screenshots': 0,
            'successful_ocr': 0,
            'failed_ocr': 0,
            'messages_detected': 0,
            'responses_sent': 0,
            'learning_interactions': 0,
            'session_start': datetime.now().isoformat(),
            'languages_detected': defaultdict(int),
            'response_categories': defaultdict(int),
            'performance_metrics': {
                'avg_ocr_time': 0.0,
                'avg_response_time': 0.0,
                'success_rate': 0.0
            },
            'response_history': [],
            'last_minute_responses': []
        }
        
    def find_telegram_window(self):
        """🔍 Find Telegram Desktop window"""
        try:
            if not WIN32_AVAILABLE:
                self.logger.warning("⚠️ Win32 not available - using fallback mode")
                return True
                
            def enum_windows_callback(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd):
                    window_title = win32gui.GetWindowText(hwnd)
                    if 'telegram' in window_title.lower():
                        windows.append((hwnd, window_title))
                return True
            
            windows = []
            win32gui.EnumWindows(enum_windows_callback, windows)
            
            if windows:
                # Select best match
                for hwnd, title in windows:
                    if 'telegram desktop' in title.lower() or title.lower() == 'telegram':
                        self.telegram_hwnd = hwnd
                        self.logger.info(f"📱 Found Telegram: {title}")
                        return True
                        
                # Fallback to first Telegram window
                self.telegram_hwnd = windows[0][0]
                self.logger.info(f"📱 Using Telegram window: {windows[0][1]}")
                return True
            else:
                self.logger.warning("⚠️ No Telegram window found - continuing in demo mode")
                return True
                
        except Exception as e:
            self.logger.error(f"❌ Window search failed: {e}")
            return True  # Continue anyway
    
    def capture_screen(self):
        """📸 Capture screen"""
        try:
            if not AUTOMATION_AVAILABLE:
                self.logger.warning("⚠️ Automation not available - using demo mode")
                return None
                
            if self.telegram_hwnd and WIN32_AVAILABLE:
                # Focus Telegram window
                win32gui.SetForegroundWindow(self.telegram_hwnd)
                time.sleep(self.config['screenshot_delay'])
            
            # Take screenshot
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"conversation_data/screenshot_{timestamp}.png"
            
            screenshot = pyautogui.screenshot()
            screenshot.save(screenshot_path)
            
            self.stats['total_screenshots'] += 1
            return screenshot_path
            
        except Exception as e:
            self.logger.error(f"❌ Screenshot failed: {e}")
            return None
    
    def process_screenshot(self, screenshot_path):
        """🔍 Process screenshot with OCR"""
        start_time = time.time()
        
        try:
            # Extract text using OCR
            ocr_result = self.ocr.extract_text(screenshot_path)
            
            if not ocr_result:
                self.stats['failed_ocr'] += 1
                return None
            
            self.stats['successful_ocr'] += 1
            
            # Process OCR result
            extracted_text = ocr_result.get('text', '')
            language = ocr_result.get('language', 'unknown')
            confidence = ocr_result.get('confidence', 0.0)
            
            if confidence < self.config['ocr_confidence_threshold']:
                self.logger.warning(f"⚠️ Low OCR confidence: {confidence:.2f}")
                return None
            
            # Update statistics
            processing_time = time.time() - start_time
            self.stats['performance_metrics']['avg_ocr_time'] = (
                (self.stats['performance_metrics']['avg_ocr_time'] + processing_time) / 2
            )
            
            self.stats['languages_detected'][language] += 1
            self.stats['messages_detected'] += 1
            
            self.logger.info(f"📖 Detected text ({language}): {extracted_text[:50]}...")
            
            return {
                'text': extracted_text,
                'language': language,
                'confidence': confidence,
                'processing_time': processing_time
            }
            
        except Exception as e:
            self.logger.error(f"❌ OCR processing failed: {e}")
            self.stats['failed_ocr'] += 1
            return None
    
    def should_respond(self):
        """🤔 Decide whether to respond"""
        # Check response probability
        if random.random() > self.config['response_probability']:
            return False
            
        # Check rate limiting
        current_time = time.time()
        minute_ago = current_time - 60
        
        # Clean old responses
        self.stats['last_minute_responses'] = [
            t for t in self.stats['last_minute_responses'] if t > minute_ago
        ]
        
        # Check if we've exceeded rate limit
        if len(self.stats['last_minute_responses']) >= self.config['max_responses_per_minute']:
            self.logger.warning("⚠️ Response rate limit reached")
            return False
            
        return True
    
    def generate_response(self, message_data):
        """🤖 Generate intelligent response"""
        start_time = time.time()
        
        try:
            if not self.config['auto_response_enabled']:
                return None
                
            if not self.should_respond():
                return None
                
            message_text = message_data['text']
            language = message_data['language']
            
            # Generate response using learning system
            response = self.learning.generate_response(message_text)
            
            if not response:
                # Enhanced fallback responses
                fallback_responses = {
                    'persian': [
                        'جالب بود! 😊', 'ممنون از پیامت', 'چطوری؟', 'حالت خوبه؟',
                        'بیشتر بگو', 'جالبه!', 'آها 🤔', 'درسته'
                    ],
                    'english': [
                        'Interesting! 😊', 'Thanks for your message', 'How are you?', 
                        'Tell me more', 'I see', 'Really?', 'Cool!', 'Right'
                    ],
                    'unknown': ['Hello! 😊', 'سلام! 😊']
                }
                response = random.choice(fallback_responses.get(language, fallback_responses['unknown']))
            
            # Limit response length
            if len(response) > self.config['max_response_length']:
                response = response[:self.config['max_response_length']] + '...'
            
            # Update statistics
            processing_time = time.time() - start_time
            self.stats['performance_metrics']['avg_response_time'] = (
                (self.stats['performance_metrics']['avg_response_time'] + processing_time) / 2
            )
            
            # Categorize response
            category = self.categorize_response(response)
            self.stats['response_categories'][category] += 1
            
            return response
            
        except Exception as e:
            self.logger.error(f"❌ Response generation failed: {e}")
            return None
    
    def categorize_response(self, response):
        """📂 Categorize response type"""
        response_lower = response.lower()
        
        if any(word in response_lower for word in ['سلام', 'درود', 'hello', 'hi']):
            return 'greeting'
        elif any(word in response_lower for word in ['ممنون', 'مرسی', 'thanks', 'thank']):
            return 'thanks'
        elif any(word in response_lower for word in ['عالی', 'خوب', 'great', 'good']):
            return 'positive'
        elif '؟' in response or '?' in response:
            return 'question'
        else:
            return 'general'
    
    def send_response(self, response_text):
        """💬 Send response to Telegram"""
        try:
            if not AUTOMATION_AVAILABLE:
                self.logger.info(f"💬 [DEMO] Would send: {response_text}")
                self.stats['responses_sent'] += 1
                self.stats['last_minute_responses'].append(time.time())
                return True
                
            if not response_text:
                return False
            
            # Add random delay
            delay = random.uniform(*self.config['response_delay'])
            time.sleep(delay)
            
            # Type response
            pyautogui.typewrite(response_text)
            time.sleep(0.5)
            
            # Send message (Enter)
            pyautogui.press('enter')
            
            self.stats['responses_sent'] += 1
            self.stats['last_minute_responses'].append(time.time())
            self.stats['response_history'].append({
                'text': response_text,
                'timestamp': datetime.now().isoformat()
            })
            
            # Keep only recent history
            if len(self.stats['response_history']) > 50:
                self.stats['response_history'] = self.stats['response_history'][-50:]
            
            self.logger.info(f"💬 Response sent: {response_text[:30]}...")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to send response: {e}")
            return False
    
    def learn_from_interaction(self, message_data, response_text):
        """🎓 Learn from interactions"""
        try:
            if not self.config['learning_enabled']:
                return
                
            message_text = message_data['text']
            language = message_data['language']
            
            # Add to learning system
            self.learning.add_conversation(message_text, response_text, language)
            
            self.stats['learning_interactions'] += 1
            
        except Exception as e:
            self.logger.error(f"❌ Learning failed: {e}")
    
    def calculate_success_rate(self):
        """📈 Calculate success rate"""
        total_attempts = self.stats['successful_ocr'] + self.stats['failed_ocr']
        if total_attempts > 0:
            return self.stats['successful_ocr'] / total_attempts
        return 0.0
    
    def print_status(self):
        """📊 Print comprehensive status"""
        success_rate = self.calculate_success_rate()
        self.stats['performance_metrics']['success_rate'] = success_rate
        
        print("\n" + "="*70)
        print("🚀 ADVANCED TELEGRAM RESPONDER STATUS")
        print("="*70)
        print(f"📸 Screenshots: {self.stats['total_screenshots']}")
        print(f"✅ Successful OCR: {self.stats['successful_ocr']}")
        print(f"❌ Failed OCR: {self.stats['failed_ocr']}")
        print(f"📨 Messages detected: {self.stats['messages_detected']}")
        print(f"💬 Responses sent: {self.stats['responses_sent']}")
        print(f"🎓 Learning interactions: {self.stats['learning_interactions']}")
        print(f"📈 Success rate: {success_rate:.1%}")
        
        print(f"\n🌍 Languages detected:")
        for lang, count in self.stats['languages_detected'].items():
            print(f"   {lang}: {count}")
            
        print(f"\n📂 Response categories:")
        for category, count in self.stats['response_categories'].items():
            print(f"   {category}: {count}")
            
        print(f"\n⚡ Performance:")
        metrics = self.stats['performance_metrics']
        print(f"   Avg OCR time: {metrics['avg_ocr_time']:.2f}s")
        print(f"   Avg response time: {metrics['avg_response_time']:.2f}s")
        print(f"   Responses this minute: {len(self.stats['last_minute_responses'])}")
        
        # Learning system stats
        if hasattr(self.learning, 'get_stats'):
            learning_stats = self.learning.get_stats()
            print(f"\n🧠 Learning system:")
            print(f"   Total conversations: {learning_stats.get('total_conversations', 0)}")
            print(f"   Persian conversations: {learning_stats.get('persian_conversations', 0)}")
            print(f"   English conversations: {learning_stats.get('english_conversations', 0)}")
            print(f"   Patterns learned: {learning_stats.get('patterns_learned', 0)}")
            print(f"   Word associations: {learning_stats.get('word_associations', 0)}")
        
        # Recent responses
        if self.stats['response_history']:
            print(f"\n💬 Recent responses:")
            for resp in self.stats['response_history'][-3:]:
                print(f"   {resp['text'][:40]}...")
                
        print("="*70)
    
    def save_session_data(self):
        """💾 Save session data"""
        try:
            session_data = {
                'stats': self.stats,
                'config': self.config,
                'session_end': datetime.now().isoformat(),
                'system_status': {
                    'automation_available': AUTOMATION_AVAILABLE,
                    'win32_available': WIN32_AVAILABLE,
                    'vision_available': VISION_AVAILABLE,
                    'tesseract_available': TESSERACT_AVAILABLE
                }
            }
            
            filename = f"conversation_data/session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, ensure_ascii=False, indent=2)
                
            self.logger.info(f"💾 Session data saved: {filename}")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to save session data: {e}")
    
    def run_monitoring_loop(self):
        """🔄 Main monitoring loop"""
        self.logger.info("🚀 Starting Advanced Telegram Responder...")
        
        if not self.find_telegram_window():
            print("⚠️ Telegram window not found - running in demo mode")
        
        self.running = True
        last_screenshot_text = None
        
        try:
            while self.running:
                try:
                    # In demo mode, simulate message detection
                    if not AUTOMATION_AVAILABLE:
                        demo_messages = [
                            "سلام! چطوری؟",
                            "Hello, how are you?",
                            "چه خبر؟",
                            "What's up?",
                            "ممنون از کمکت",
                            "Thanks for your help"
                        ]
                        
                        message_data = {
                            'text': random.choice(demo_messages),
                            'language': 'persian' if random.random() > 0.5 else 'english',
                            'confidence': 0.9
                        }
                        
                        # Skip if same as last message
                        current_text = message_data['text']
                        if current_text == last_screenshot_text:
                            time.sleep(self.config['check_interval'])
                            continue
                        
                        last_screenshot_text = current_text
                        self.stats['messages_detected'] += 1
                        self.stats['languages_detected'][message_data['language']] += 1
                        
                        print(f"🎭 [DEMO] Simulated message: {current_text}")
                        
                    else:
                        # Capture screenshot
                        screenshot_path = self.capture_screen()
                        if not screenshot_path:
                            time.sleep(self.config['check_interval'])
                            continue
                        
                        # Process screenshot
                        message_data = self.process_screenshot(screenshot_path)
                        if not message_data:
                            time.sleep(self.config['check_interval'])
                            continue
                        
                        # Check if this is a new message
                        current_text = message_data['text']
                        if current_text == last_screenshot_text:
                            time.sleep(self.config['check_interval'])
                            continue
                        
                        last_screenshot_text = current_text
                    
                    # Generate and send response
                    response = self.generate_response(message_data)
                    if response:
                        if self.send_response(response):
                            # Learn from interaction
                            self.learn_from_interaction(message_data, response)
                    
                    # Print status every 5 successful operations
                    if self.stats['messages_detected'] % 5 == 0:
                        self.print_status()
                    
                    time.sleep(self.config['check_interval'])
                    
                except KeyboardInterrupt:
                    self.logger.info("⏹️ Stopping by user request...")
                    break
                except Exception as e:
                    self.logger.error(f"❌ Loop error: {e}")
                    time.sleep(5)  # Wait longer on errors
                    
        except Exception as e:
            self.logger.error(f"❌ Critical error: {e}")
        finally:
            self.running = False
            self.save_session_data()
            self.print_status()
            self.logger.info("🏁 Advanced Telegram Responder stopped")

    def run_interactive_mode(self):
        """🖥️ Interactive control mode"""
        print("\n🚀 ADVANCED TELEGRAM RESPONDER v4.0")
        print("===================================")
        print("🎯 Ultimate AI-powered auto-responder with learning")
        print("🧠 Persian/English conversation processing")
        print("📚 Advanced pattern recognition and response generation")
        print("===================================")
        
        # Show system status
        print(f"\n🔧 System Status:")
        print(f"   Automation: {'✅' if AUTOMATION_AVAILABLE else '❌'}")
        print(f"   Win32: {'✅' if WIN32_AVAILABLE else '❌'}")
        print(f"   Vision: {'✅' if VISION_AVAILABLE else '❌'}")
        print(f"   Tesseract: {'✅' if TESSERACT_AVAILABLE else '❌'}")
        
        if not AUTOMATION_AVAILABLE:
            print("\n🎭 Running in DEMO MODE")
            print("   Install automation: pip install pyautogui keyboard")
        
        print("\n📋 Available Commands:")
        print("   start    - Start monitoring")
        print("   stop     - Stop monitoring") 
        print("   status   - Show current status")
        print("   config   - Show configuration")
        print("   stats    - Show detailed statistics")
        print("   test     - Test response generation")
        print("   learn    - Show learning data")
        print("   demo     - Run demo mode")
        print("   exit     - Exit program")
        print("===================================\n")
        
        while True:
            try:
                command = input("🚀 Enter command: ").strip().lower()
                
                if command == 'start':
                    if not self.running:
                        self.run_monitoring_loop()
                    else:
                        print("✅ Already running!")
                        
                elif command == 'stop':
                    if self.running:
                        self.running = False
                        print("⏹️ Stopping...")
                    else:
                        print("⚠️ Not running!")
                        
                elif command == 'status':
                    self.print_status()
                    
                elif command == 'config':
                    print("\n⚙️ Current Configuration:")
                    for key, value in self.config.items():
                        print(f"   {key}: {value}")
                    print()
                    
                elif command == 'stats':
                    self.print_status()
                    
                elif command == 'test':
                    test_messages = [
                        "سلام! چطوری؟",
                        "Hello, how are you?", 
                        "چه خبر؟",
                        "Thanks for your help",
                        "ممنون از کمکت"
                    ]
                    
                    print("\n🧪 Testing response generation:")
                    for msg in test_messages:
                        response = self.learning.generate_response(msg)
                        print(f"   Input: {msg}")
                        print(f"   Response: {response}")
                        print()
                        
                elif command == 'learn':
                    if hasattr(self.learning, 'get_stats'):
                        stats = self.learning.get_stats()
                        print(f"\n🧠 Learning Statistics:")
                        for key, value in stats.items():
                            print(f"   {key}: {value}")
                    print()
                    
                elif command == 'demo':
                    print("🎭 Running demo mode for 30 seconds...")
                    original_automation = AUTOMATION_AVAILABLE
                    globals()['AUTOMATION_AVAILABLE'] = False
                    
                    old_interval = self.config['check_interval']
                    self.config['check_interval'] = 3.0
                    
                    demo_start = time.time()
                    self.run_monitoring_loop()
                    
                    self.config['check_interval'] = old_interval
                    globals()['AUTOMATION_AVAILABLE'] = original_automation
                    
                elif command == 'exit':
                    if self.running:
                        self.running = False
                    print("👋 Goodbye!")
                    break
                    
                else:
                    print("❌ Unknown command. Available: start, stop, status, config, stats, test, learn, demo, exit")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

def main():
    """🚀 Main function"""
    try:
        print("🚀 Advanced Telegram Auto Responder v4.0")
        print("🎯 Loading AI systems...")
        
        responder = AdvancedTelegramResponder()
        responder.run_interactive_mode()
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        logging.error(f"Fatal error: {e}")

if __name__ == "__main__":
    main()
